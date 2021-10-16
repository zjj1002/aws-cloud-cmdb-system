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
from libs.ri_record import RIRecord


class ElastiCacheBill(Bill):
    _service_type = 'elastic_cache'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_ec_bill()

    def __init_ec_bill(self):
        """
            出事化ElastiCache费用信息
        :return:
        """
        columns = ",".join(self._user_bill_columns)
        sql = """
            select %(columns)s,Cost
            from bill 
            where ProductName = 'Amazon ElastiCache'
            """ % locals()
        bill = sqldf(sql, {"bill": self.bill})
        bill["ResourceId"] = bill["ResourceId"].map(lambda x: x.split(":")[-1])
        bill.fillna("NULL", inplace=True)
        self.bill = bill

    def get_ec_bill(self):
        """
            获取ec账单。
        :return:
        """
        columns = ",".join(["ResourceId", "UsageType", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            group by %(columns)s
            """ % locals()
        ec_bill = sqldf(sql, {"bill": self.bill})
        return ec_bill

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
            group by  %(columns)s
            """ % locals()
        bu_info = sqldf(sql, {"bill": self.bill})
        return self.format_dep_name(bu_info, resource_type="elastic_cache")

        # conf_mapping = self.config.get_config("resource_dep_mapping.elastic_cache")
        #
        # if not bu_info.empty:
        #     bu_info[self.dep_tag_name] = bu_info.iloc[:, :] \
        #         .apply(lambda x: x[self.dep_tag_name]
        #     if x[self.dep_tag_name] != 'NULL'
        #     else conf_mapping.get(x["ResourceId"], "NULL"), axis=1)
        #
        # return bu_info

    def get_ec_run_bill(self):
        """
            查询ec运行费用。
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,sum(Cost) as RunningCost
            from bill 
            where UsageType like '%%NodeUsage:%%'
            group by  %(columns)s
            """ % locals()
        ec_bill = sqldf(sql, {"bill": self.bill})
        return ec_bill

    def get_storage_bill(self):
        """
            查询r存储费用
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,sum(Cost) as EbsCost
            from bill 
            where UsageType like '%%Storage%%'
            group by  %(columns)s
            """ % locals()
        ec_bill = sqldf(sql, {"bill": self.bill})
        return ec_bill

    def get_service_running_bill_info(self):
        """
            查询ElastiCache运行账单数据。
        :return:
        """
        columns = ",".join(["ResourceId", "UsageType", "Operation", "UsageStartDate"])
        sql = """
                    select %(columns)s,sum(Cost) as RunCost,sum(UsageQuantity) as UsageQuantity
                    from bill 
                    where UsageType like '%%NodeUsage:%%'
                    group by ResourceId,UsageStartDate
                    """ % locals()
        bill = sqldf(sql, {"bill": self.bill})
        return bill

    def _init_on_demand_price(self):
        """
            初始化Ondemand价格表
        :return:
        """

        sql = """
            select UsageType,Operation,Rate as OnDemandPrice
            from bill 
            where Operation like 'CreateCacheCluster%%'
            group by UsageType,Operation
            """
        bill = sqldf(sql, {"bill": self.bill})
        bill["OnDemandPrice"] = bill["OnDemandPrice"].map(lambda x: float(x))
        self._on_demand_price = bill


# main
if __name__ == '__main__':
    b = ElastiCacheBill()
    rr = RIRecord()
    logging.info(b.get_id_bu_mapping())
    # logging.info(b.get_service_running_bill_info())
    # logging.info(b.get_on_demand_bill(ri_bill=ri_bill))
