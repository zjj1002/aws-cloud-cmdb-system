#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:14
# @Author : jianxlin
# @Site : 
# @File : ec2_report.py
# @Software: PyCharm
from pandasql import sqldf

from libs.report.base import ReportData


class SnapReportData(ReportData):
    _NAME = "Snapshot"

    def __init__(self, ec2_bill=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ec2_bill = ec2_bill
        self._report_data = self._ec2_bill.get_no_ec2_snap_bill()
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
        dep_tag_name = self._ec2_bill.dep_tag_name

        sql = """
            select %(dep_tag_name)s,sum(TotalCost) as SnapshotCost
            from ec2_report
            group by %(dep_tag_name)s
            """ % locals()
        return sqldf(sql, {"ec2_report": self.report_data})


if __name__ == '__main__':
    from libs.bill.base import Bill
    from libs.bill.ec2_bill import Ec2Bill

    b = Bill()
    ec2_bill = Ec2Bill(base_bill=b)
    r = SnapReportData(ec2_bill=ec2_bill)
