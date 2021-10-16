#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:14
# @Author : jianxlin
# @Site : 
# @File : ec2_report.py
# @Software: PyCharm

from pandasql import sqldf

from libs.report.base import ReportData


class Ec2ReportData(ReportData):
    _NAME = "EC2"
    _STORAGE_COST_NAME = "EbsCost"

    def __init__(self, cw_bill=None, ec2_bill=None, s3_bill=None, other_bill=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cloud_watch_bill = cw_bill
        self._ec2_bill = ec2_bill
        self._aws_other_service_bill = other_bill
        self._s3_bill = s3_bill
        self._report_data = self._ec2_bill.get_ec2_instance_id_mapping()
        self._report_data.rename(columns={"Cost": "RunningCost"})
        self._ec2_run_time = self.ec2_bill.get_running_time()
        self.merge()

        self.report_data.fillna(0.0, inplace=True)

    @property
    def ec2_bill(self):
        return self._ec2_bill

    @property
    def cw_bill(self):
        return self._cloud_watch_bill

    def merge(self):
        self.merge_ec2_running_time_info()
        self.merge_ec2_running_bill()
        self.merge_ec2_cloud_watch_bill()
        self.merge_ebs_bill()
        self.merge_snap_bill()
        self.merge_ec2_other_resource_bill()
        self.merge_ec2_other_bill()
        self.merge_s3_share_bill()
        self.merge_transfer_bill()
        self.merge_cloud_watch_other_bill()
        self.merge_other_service_bill()
        self.merge_total_cost()
        self.insert_to_db()

        # self.merge_storage_deductible_cost()
        # self.merge_ri_purchase_bill()

    def merge_ec2_running_bill(self):
        """
            合并ec2主机基本运行费用。
        :return:
        """
        self.merge_bill_data(self.ec2_bill.get_on_demand_bill(),
                             on=["ResourceId"])

    def merge_service_bill_with_ec2_run_time(self, data=None):
        """
            使用主机运行时间合并账单。
        :param data:
        :return:
        """
        for name, cost in data.values:
            name = "%sCost" % name
            _run_t_tmp = self._ec2_run_time.copy()
            _run_t_tmp[name] = _run_t_tmp["Time%"].map(lambda x: x * cost)
            self.merge_bill_data(_run_t_tmp[["ResourceId", name]])

    def merge_ec2_base_info(self):
        """
            增加ec2主机基础信息。
        :return:
        """

    def merge_ec2_running_time_info(self):
        """
            增加ec2运行时长信息。
        :return:
        """
        self.merge_bill_data(self._ec2_run_time[["ResourceId", "RunTime"]])

    def merge_transfer_bill(self):
        """
            添加网络流量账单。
        :return:
        """
        self.merge_bill_data(self.ec2_bill.get_ec2_transfer_bill())

    def merge_ebs_bill(self):
        """
            添加ebs账单。
        :return:
        """

        self.merge_bill_data(self.ec2_bill.get_ec2_ebs_bill())

    def merge_snap_bill(self):
        """
            添加磁盘快照账单
        :return:
        """
        self.merge_bill_data(self.ec2_bill.get_ec2_snap_bill())

    def merge_ec2_other_resource_bill(self):
        """
            添加Ec2非资源账单
        :return:
        """
        self.merge_service_bill_with_ec2_run_time(self._ec2_bill.get_ec2_other_bill())

    def merge_ec2_other_bill(self):
        """
            添加Ec2其他账单
        :return:
        """
        self.merge_service_bill_with_ec2_run_time(self._ec2_bill.get_other_bill())

    def merge_ec2_cloud_watch_bill(self):
        """
            添加主机监控数据储存费用（CloudWatch：MetricStorage）
        :return:
        """
        self.merge_bill_data(self.cw_bill.get_ec2_metric_storage_bill())

    def merge_cloud_watch_other_bill(self):
        """
            添加cloudWatch其他账单
        :return:
        """
        self.merge_service_bill_with_ec2_run_time(self._cloud_watch_bill.get_cloud_watch_share_bill())

    def merge_s3_share_bill(self):
        """
            添加S3公共资源账单
        :return:
        """
        self.merge_service_bill_with_ec2_run_time(self._s3_bill.get_share_bill())

    def merge_other_service_bill(self):
        """
            添加其他服务费用。
        :return:
        """
        self.merge_service_bill_with_ec2_run_time(self._aws_other_service_bill.get_other_bill())

    # def merge_ri_purchase_bill(self):
    #     """
    #        合并主机当月RI支付费用。
    #     :return:
    #     """
    #     self.merge_bill_data(data=self._ri_record.get_ec2_ri_purchase_info())

    def merge_aws_total_cost(self):
        """
            添加aws账单总计信息。
        :return:
        """
        self.report_data["AwsTotalCost"] = self.report_data.iloc[:, 4:-3].apply(lambda x: x.sum(), axis=1)

    def merge_total_cost(self):
        """
            添加账单总计信息。
        :return:
        """
        self.report_data["TotalCost"] = self.report_data.iloc[:, 6:].apply(lambda x: x.sum(), axis=1)

    def get_dep_total_bill(self):
        """
            查询dep总费用。
        :return:
        """
        dep_tag_name = self._ec2_bill.dep_tag_name

        sql = """
            select %(dep_tag_name)s,sum(TotalCost) as Ec2Cost
            from ec2_report
            group by %(dep_tag_name)s
            """ % locals()
        return sqldf(sql, {"ec2_report": self.report_data})

    def get_dep_additional_bill(self):
        """
            查询dep附加费用。
        :return:
        """

        dep_tag_name = self._ec2_bill.dep_tag_name

        sql = """
            select %(dep_tag_name)s,sum(AdditionalCost) as AdditionalCost
            from ec2_report
            group by %(dep_tag_name)s
            """ % locals()
        return sqldf(sql, {"ec2_report": self.report_data})


if __name__ == '__main__':
    from libs.bill.base import Bill
    from libs.bill.cloudwatch_bill import CloudWatchBill
    from libs.bill.ec2_bill import Ec2Bill
    from libs.bill.other_bill import OtherBill
    from libs.bill.s3_bill import S3Bill

    b = Bill()
    ec2_bill = Ec2Bill(base_bill=b)
    cw_bill = CloudWatchBill(base_bill=b)
    other_bill = OtherBill(base_bill=b, )
    s3_bill = S3Bill(base_bill=b, ec2_bill=ec2_bill)
    erd = Ec2ReportData(ec2_bill=ec2_bill, cw_bill=cw_bill, s3_bill=s3_bill, other_bill=other_bill)
    # erd.insert_to_db()
