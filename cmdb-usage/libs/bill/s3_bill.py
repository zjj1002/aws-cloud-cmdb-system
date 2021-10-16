#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:22
# @Author : jianxlin
# @Site : 
# @File : base.py
# @Software: PyCharm
import logging

from pandasql import sqldf
from libs.bill.base import Bill
from libs.decorate import cache
import pandas as pd


class S3Bill(Bill):
    _service_type = "S3"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_s3_bill()

    def __init_s3_bill(self):
        """
            出事化S3费用信息
        :return:
        """
        columns = ",".join(["ProductName", "ResourceId", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            where ProductName = 'Amazon Simple Storage Service'
            group by %(columns)s

            """ % locals()
        s3_bill = sqldf(sql, {"bill": self.bill})
        self._bill = self.format_dep_name(bill=s3_bill, resource_type='s3')

    @cache
    def get_bu_bucket_bill(self):
        """
            查询BU所属桶账单信息
        :return:
        """
        dep_name = self.dep_tag_name

        sql = """
            select %(dep_name)s,ResourceId,sum(Cost) as Cost
            from bill
            where ResourceId != "NULL"
            group by %(dep_name)s,ResourceId
        """ % locals()
        return sqldf(sql, {"bill": self.bill})

    @cache
    def get_share_bill(self):
        """
            查询共享账单
        :return:
        """
        dep_name = self.dep_tag_name

        sql = """
            select ProductName,sum(Cost) as Cost
            from bill
            where ResourceId == "NULL"
            group by ProductName
        """ % locals()
        return sqldf(sql, {"bill": self.bill})


if __name__ == '__main__':
    b = S3Bill()
    # logging.info(b.get_s3_bill())
    bb = b.get_bu_bucket_bill()
    cc = b.get_share_bill()
    logging.info(bb)
    logging.info(cc)
    # logging.info(bb.loc[,"Cost"])
    # logging.info(b.get_nbu_backup_bill())
    # logging.info(b.get_no_nbu_backup_bill())
