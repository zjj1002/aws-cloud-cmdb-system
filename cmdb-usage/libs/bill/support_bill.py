#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:23
# @Author : jianxlin
# @Site : 
# @File : support_bill.py
# @Software: PyCharm

import logging

from pandasql import sqldf
from libs.bill.base import Bill
from libs.decorate import cache


class SupportBill(Bill):
    _service_type = "Support"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_support_bill()

    def __init_support_bill(self):
        """
            出事化EC2费用信息
        :return:
        """
        columns = ",".join(self._user_bill_columns)
        sql = """
            select %(columns)s,Cost
            from bill 
            where ProductName = 'AWS Support BJS (Business)'
            """ % locals()
        self.bill = sqldf(sql, {"bill": self.bill})

    @cache
    def get_support_bill(self):
        """
            获取support账单。
        :return:
        """
        columns = ",".join(["ProductName", ])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.bill})


# main
if __name__ == '__main__':
    b = SupportBill()
    logging.info(b.get_total_bill())
