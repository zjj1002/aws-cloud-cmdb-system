#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:23
# @Author : jianxlin
# @Site : 
# @File : cloudwatch_bill.py
# @Software: PyCharm
import logging

from pandasql import sqldf
from libs.bill.base import Bill


class CloudWatchBill(Bill):
    _service_type = "CloudWatch"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_cloudwatch_bill()

    def __init_cloudwatch_bill(self):
        """
            出事化EC2费用信息
        :return:
        """
        columns = ",".join(self._user_bill_columns)
        sql = """
            select %(columns)s,Cost
            from bill 
            where ProductName = 'AmazonCloudWatch'
            """ % locals()
        self.bill = sqldf(sql, {"bill": self.bill})

    def get_cloud_watch_share_bill(self):
        """
            获取cloudwatch共享账单。
        :return:
        """
        columns = ",".join(["ProductName", ])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            where Operation != 'MetricStorage:AWS/EC2'
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.bill})

    def get_metric_storage_bill(self):
        """
            获取CloudWatch服务MetricStorage账单。
        :return:
        """
        columns = ",".join(["ResourceId", ])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            where Operation = 'MetricStorage:AWS/EC2'
            group by %(columns)s
            """ % locals()
        _b = sqldf(sql, {"bill": self.bill})
        _b["ResourceId"] = _b["ResourceId"].apply(lambda x: x.split("/")[-1])
        return _b

    def get_ec2_metric_storage_bill(self):
        """
            获取ec2主机MetricStorage账单。
        :return:
        """

        columns = ",".join(["ResourceId", ])
        sql = """
            select %(columns)s,sum(Cost) as Ec2MetricStorageCost
            from bill 
            where ResourceId like 'i-%%'
            group by %(columns)s
            """ % locals()
        _b = sqldf(sql, {"bill": self.get_metric_storage_bill()})
        return _b

    def get_other_metric_storage_bill(self):
        """
            获取ec2主机MetricStorage账单。
        :return:
        """

        columns = ",".join(["ResourceId", ])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            where ResourceId not like 'i-%%'
            group by %(columns)s
            """ % locals()
        _b = sqldf(sql, {"bill": self.get_metric_storage_bill()})
        return _b


# main
if __name__ == '__main__':
    b = CloudWatchBill()
    logging.info(b.get_total_bill())
    # logging.info(b.get_metric_storage_bill())
    # logging.info(b.get_ec2_metric_storage_bill())
    # logging.info(b.get_other_metric_storage_bill())
