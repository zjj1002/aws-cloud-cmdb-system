#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-16 18:12
# @Author : jianxlin
# @Site : 
# @File : bu_total_report.py
# @Software: PyCharm
import logging
from copy import deepcopy

from libs.config import config
from libs.date.report_date import report_date
from libs.db_context import get_db_engine
from libs.report.base import ReportData, get_report_db_date_copy
from settings import const
from libs.report.aws_service_report import AwsServiceReportData


class DepAwsCostReportData(ReportData):
    _BILL_DB_TABLE_NAME = 'aws_project_bill_report'

    def __init__(self, base_bill=None,
                 ec2_report=None,
                 rds_report=None,
                 ebs_report=None,
                 snap_report=None,
                 elastic_cache_report=None,
                 support_bill=None,
                 s3_report=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_bill = base_bill
        self._ec2_report = ec2_report
        self._rds_report = rds_report
        self._elastic_cache_report = elastic_cache_report
        self._ebs_report = ebs_report
        self._s3_report = s3_report
        self._snap_report = snap_report
        self._support_bill = support_bill
        self.report_data = base_bill.dep_list
        self.__merge_bill()

    def __merge_bill(self):
        """
            合并账单信息
        :return:
        """
        self._merge_aws_service_bill()
        self._merge_no_reserved_instance_cost()
        self._merge_support_bill()
        self._merge_aws_bill_tax()
        self._merge_aws_total_cost()
        self._merge_credit()
        self._merge_rounding()
        self.report_data.fillna(0.0, inplace=True)
        self.insert_to_db()

    def _merge_aws_service_bill(self):
        """
            合并aws主要服务账单。
        :return:
        """
        aws_report = AwsServiceReportData()
        self.merge_bill_data(aws_report.report_data, on=self.dep_tag_name)

    def _merge_ec2_bill(self):
        """
            合并ec2账单。
        :return:
        """
        self.merge_bill_data(self._ec2_report.get_dep_total_bill(), on=self.dep_tag_name)

    def _merge_ebs_bill(self):
        """
            合并ebs账单。
        :return:
        """
        self.merge_bill_data(self._ebs_report.get_dep_total_bill(), on=self.dep_tag_name)

    def _merge_snap_bill(self):
        """
            合并snap账单。
        :return:
        """
        self.merge_bill_data(self._snap_report.get_dep_total_bill(), on=self.dep_tag_name)

    def _merge_s3_bill(self):
        """
            合并s3账单。
        :return:
        """
        self.merge_bill_data(self._s3_report.get_dep_total_bill(), on=self.dep_tag_name)

    def _merge_rds_bill(self):
        """
            合并rds账单
        :return:
        """
        self.merge_bill_data(self._rds_report.get_dep_total_bill(), on=self.dep_tag_name)

    def _merge_elastic_cache_bill(self):
        """
            合并ElastiCache账单
        :return:
        """
        self.merge_bill_data(self._elastic_cache_report.get_dep_total_bill(), on=self.dep_tag_name)

    def _merge_credit(self):
        """
            合并credit。
        :return:
        """
        pass
        # self.merge_bill_data(self._base_bill.get_credit(), on=self.dep_tag_name) #liuchuanhao 未开启 先注释

    def _merge_rounding(self):
        """
            合并rounding。
        :return:
        """

        self.merge_bill_data(self._base_bill.get_rounding(), on=self.dep_tag_name)

    def _merge_support_bill(self):
        """
            合并support账单。
        :return:
        """
        support_bill = self._support_bill.get_support_bill()
        support_cost = 0 if support_bill.empty else support_bill.values[0][1]

        total_bill = 0.0
        for cost in self.report_data.sum().values:
            if isinstance(cost, float):
                total_bill += cost

        self.report_data["SupportCost"] = self.report_data.iloc[:, 1:].apply(
            lambda x: support_cost * (x.sum() / total_bill), axis=1)

    def _merge_no_reserved_instance_cost(self):
        ri_cost = self._base_bill.no_reserved_instance_ri_cost
        total_bill = 0.0
        for cost in self.report_data.sum().values:
            if isinstance(cost, float):
                total_bill += cost
        self.report_data["NoReservedRiCost"] = self.report_data.iloc[:, 1:].apply(
            lambda x: ri_cost * (x.sum() / total_bill), axis=1)

    def _merge_aws_bill_tax(self):
        """
            合并税费
        :return:
        """
        self.report_data["TAX"] = self.report_data.iloc[:, 1:].apply(
            lambda x: x.sum() * config.get_config("Tax"), axis=1)

    def _merge_aws_total_cost(self):
        """
            合并AWS总账单。
        :return:
        """
        self.report_data["AwsTotalCost"] = self.report_data.iloc[:, 1:].apply(lambda x: x.sum(), axis=1)

    def _merge_ec2_additional_cost(self):
        """
            合并ec2附加费用。
        :return:
        """
        self.merge_bill_data(self._ec2_report.get_dep_additional_bill(), on=self.dep_tag_name)

    def _merge_dep_total_cost(self):
        """
            合并部门总账单。
        :return:
        """
        self.report_data["TotalCost"] = self.report_data.iloc[:, -2:].apply(lambda x: x.sum(), axis=1)

    def insert_to_db(self):
        """
                    将报告写入数据库
                :return:
                """
        d = deepcopy(self.report_data)
        d['bill_date'] = report_date.report_full_month_as_str
        d = get_report_db_date_copy(d)

        engine = get_db_engine(db_key=const.DEFAULT_DB_KEY)
        clean_sql = """
                    delete from %s
                    where bill_date = '%s'
                """ % (self._BILL_DB_TABLE_NAME, report_date.report_full_month_as_str)
        engine.execute(clean_sql)

        d.to_sql(self._BILL_DB_TABLE_NAME, engine, index=False, if_exists='append')
# if __name__ == '__main__':
#     from libs.bill.base import Bill
#     from libs.bill.cloudwatch_bill import CloudWatchBill
#     from libs.bill.ec2_bill import Ec2Bill
#     from libs.bill.other_bill import OtherBill
#     from libs.bill.s3_bill import S3Bill
#     from libs.bill.rds_bill import RDSBill
#     from libs.config import Config
#     from libs.reports.ec2_report import Ec2ReportData
#
#     conf = Config()
#     b = Bill(config=conf)
#     ec2_bill = Ec2Bill(base_bill=b, config=conf)
#     cw_bill = CloudWatchBill(base_bill=b, config=conf)
#     other_bill = OtherBill(base_bill=b, config=conf)
#     rds_bill = RDSBill(base_bill=b, config=conf)
#     support_bill = SupportBill(base_bill=b, config=conf)
#     s3_bill = S3Bill(base_bill=b, ec2_bill=ec2_bill, config=conf)
#     erd = Ec2ReportData(ec2_bill=ec2_bill, cw_bill=cw_bill, s3_bill=s3_bill, other_bill=other_bill, rds_bill=rds_bill)
#     drd = DepReportData(base_bill=b, ec2_bill=Ec2Bill(base_bill=b), ec2_report=erd, rds_bill=rds_bill,
#                         support_bill=support_bill)
#     logging.info(drd.report_data)
