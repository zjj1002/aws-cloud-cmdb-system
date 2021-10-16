#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:23
# @Author : jianxlin
# @Site : 
# @File : other_bill.py
# @Software: PyCharm

import logging

from pandasql import sqldf
from libs.bill.base import Bill
from libs.decorate import cache


class OtherBill(Bill):
    _service_type = "other"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_other_bill()

    def __init_other_bill(self):
        """
            出事化EC2费用信息
        :return:
        """
        columns = ",".join(self._user_bill_columns)
        sql = """
            select %(columns)s,Cost
            from bill 
            where ProductName != 'Amazon Relational Database Service'
            and ProductName != 'AmazonCloudWatch'
            and ProductName != 'Amazon Elastic Compute Cloud'
            and ProductName != 'Amazon Simple Storage Service'
            and ProductName != 'Amazon ElastiCache'
            and ProductName != 'AWS Support BJS (Business)'
            """ % locals()
        self.bill = sqldf(sql, {"bill": self.bill})

    @cache
    def get_other_bill(self):
        """
            获取other账单。
        :return:
        """
        columns = ",".join(["ProductName", ])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            group by %(columns)s
            """ % locals()
        other_bill = sqldf(sql, {"bill": self.bill})
        return other_bill[other_bill["ProductName"] != 'NULL']


# main
if __name__ == '__main__':
    b = OtherBill()
    logging.info(b.get_total_bill())
