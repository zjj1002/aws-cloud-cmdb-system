#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:14
# @Author : jianxlin
# @Site : 
# @File : ec2_report.py
# @Software: PyCharm
from pandasql import sqldf

from libs.report.base import ReportData


class RdsReportData(ReportData):
    _NAME = "RDS"
    _STORAGE_COST_NAME = "EbsCost"

    def __init__(self, rds_bill=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rds_bill = rds_bill
        self._report_data = self._rds_bill.get_id_bu_mapping()
        self.merge()
        self.report_data.fillna(0.0, inplace=True)

    @property
    def rds_bill(self):
        return self._rds_bill

    def merge(self):
        """
            合并费用数据。
        :return:
        """
        self.merge_bill_data(self.rds_bill.get_on_demand_bill())
        # self.merge_bill_data(self._ri_record.get_rds_ri_effective_info())
        self.merge_bill_data(self.rds_bill.get_storage_bill())
        self.merge_bill_data(self.rds_bill.get_data_transfer_bill())
        self.merge_total_cost()
        self.insert_to_db()

        # self.merge_storage_deductible_cost()
        # self.merge_bill_data(data=self._ri_record.get_rds_ri_purchase_info())

    def merge_total_cost(self):
        """
            添加账单总计信息。
        :return:
        """
        self.report_data["TotalCost"] = self.report_data.iloc[:, 4:].apply(lambda x: x.sum(), axis=1)

    def get_dep_total_bill(self):
        """
            查询dep总费用。
        :return:
        """
        dep_tag_name = self.dep_tag_name

        sql = """
            select %(dep_tag_name)s,sum(TotalCost) as RdsCost
            from ec2_report
            group by %(dep_tag_name)s
            """ % locals()
        return sqldf(sql, {"ec2_report": self.report_data})


if __name__ == '__main__':
    from libs.bill.base import Bill
    from libs.bill.rds_bill import RDSBill

    b = Bill()
    rds_bill = RDSBill(base_bill=b)
    erd = RdsReportData(rds_bill=rds_bill)
