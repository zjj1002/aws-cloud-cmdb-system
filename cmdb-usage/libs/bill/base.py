#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:22
# @Author : jianxlin
# @Site : 
# @File : base.py
# @Software: PyCharm
import logging

import pandas as pd
from pandasql import sqldf
from libs.config import config
from libs.decorate import show_running_time
from libs.tools import instance_type_format
# from libs.bill.billing_cache import BillingCache
from libs.date.report_date import report_date

pd.options.display.float_format = '{:,.10f}'.format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

CACHE = {}


def _instance_additional_rate(ri_type, instance_type):
    """
        统计实例额外的rate
    :return:
    """
    ri_type = ri_type.split(":")[-1]
    instance_type = instance_type.split(":")[-1]
    new_rate = (instance_type_format(instance_type=instance_type) - instance_type_format(
        instance_type=ri_type)) * 1.0 / instance_type_format(
        instance_type=instance_type)
    return 0 if new_rate < 0 else new_rate


class Bill(object):
    _service_type = "Base"

    def __init__(self, base_bill=None):
        logging.info("初始化 %s 数据" % self._service_type)
        self._bill_cache = {}
        self._dep_list = None
        self._no_subscript_bill = None
        self._no_reserved_instance_ri_cost = 0
        self._dep_tag_name = "userproject"
        self._bill_project_tag_name = config.get_config("tag.dep_tag_name")
        self._bill_columns = ["SubscriptionId",
                              "UsageType",
                              "ResourceId",
                              "ProductName",
                              "Operation",
                              "UsageStartDate",
                              "UsageEndDate",
                              "ReservedInstance",
                              "Rate",
                              "RecordType",
                              "UsageQuantity",
                              "UsageStartDate",
                              "AvailabilityZone",
                              "ItemDescription"]

        self._user_bill_columns = self._bill_columns.copy()
        self._user_bill_columns.append("userproject")
        self._bill = None if base_bill is None else base_bill.bill
        self._dep_ec2_running_time = {}
        self._services_bill = {}
        self._on_demand_price = None
        self.__init_bill()
        # self.__set_no_reserved_instance_ri_bill()
        self._init_on_demand_price()

    @property
    def dep_list(self):
        return self._dep_list

    @property
    def no_reserved_instance_ri_cost(self):
        """
            未匹配到任何实例的RI运行费用。
        :return:
        """
        return self._no_reserved_instance_ri_cost

    @property
    def on_demand_price(self):
        return self._on_demand_price

    @property
    def dep_tag_name(self):
        return self._dep_tag_name

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, value):
        self._bill = value

    @show_running_time
    def __init_bill(self):
        """
            读取文件数据。
        :return:
        """
        if self.bill is not None:
            return
        logging.info("读取详单文件..")
        dep_tag_name = self.dep_tag_name
        useful_columns = self._bill_columns
        useful_columns += ["Cost", config.get_config("tag.dep_tag_name")]
        bill = pd.read_csv(filepath_or_buffer=config.cloud_bill_record_path, low_memory=False, usecols=useful_columns)
        bill.rename(columns={self._bill_project_tag_name: dep_tag_name}, inplace=True)
        bill.columns = bill.columns.str.replace(':', '')
        bill.fillna("NULL", inplace=True)

        logging.info("计算部门列表")
        self.__set_dep_list(bill)

        logging.info("读取公共费用信息")
        self.__set_no_subscript_bill(bill)

        usage_start_date = report_date.usage_start_date_as_str
        usage_end_date = report_date.usage_end_date_as_str

        logging.info("读取 %s 费用信息。。" % usage_start_date)
        sql = """
            select *
            from bill 
            where SubscriptionId != "NULL" 
            and UsageStartDate >= '%(usage_start_date)s'
            and UsageEndDate <= '%(usage_end_date)s'
            and not (ReservedInstance = 'Y'
                and ResourceId = "NULL" )
            """ % locals()
        self.bill = sqldf(sql, {"bill": bill})

        # 计算未匹配预留实例费用
        logging.info("计算预留实例费用信息")
        un_reserved_ri_bill = bill[(bill.ReservedInstance == "Y") & (bill.ResourceId == "NULL")]
        bill = None
        self._no_reserved_instance_ri_cost = un_reserved_ri_bill["Cost"].sum()
        # # 添加账单日期
        # self.bill["UsageStartDate"] = self.bill.apply(
        #     lambda b: b.UsageStartDate.split(" ")[0], axis=1)

        # 替换windows证书
        logging.info("替换win证书信息")

        self.bill["Operation"] = self.bill.apply(
            lambda b: b.Operation if b.Operation != "RunInstances:0800" else "RunInstances", axis=1)

        self._init_on_demand_price()

    def get_credit(self):
        """
            功能未开启
        :return:
        """
        sql = """
            select sum(Cost) as Credit
            from bill
            where Cost = 0
        """
        credit = sqldf(sql, {"bill": self._no_subscript_bill})
        credit[self.dep_tag_name] = config.get_config("credit_bu_name")
        return 0

    def get_rounding(self):
        sql = """
            select sum(Cost) as Rounding
            from bill 
            where RecordType = 'Rounding'
        """
        rounding = sqldf(sql, {"bill": self._no_subscript_bill})
        rounding[self.dep_tag_name] = config.get_config("credit_bu_name")
        return rounding

    def __set_dep_list(self, bill=None):
        """
            查询dep列表
        :return:
        """
        dep = self.dep_tag_name
        sql = """
            select %(dep)s
            from bill
            group by %(dep)s
            """ % locals()
        dep_list = sqldf(sql, {"bill": bill})
        dep_list[dep] = dep_list[dep].apply(lambda d: d.lower())
        dep_list = sqldf(sql, {"bill": dep_list})
        logging.info("Department list:")
        logging.info(dep_list)
        self._dep_list = dep_list

    def __set_no_subscript_bill(self, bill=None):
        """
            读取非订阅账单
        :return:
        """
        logging.info("Set no subscript bill")
        self._no_subscript_bill = bill[(bill.SubscriptionId == "NULL")]
        # logging.info(self._no_subscript_bill)

    def get_total_bill(self):
        """
            查询总账单。
        :return:
        """
        sql = """
            select UsageType,sum(Cost) as Cost
            from bill
            group by UsageType
            """

        logging.info(sqldf(sql, env={"bill": self.bill}))

        sql = """
            select sum(Cost) as Cost
            from bill
            """

        logging.info(sqldf(sql, env={"bill": self.bill}))

    def format_dep_name(self, bill=None, resource_type=None):
        """
            格式化部门名称。
        :return:
        """
        if bill.empty:
            return bill

        def _fun(row):
            """
                lambda 方法
            :param row:
            :return:
            """
            dep_mapping = config.get_config("resource_dep_mapping")
            dep_name_alias = config.get_config("department_name_alias")
            dep_name = row[self.dep_tag_name]
            if dep_name == "NULL":
                dep_name = dep_mapping.get(row["ResourceId"], dep_name)
            new_dep_name = dep_name_alias.get(dep_name, dep_name)

            new_dep_name = new_dep_name.lower()

            return new_dep_name

        bill[self.dep_tag_name] = bill.iloc[:, :].apply(lambda x: _fun(x), axis=1)

        bill.drop_duplicates(
            subset=['ResourceId'],
            keep='first',
            inplace=True)
        return bill

    def get_service_running_bill_info(self):
        """
            获取服务运行账单数据。
        :return:
            type:DataFrame
                columns:
                    ResourceId
                    UsageType
                    UsageStartDate
                    RunCost
        """
        return None

    def get_instance_run_info(self):

        instance_running_info = self.get_service_running_bill_info()

        # 添加单价
        instance_running_info = instance_running_info.merge(self.on_demand_price, how='left',
                                                            on=("UsageType", "Operation"))

        # # 格式化时间样式
        # instance_running_info["UsageStartDate"] = instance_running_info["UsageStartDate"].apply(
        #     lambda x: x.split(":")[0])

        # # 添加RI账单
        # instance_running_info = instance_running_info.merge(ri_bill, how='left',
        #                                                     on=("ResourceId", "UsageStartDate"))
        values = {"Cost": 0.0, "Rate": 1, "OnDemandPrice": -1}
        instance_running_info = instance_running_info.fillna(value=values)

        _err = instance_running_info[(instance_running_info.OnDemandPrice < 0)]
        if not _err.empty:
            logging.info(_err[["ResourceId", "UsageType", "Operation"]].drop_duplicates())
            raise Exception("未知实例类型")

        # def _additional_rate(info):
        #     if info["Operation_x"] != "RunInstances":
        #         # 与预留实例类型不匹配实例，全部以OnDemand计算。
        #         if info["InstanceType"] != info["UsageType"].split(":")[-1]:
        #             return 1
        #         return info["Rate"]
        #     if info["Rate"] == 1:
        #         return info["Rate"]
        #     if self._service_type != "ec2":
        #         return info["Rate"]
        #     return _instance_additional_rate(ri_type=info["InstanceType"], instance_type=info["UsageType"])
        #
        # if not instance_running_info.empty:
        #     instance_running_info["Rate"] = instance_running_info.apply(lambda info: _additional_rate(info), axis=1)
        #
        # instance_running_info["UsageQuantity"] = instance_running_info.UsageQuantity * instance_running_info.Rate
        return instance_running_info

    def get_on_demand_bill(self):
        """
            获取按需运行账单。
        :return:
        """

        sql = """
            select ResourceId,sum(OnDemandPrice * UsageQuantity)  as OnDemandTheoreticCost,sum(RunCost) as RunCost,sum(UsageQuantity) as OnDemandHours
            from info
            group by ResourceId
            """

        bill = sqldf(sql, env={"info": self.get_instance_run_info()})

        cost = bill.RunCost.sum()
        on_demand_total_theoretic_cost = bill.OnDemandTheoreticCost.sum()
        bill["OnDemandCost"] = bill["OnDemandTheoreticCost"].apply(
            lambda c: (c / on_demand_total_theoretic_cost) * cost)
        return bill[
            ["ResourceId", "OnDemandHours", "OnDemandTheoreticCost", "OnDemandCost"]]

    def _init_on_demand_price(self):
        """
            出事化按需单价。
        :return:
        """
        pass

    def get_ec2_ri_value(self):
        """
            查询当月EC2 RI实例匹配容量信息。
        """
        sql = """
            select ResourceId,UsageType,Operation,sum(UsageQuantity) as RunHours
            from record
            group by ResourceId,UsageType,Operation 
        """
        record = sqldf(sql, {"record": self.get_service_running_bill_info()})
        # record["UsageType"] = record.apply(lambda r: r.UsageType.split(":")[-1], axis=1)
        return record


if __name__ == '__main__':
    b = Bill()
    logging.info(b.get_ec2_ri_value())
    # logging.info(b.get_on_demand_bill())
