#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:22
# @Author : jianxlin
# @Site : 
# @File : base.py
# @Software: PyCharm
import logging

from pandasql import sqldf

from libs import config
from libs.bill.base import Bill
from libs.ri_record import RIRecord


class RDSBill(Bill):
    _service_type = "rds"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_rds_bill()

    def __init_rds_bill(self):
        """
            出事化EC2费用信息
        :return:
        """
        columns = ",".join(self._user_bill_columns)
        sql = """
            select %(columns)s,Cost
            from bill 
            where ProductName = 'Amazon Relational Database Service'
            """ % locals()
        bill = sqldf(sql, {"bill": self.bill})
        bill["ResourceId"] = bill["ResourceId"].map(lambda x: x.split(":")[-1])
        self.bill = bill

    def get_rds_bill(self):
        """
            获取rds账单。
        :return:
        """
        columns = ",".join(["ResourceId", "UsageType", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            group by %(columns)s
            """ % locals()
        rds_bill = sqldf(sql, {"bill": self.bill})
        return rds_bill

    def get_id_bu_mapping(self):
        """
            获取资源ID与Bu的对应关系。
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        dep_tag_name = self.dep_tag_name
        sql = """
            select %(columns)s
            from bill 
            group by ResourceId
            """ % locals()
        rds_bill = sqldf(sql, {"bill": self.bill})
        return self.format_dep_name(rds_bill, resource_type="rds")

        # if not rds_bill.empty:
        #     conf_mapping = self.config.get_config("resource_dep_mapping.rds")
        #     rds_bill[self.dep_tag_name] = rds_bill.iloc[:, :] \
        #         .apply(lambda x: x[self.dep_tag_name]
        #     if x[self.dep_tag_name] != 'NULL'
        #     else conf_mapping.get(x["ResourceId"], "NULL"), axis=1)
        #
        # return rds_bill

    def get_rds_run_bill(self):
        """
            查询rds运行费用。
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,sum(Cost) as RunningCost
            from bill 
            where UsageType like '%%HeavyUsage:%%'
            or UsageType like '%%Multi-AZUsage:%%'
            or UsageType like '%%InstanceUsage:%%'
            group by  %(columns)s
            """ % locals()
        rds_bill = sqldf(sql, {"bill": self.bill})
        return rds_bill

    def get_storage_bill(self):
        """
            查询r存储费用
        :return:
        """
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,sum(Cost) as EbsCost
            from bill 
            where UsageType like '%%Storage'
            group by  ResourceId
            """ % locals()
        rds_bill = sqldf(sql, {"bill": self.bill})
        return rds_bill

    def get_data_transfer_bill(self):
        """
            获取数据传输账单。
        :return:
        """
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,sum(Cost) as TransferCost
            from bill 
            where UsageType like '%%DataTransfer%%'
            group by  ResourceId
            """ % locals()
        rds_bill = sqldf(sql, {"bill": self.bill})
        return rds_bill

    def get_service_running_bill_info(self):
        """
            查询RDS运行账单数据。
        :return:
        """
        columns = ",".join(["ResourceId", "UsageType", "Operation", "UsageStartDate"])
        sql = """
                    select %(columns)s,sum(Cost) as RunCost,sum(UsageQuantity) as UsageQuantity
                    from bill 
                    where UsageType like '%%HeavyUsage:%%'
                    or UsageType like '%%Multi-AZUsage:%%'
                    or UsageType like '%%InstanceUsage:%%'
                    group by ResourceId,UsageStartDate
                    """ % locals()
        bill = sqldf(sql, {"bill": self.bill})
        return bill

    def _init_on_demand_price(self):
        from libs.aws.price import RdsOnDemandPrice
        rp = RdsOnDemandPrice()
        self._on_demand_price = rp.on_demand_price


# main
if __name__ == '__main__':
    b = RDSBill()
    logging.info(b.get_id_bu_mapping())
    # rr = RIRecord()
    # ri_bill = rr.rds_record()
    # logging.info(b.get_service_running_bill_info())
    # logging.info(b.get_on_demand_bill(ri_bill=ri_bill))

    # logging.info(b.get_id_bu_mapping())
    # logging.info(b.get_id_bu_mapping())
    # logging.info(b.get_rds_run_bill())
    # logging.info(b.get_storage_bill())
    # logging.info(b.get_data_transfer_bill())
    # logging.info(b.get_unknown_rds_bill())
