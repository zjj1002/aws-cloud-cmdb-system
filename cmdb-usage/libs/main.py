#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:23
# @Author : jianxlin
# @Site :
# @File : main.py
# @Software: PyCharm
import logging

from libs.aws.s3 import S3
from libs.config import config
from libs.decorate import show_running_time

from libs.bill.base import Bill
from libs.bill.ec2_bill import Ec2Bill
from libs.bill.other_bill import OtherBill
from libs.bill.s3_bill import S3Bill
from libs.bill.rds_bill import RDSBill
from libs.bill.elasticache_bill import ElastiCacheBill
from libs.bill.support_bill import SupportBill
from libs.bill.cloudwatch_bill import CloudWatchBill

from libs.report.ec2_report import Ec2ReportData
from libs.report.rds_report import RdsReportData
from libs.report.ebs_report import EbsReportData
from libs.report.s3_report import S3ReportData
from libs.report.snap_report import SnapReportData
from libs.report.elastic_cache_report import ElastiCacheReportData
from libs.report.bu_aws_cost_report import DepAwsCostReportData

from libs.excel.report import Report
from libs.date.report_date import report_date

ReportData = None


def download_cost_detail_report():
    """
        从s3下载成本详细报告。
    :return:
    """
    return True


class NewReport(object):
    def __init__(self):
        self.download_cbr()
        base_bill = Bill()
        self._base_bill = base_bill
        self._report = Report()
        self._ec2_report = None
        self._ebs_report = None
        self._snap_report = None
        self._s3_report = None
        self._elastic_cache_report = None
        self._rds_report = None
        self._dep_aws_bill_report = None
        self._ec2_bill = Ec2Bill(base_bill=base_bill)
        self._support_bill = SupportBill(base_bill=base_bill)
        self._cw_bill = CloudWatchBill(base_bill=base_bill)
        self._other_bill = OtherBill(base_bill=base_bill)
        self._rds_bill = RDSBill(base_bill=base_bill)
        self._ec_bill = ElastiCacheBill(base_bill=base_bill)
        self._s3_bill = S3Bill(base_bill=base_bill)

    def download_cbr(self):
        """

        :return:
        """

        if config.debug_mode:
            logging.info("Skip download bill file from s3.")
            return
        s3 = S3()
        s3.download_cbr()

    @show_running_time
    def create_report(self):
        """
            添加报告
        :return:
        """
        self.append_ec2_report()
        self.append_rds_report()
        self.append_elastic_cache_report()
        self.append_dep_s3_report()
        self.append_dep_ebs_report()
        self.append_dep_snap_report()
        self.append_dep_aws_cost_report()
        self._report.save()

    def send_report(self):
        """
            发送账单报告。
        :return:
        """

    @show_running_time
    def append_ec2_report(self):
        """
            添加ec2主机账单报告。
        :return:
        """
        ec2_report = Ec2ReportData(cw_bill=self._cw_bill,
                                   ec2_bill=self._ec2_bill,
                                   s3_bill=self._s3_bill,
                                   other_bill=self._other_bill)
        self._ec2_report = ec2_report
        self._report.append_sheet(sheet=ec2_report.report_data, name="Ec2报表")

    @show_running_time
    def append_rds_report(self):
        """
            添加RDS账单报告。
        :return:
        """
        rds_report = RdsReportData(rds_bill=self._rds_bill)
        self._rds_report = rds_report
        self._report.append_sheet(sheet=rds_report.report_data, name="RDS报表")

    @show_running_time
    def append_elastic_cache_report(self):
        """
            添加ElastiCache账单报告。
        :return:
        """
        elastic_cache_report = ElastiCacheReportData(ec_bill=self._ec_bill)
        self._elastic_cache_report = elastic_cache_report
        self._report.append_sheet(sheet=elastic_cache_report.report_data, name="ElastiCache报表")

    @show_running_time
    def append_dep_ebs_report(self):
        """
            添加EB账单报告。
        :return:
        """
        ebs_report = EbsReportData(ec2_bill=self._ec2_bill)
        self._ebs_report = ebs_report
        self._report.append_sheet(sheet=ebs_report.report_data, name="磁盘账单报表（部门）")

    @show_running_time
    def append_dep_snap_report(self):
        """
            添加Snap账单报告。
        :return:
        """
        snap_report = SnapReportData(ec2_bill=self._ec2_bill)
        self._snap_report = snap_report
        self._report.append_sheet(sheet=snap_report.report_data, name="磁盘镜像报表（部门）")

    @show_running_time
    def append_dep_s3_report(self):
        """
            添加S3账单报告。
        :return:
        """
        s3_report = S3ReportData(s3_bill=self._s3_bill)
        self._s3_report = s3_report
        self._report.append_sheet(sheet=s3_report.report_data, name="S3费用报表（部门）")

    @show_running_time
    def append_dep_aws_cost_report(self):
        """

        :return:
        """
        dep_report = DepAwsCostReportData(base_bill=self._base_bill,
                                          support_bill=self._support_bill,
                                          ec2_report=self._ec2_report,
                                          ebs_report=self._ebs_report,
                                          snap_report=self._snap_report,
                                          elastic_cache_report=self._elastic_cache_report,
                                          rds_report=self._rds_report,
                                          s3_report=self._s3_report)
        self._dep_aws_bill_report = dep_report
        self._report.append_sheet(sheet=dep_report.report_data, name="BU账单汇总报表(AWS)")


def main():
    """
        工具逻辑处理框架。
    :return:
    """
    from datetime import datetime
    d = datetime(year=2020, month=8, day=11)
    report_date.set_date(date=d)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  #

    new_report = NewReport()
    new_report.create_report()


if __name__ == '__main__':
    main()
