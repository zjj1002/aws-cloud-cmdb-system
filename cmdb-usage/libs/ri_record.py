#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-06-05 17:05
# @Author : jianxlin
# @Site : 
# @File : ri_record.py
# @Software: PyCharm
from datetime import datetime
from datetime import timedelta

import pandas as pd
from pandasql import sqldf

from libs.config import config

pd.options.display.float_format = '{:,.10f}'.format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

CACHE = {}


class RIRecord(object):
    def __init__(self):
        pass

    def __get_sheet_data(self, name=None, columns=None):
        """
            查询数据
        :param name:
        :param columns:
        :return:
        """
        aws_account_id = config.aws_account_id
        columns = ",".join(columns)
        record = pd.read_excel(config.ri_record_path, sheet_name=name)
        sql = """
            select %(columns)s
            from record
            where Account == '%(aws_account_id)s'
        """ % locals()
        return sqldf(sql, {"record": record})

    def __get_service_ri_purchase(self, name=None):
        """
            获取预留实例购买时间信息
        :param name:
        :return:
        """
        this_month = config.report_month

        next_month_num = (this_month.month + 1) % 12
        next_year_num = this_month.year + (this_month.month + 1) // 12

        next_month = this_month.replace(month=next_month_num, year=next_year_num)
        next_month = str(next_month)
        this_month = str(this_month)

        columns = ("InstanceId", "EffectiveDate", "PurchaseDate", "PrepaidPrice", "EbsPrepaidCost")

        record = self.__get_sheet_data(name=name, columns=columns)

        if not record.empty:
            record["PurchaseDate"] = record.apply(lambda c: c.PurchaseDate or c.EffectiveDate, axis=1)

        sql = """
            select InstanceId as ResourceId,sum(PrepaidPrice) as RiPurchaseDateCost,EbsPrepaidCost
            from record
            where '%(this_month)s' <= EffectiveDate
            and EffectiveDate < '%(next_month)s'
            group by InstanceId
        """ % locals()
        record = record.fillna(0)
        record = sqldf(sql, env={"record": record})
        if not record.empty:
            record["ResourceId"] = record.apply(lambda r: r.ResourceId.strip(), axis=1)
        return record

    def __get_service_ri_effective(self, name):
        """
            获取报告月份服务RI生效记录。
        :return:
        """
        this_month = config.report_month

        next_month_num = (this_month.month + 1) % 12
        next_year_num = this_month.year + (this_month.month + 1) // 12

        next_month = this_month.replace(month=next_month_num, year=next_year_num)
        next_month = str(next_month)
        this_month = str(this_month)

        columns = ("InstanceId", "EffectiveDate", "PrepaidPrice")

        record = self.__get_sheet_data(name=name, columns=columns)

        sql = """
            select InstanceId as ResourceId,sum(PrepaidPrice) as RiEffectiveDateCost
            from record
            where '%(this_month)s' <= EffectiveDate
            and EffectiveDate < '%(next_month)s'
            group by InstanceId
        """ % locals()
        record = record.fillna(0)
        record = sqldf(sql, env={"record": record})
        if not record.empty:
            record["ResourceId"] = record.apply(lambda r: r.ResourceId.strip(), axis=1)
        return record

    def __get_service_ri_record(self, name=None):
        """
            获取预留实例购买记录
        :param name:
        :return:
        """
        ret = {}
        month_start_date = datetime.strptime(config.get_config("report_month"), "%Y-%m")
        month_end_date = month_start_date + timedelta(days=31)
        month_end_date = month_end_date.replace(day=+ 1)
        record = self.__get_sheet_data(name=name, columns=("InstanceId",
                                                           "PurchaseDate",
                                                           "EffectiveDate",
                                                           "RunPrice",
                                                           "MatchStartDate",
                                                           "MatchEndDate",
                                                           "InstanceType",
                                                           "Operation"))

        for r in record.values:
            instance_id, ri_purchase_date, ri_effective_date, price, _matching_start_date, _matching_end_date, instance_type, operation = r
            if not instance_id:
                continue
            instance_id = instance_id.strip()
            ri_purchase_date = ri_purchase_date or ri_effective_date
            ri_start_date = datetime.strptime(ri_purchase_date, "%Y-%m-%d %H:%M:%S.%f")
            ri_start_date = ri_start_date - timedelta(hours=9)

            if _matching_start_date is None:
                matched_start_date = month_start_date
            else:
                matched_start_date = datetime.strptime(_matching_start_date, "%Y-%m-%d %H:%M:%S.%f")
                matched_start_date = matched_start_date - timedelta(hours=9)

            if _matching_end_date is None:
                matched_end_date = month_end_date
            else:
                matched_end_date = datetime.strptime(_matching_end_date, "%Y-%m-%d %H:%M:%S.%f")
                matched_end_date = matched_end_date - timedelta(hours=9)

            ri_end_date = ri_start_date.replace(year=ri_start_date.year + 1)

            matched_start_date = max([ri_start_date,
                                      month_start_date,
                                      matched_start_date])

            matched_end_date = min([ri_end_date,
                                    month_end_date,
                                    matched_end_date])

            if instance_id not in ret.keys():
                ret[instance_id] = []

            ret[instance_id].append(
                {
                    "price": price,
                    "matched_start_date": matched_start_date,
                    "matched_end_date": matched_end_date,
                    "instance_type": instance_type,
                    "operation": operation
                }
            )
        ri_bill = []

        for instance_id, matched_times in ret.items():
            for i in range(0, 24 * 33):
                ON_RI = False
                price = 0.0
                instance_type = None
                operation = None
                t = month_start_date + timedelta(hours=i)
                for mt in matched_times:
                    if mt["matched_start_date"] <= t <= mt["matched_end_date"]:
                        ON_RI = True
                        price = mt["price"]
                        instance_type = mt["instance_type"]
                        operation = mt["operation"]
                        break
                if ON_RI:
                    ri_bill.append(
                        (instance_id, t.strftime("%Y-%m-%d %H"), price, 0, instance_type, operation)
                    )
        return pd.DataFrame(ri_bill,
                            columns=["ResourceId", "UsageStartDate", "RiCost", "Rate", "InstanceType", "Operation"])

    def get_ri_time_percent(self, name=None):
        """
            查询主机按预留运行时长比例
        :return:
        """
        # m = ReportDate()
        # month_hours = (m.next_month - m.report_month).days * 24
        ri = self.__get_service_ri_record(name=name)
        sql = """
            select ResourceId,count(UsageStartDate) as RiHours
            from ri
            group  by ResourceId
            """
        ri_hours = sqldf(sql, {"ri": ri})
        ri_hours["RiRunningPercent"] = ri_hours["RiHours"].apply(lambda x: x / 24)
        return ri_hours[["ResourceId", "RiRunningPercent"]]

    def ec2_record(self):
        """
            获取ec2记录
        :return:
        """
        return self.__get_service_ri_record(name="EC2")

    def rds_record(self):
        """
            获取ec2记录
        :return:
        """
        return self.__get_service_ri_record(name="RDS")

    def elastic_cache_record(self):
        """
            获取ec2记录
        :return:
        """
        return self.__get_service_ri_record(name="ElastiCache")

    def get_ec2_ri_effective_info(self):
        """
            查询ec2实际生效日期信息。
        :return:
        """
        return self.__get_service_ri_effective(name="EC2")

    def get_rds_ri_effective_info(self):
        """
            查询rds实际生效日期信息。
        :return:
        """
        return self.__get_service_ri_effective(name="RDS")

    def get_elastic_cache_ri_effective_info(self):
        """
            查询ElastiCache实际生效日期信息。
        :return:
        """
        return self.__get_service_ri_effective(name="ElastiCache")

    def get_ec2_ri_purchase_info(self):
        """
            查询ec2购买日期信息。
        :return:
        """
        return self.__get_service_ri_purchase(name="EC2")

    def get_rds_ri_purchase_info(self):
        """
            查询rds购买日期信息。
        :return:
        """
        return self.__get_service_ri_purchase(name="RDS")

    def get_elastic_cache_ri_purchase_info(self):
        """
            查询rds购买日期信息。
        :return:
        """
        return self.__get_service_ri_purchase(name="ElastiCache")

    def get_ri_hours(self, name):
        sql = """
            select ResourceId,InstanceType as UsageType,Operation,count(UsageStartDate) as RiOnRecordHours
            from record
            group by ResourceId,InstanceType,Operation
        """
        return sqldf(sql, {"record": self.__get_service_ri_record(name)})

    # #
    # def get_total_cost(self, cost_name):
    #     """
    #         获取cost_name总和
    #     :param cost_name:
    #     :return:
    #     """
    #     r = self.get_ri_time_percent(name="EC2")
    #     logging.info("########")
    #     return r[["RiRunningPercent"]].apply(lambda c: c.sum(), axis=0)
    #


if __name__ == '__main__':
    pass
    # rpr = RIRecord()
    # r = rpr.get_ri_hours(name="EC2")
    # logging.info(r)
    # r = rpr.get_ec2_ri_purchase_info()
    # logging.info(r)
    # logging.info(r[(r.ResourceId == "i-0cfcf1f6c745d332e")])
    # logging.info(r[(r.ResourceId == "i-00c0ed3a9a7f487ee")])
    # logging.info(r[(r.ResourceId == "i-0142d5ecd56f515fd")])
    # logging.info(rpr.get_ec2_ri_purchase_info())
    # logging.info(rpr.get_ec2_ri_effective_info())
    # logging.info(rpr.ec2_record())
    # # logging.info(float(rpr.get_total_cost(cost_name="EC2")))
    # r = rpr.ec2_record()
    # sql = """
    #     select ResourceId,sum(RiCost)
    #     from b
    #     group  by ResourceId
    #     """
    # logging.info(sqldf(sql, {"b": r}))
