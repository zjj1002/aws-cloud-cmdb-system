#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:14
# @Author : jianxlin
# @Site : 
# @File : ec2_report.py
# @Software: PyCharm
import logging
from datetime import datetime

import pandas as pd
from libs.report.base import ReportData
from libs.tools import get_lower_case_name

from settings import const

from libs.db_context import get_db_engine
from libs.date.report_date import report_date


class AwsServiceReportData(ReportData):
    """
        从数据库中读取本月所有账单数据。
    """
    _NAME = "AWS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._report_data = None
        self.__init_report()

    def __init_report(self):
        """
            获取主要服务账单报告。
        :return:
        """
        dep = get_lower_case_name(self.dep_tag_name)

        report_month = report_date.report_month.strftime("%Y-%m-%d 00:00:00")
        report_last_month = report_date.report_last_month.strftime("%Y-%m-%d 00:00:00")

        con = get_db_engine(db_key=const.DEFAULT_DB_KEY)

        sql = """
            select %(dep)s,service_name,sum(total_cost) as cost 
            from aws_service_bill_report  
            where bill_date >= '%(report_month)s' 
            and bill_date < '%(report_last_month)s' 
            group by %(dep)s,service_name;
        """ % locals()
        bu_service_cost = pd.read_sql(sql=sql, con=con)

        bu_service_cost.fillna(0.0, inplace=True)
        bu_service_cost = bu_service_cost.set_index([dep, 'service_name'])
        bu_service_cost = bu_service_cost.unstack()
        bu_service_cost.columns = list(bu_service_cost.columns.get_level_values(1))

        bu_service_cost.rename(columns={
            "EBS": "ebs_cost",
            "EC2": "ec2_cost",
            "ElastiCache": "elasticache_cost",
            "S3": "s3_cost",
            "Snapshot": "snapshot_cost",
            "RDS": "rds_cost"
        }, inplace=True)

        bu_service_cost.reset_index()
        self._report_data = bu_service_cost


if __name__ == '__main__':
    pass
