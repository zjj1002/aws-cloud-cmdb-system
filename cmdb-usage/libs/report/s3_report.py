#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:14
# @Author : jianxlin
# @Site : 
# @File : s3_report.py
# @Software: PyCharm
from pandasql import sqldf

from libs.report.base import ReportData


class S3ReportData(ReportData):
    _NAME = "S3"

    def __init__(self, s3_bill=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._s3_bill = s3_bill
        self._report_data = self._s3_bill.get_bu_bucket_bill()
        self.merge()
        self.report_data.fillna(0.0, inplace=True)

    @property
    def s3_bill(self):
        return self._s3_bill

    def merge(self):
        """
            合并费用数据。
        :return:
        """
        self.merge_total_cost()
        self.insert_to_db()


    def merge_total_cost(self):
        """
            添加账单总计信息。
        :return:
        """
        self.report_data["TotalCost"] = self.report_data.iloc[:, 2:].apply(lambda x: x.sum(), axis=1)

    def get_dep_total_bill(self):
        """
            查询dep总费用。
        :return:
        """
        dep_tag_name = self.dep_tag_name

        sql = """
            select %(dep_tag_name)s,sum(TotalCost) as S3Cost
            from s3_report
            group by %(dep_tag_name)s
            """ % locals()
        return sqldf(sql, {"s3_report": self.report_data})


if __name__ == '__main__':
    from libs.bill.base import Bill
    from libs.bill.s3_bill import S3Bill
    b = Bill()
    s3_bill = S3Bill(base_bill=b)
    erd = S3ReportData(s3_bill=s3_bill)
    erd.insert_to_db()
    # logging.info(erd.report_data)
