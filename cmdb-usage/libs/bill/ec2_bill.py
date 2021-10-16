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
from libs.bill.base import Bill
from libs.decorate import cache, show_running_time
from libs.tools import get_usage_type_from_item_description, is_heavy_usage_type, is_heavy_usage_item_scription
from libs.tools import instance_type_format
from libs.aws.ec2 import EC2

pd.options.display.float_format = '{:,.10f}'.format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class Ec2Bill(Bill):
    _service_type = "ec2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aws_volumes = None
        self._aws_snapshots = None
        self.__init_ec2_bill()
        self.__init_aws_service_info()

    def __init_aws_service_info(self):
        """
            初始化aws服务信息。
        :return:
        """
        e = EC2()
        self._aws_volumes = pd.DataFrame(e.get_volumes_list(), columns=("VolumeId", "InstanceId"))
        self._aws_snapshots = pd.DataFrame(e.get_snapshots_list(), columns=("SnapshotId", "InstanceId"))

    def __init_ec2_bill(self):
        """
            出事化EC2费用信息
        :return:
        """
        columns = ",".join(self._user_bill_columns)
        sql = """
            select %(columns)s,Cost
            from bill 
            where ProductName = 'Amazon Elastic Compute Cloud'
            """ % locals()
        self.bill = sqldf(sql, {"bill": self.bill})

        self.format_usage_quantity()

    @cache
    def get_ec2_instance_id_mapping(self):
        """
            查询ec2 Name 与 ID对应关系。
        :return:
        """

        columns = ",".join(["ResourceId", self.dep_tag_name])
        sql = """
            select %(columns)s
            from bill 
            where ResourceID like 'i-%%'
            group by ResourceId
            """ % locals()
        ret = sqldf(sql, {"bill": self.bill})
        return self.format_dep_name(ret, resource_type="ec2")

    def format_usage_quantity(self):
        """
            格式化UsageType 及 UsageQuantity。
        :return:
        """

        def sum_usage_quantity(bill_line):
            if not is_heavy_usage_type(bill_line.UsageType):
                return bill_line.UsageQuantity

            if not is_heavy_usage_item_scription(bill_line.ItemDescription):
                return bill_line.UsageQuantity
            times = float(instance_type_format(bill_line.UsageType)) / float(instance_type_format(
                usage_type=get_usage_type_from_item_description(
                    bill_line.ItemDescription)))
            return float(bill_line.UsageQuantity) * times

        def get_usage_type(bill_line):
            if not is_heavy_usage_item_scription(bill_line.ItemDescription):
                return bill_line.UsageType
            return get_usage_type_from_item_description(bill_line.ItemDescription)

        self._bill["UsageQuantity"] = self._bill.apply(lambda b: sum_usage_quantity(b), axis=1)
        self._bill["UsageType"] = self._bill.apply(lambda b: get_usage_type(b), axis=1)

    @cache
    def get_running_time(self):
        """
            获取ec2主机运行时长。
        :return:
        """
        columns = ",".join(["ResourceId"])
        sql = """
            select %(columns)s,sum(UsageQuantity) as RunTime
            from bill 
            where (
                UsageType like '%%BoxUsage%%' 
                or UsageType like '%%HeavyUsage%%'
                )
                and ResourceId like 'i-%%'

            group by %(columns)s
            """ % locals()
        _t = sqldf(sql, {"bill": self.bill})
        _t["temp"] = 1
        _t["Time%"] = _t.groupby("temp")["RunTime"].transform(lambda x: x / x.sum())
        _t = _t.drop(columns=["temp"])
        return _t

    @cache
    def get_service_running_bill_info(self):
        """
            获取ec2主机运行数据。
        :return:
        """
        columns = ",".join(["ResourceId", "UsageType", "UsageStartDate", "Operation"])
        sql = """
            select %(columns)s,sum(Cost) as RunCost,sum(UsageQuantity) as UsageQuantity
            from bill 
            where (
                UsageType like '%%BoxUsage%%' 
                or UsageType like '%%HeavyUsage%%'
                )
                and ResourceId like 'i-%%'

            group by ResourceId,UsageStartDate
            """ % locals()
        bill = sqldf(sql, {"bill": self.bill})
        return bill

    @cache
    def get_service_matched_reserved_info(self):
        """
            获取ec2主机预留实例匹配数据。
        :return:
        """
        columns = ",".join(["ResourceId", "UsageType", "UsageStartDate", "Operation"])
        sql = """
            select %(columns)s,sum(UsageQuantity) as UsageQuantity
            from bill 
            where (
                
                UsageType like '%%BoxUsage%%' 
                or UsageType like '%%HeavyUsage%%'
                )
                and ResourceId like 'i-%%'
                and ReservedInstance= 'Y'

            group by ResourceId,UsageStartDate
            """ % locals()
        bill = sqldf(sql, {"bill": self.bill})
        bill["UsageStartDate"] = bill.apply(lambda b: b.UsageStartDate.split(":")[0], axis=1)
        return bill

    @cache
    def get_summary_bill(self):
        """
            获取EC2按类型汇总后费用信息.
        :return:
        """
        columns = ",".join(self._bill_columns)
        dep_tag_name = self.dep_tag_name
        sql = """
            select %(columns)s,%(dep_tag_name)s,sum(Cost) as Cost
            from bill 
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.bill})

    @cache
    def get_ec2_all_bill(self):
        """
            获取ec2主机资源账单数据：ResourceId = i-*
        :return:
        """
        columns = ",".join(["ProductName", "ResourceId", "Operation", "UsageType", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as Cost
            from bill 
            where ResourceId like 'i-%%'
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.get_summary_bill()})

    @cache
    def get_ec2_running_bill(self):
        """
            获取ec2主机运行账单数据。
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as RunningCost
            from bill 
            where (
                UsageType like '%%Usage%%' 
                )
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.get_ec2_all_bill()})

    @cache
    def get_ec2_transfer_bill(self):
        """
            获取ec2主机数据传输账单数据。
        :return:
        """
        columns = ",".join(["ResourceId", ])
        sql = """
            select %(columns)s,sum(Cost) as TransferCost
            from bill 
            where UsageType like '%%-DataTransfer-%%' 
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.get_ec2_all_bill()})

    @cache
    def get_ec2_other_bill(self):
        """
            获取ec2主机除运行、流量账单以外的其他账单数据。
        :return:
        """
        columns = ",".join(["ProductName"])
        sql = """
            select 'Ec2OtherResource',sum(Cost) as Ec2OtherCost
            from bill 
            where UsageType not like '%%-DataTransfer-%%' 
            and UsageType not like '%%BoxUsage%%' 
            and UsageType not  like '%%HeavyUsage%%'
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.get_ec2_all_bill()})

    @cache
    def get_ebs_all_bill(self):
        """
            获取主机磁盘费用。
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as EbsCost
            from bill 
            where ResourceId like 'vol-%%'
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.get_summary_bill()})

    @cache
    def merge_instance_id_to_ebs_bill(self):
        """
            添加主机id到ebs账单。
        :return:
        """
        dep_tag_name = self.dep_tag_name
        sql = """
            select av.InstanceId , b.ResourceId as ResourceId,%(dep_tag_name)s,sum(b.EbsCost) as EbsCost
            from bill as b left join aws_volumes as av on av.VolumeId = b.ResourceId
            group by av.InstanceId
            """ % locals()
        ebs_bill = sqldf(sql, {"bill": self.get_ebs_all_bill(), "aws_volumes": self._aws_volumes})
        ebs_bill.fillna("NULL", inplace=True)
        return self.format_dep_name(ebs_bill, "ebs")

    @cache
    def get_ec2_ebs_bill(self):
        """
            获取有主机Name到磁盘费用。
        :return:
        """
        sql = """
            select InstanceId as ResourceId,sum(EbsCost) as EbsCost
            from bill 
            where  InstanceId  in (
                select ResourceId 
                from ec2s
            )
            group by ResourceId
            """ % locals()
        return sqldf(sql, {"bill": self.merge_instance_id_to_ebs_bill(), "ec2s": self.get_ec2_instance_id_mapping()})

    @cache
    def get_no_ec2_ebs_bill(self):
        """
            获取非主机磁盘费用。
        :return:
        """
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,InstanceId,%(dep_tag_name)s, EbsCost
            from bill 
            where InstanceId not in (
                select ResourceId 
                from ec2s)
            """ % locals()
        return sqldf(sql,
                     {"bill": self.merge_instance_id_to_ebs_bill(), "ec2s": self.get_ec2_instance_id_mapping()})

    # @cache
    # def get_dep_ebs_bill(self):
    #     """
    #         查询dep的ebs账单。
    #     :return:
    #     """
    #     dep_tag_name = self.dep_tag_name
    #     sql = """
    #         select ResourceId,%(dep_tag_name)s, sum(EbsCost) as EbsCost
    #         from bill
    #         where %(dep_tag_name)s != 'NULL'
    #         group by %(dep_tag_name)s
    #     """ % locals()
    #     ebs_bill = sqldf(sql, {"bill": self.get_no_ec2_ebs_bill()})
    #
    #     if not ebs_bill.empty:
    #         conf_mapping = self.config.get_config("resource_dep_mapping.ebs")
    #         ebs_bill[self.dep_tag_name] = ebs_bill.iloc[:, :] \
    #             .apply(lambda x: x[self.dep_tag_name]
    #         if x[self.dep_tag_name] != 'NULL'
    #         else conf_mapping.get(x["ResourceId"], "NULL"), axis=1)
    #     return ebs_bill
    #
    # @cache
    # def get_no_tag_ebs_bill(self):
    #     """
    #         查询无任何标签到ebs账单。
    #     :return:
    #     """
    #     dep_tag_name = self.dep_tag_name
    #     sql = """
    #         select sum(EbsCost) as EbsCost
    #         from bill
    #         where %(dep_tag_name)s == 'NULL'
    #     """ % locals()
    #
    #     bill = sqldf(sql, {"bill": self.get_no_ec2_ebs_bill()})
    #     bill.fillna(0.0, inplace=True)
    #     bill.insert(0, "Name", "UnknownEbsCost")
    #     return bill

    @cache
    def get_snap_all_bill(self):
        """
            获取主机磁盘快照费用。
        :return:
        """
        columns = ",".join(["ResourceId", self.dep_tag_name])
        sql = """
            select %(columns)s,sum(Cost) as SnapCost
            from bill 
            where ResourceId like '%%/snap-%%'
            group by %(columns)s
            """ % locals()
        ret = sqldf(sql, {"bill": self.get_summary_bill()})
        ret["ResourceId"] = ret["ResourceId"].map(lambda x: x.split("/")[-1])
        return ret

    @cache
    def merge_instance_id_to_snap_bill(self):
        """
            添加主机id到snap账单。
        :return:
        """
        dep_tag_name = self.dep_tag_name
        sql = """
            select ass.InstanceId, b.ResourceId as ResourceId,%(dep_tag_name)s,sum(b.SnapCost) as SnapCost
            from bill as b left join aws_snapshot as ass on ass.SnapshotId = b.ResourceId
            group by ass.InstanceId,ResourceId
            """ % locals()
        snapshot_bill = sqldf(sql, {"bill": self.get_snap_all_bill(), "aws_snapshot": self._aws_snapshots})
        snapshot_bill.fillna("UnKnown", inplace=True)
        return snapshot_bill

    @cache
    def get_ec2_snap_bill(self):
        """
            获取有主机Name到磁盘快照费用。
        :return:
        """
        sql = """
            select InstanceId as ResourceId,sum(SnapCost) as SnapCost
            from bill 
            where InstanceId  in (
                select ResourceId 
                from ec2s
            )
            group by InstanceId
            """
        snap_bill = sqldf(sql,
                          {"bill": self.merge_instance_id_to_snap_bill(), "ec2s": self.get_ec2_instance_id_mapping()})
        return snap_bill

    @cache
    def get_no_ec2_snap_bill(self):
        """
            获取非主机磁盘快照费用。
        :return:
        """
        dep_tag_name = self.dep_tag_name
        sql = """
            select ResourceId,%(dep_tag_name)s, sum(SnapCost) as SnapCost
            from bill 
            where InstanceId not in (
                select ResourceId 
                from ec2s
            )
            group by ResourceId
            """ % locals()
        snap_bill = sqldf(sql,
                          {"bill": self.merge_instance_id_to_snap_bill(), "ec2s": self.get_ec2_instance_id_mapping()})
        return self.format_dep_name(snap_bill, "snap")

    @cache
    def get_other_bill(self):
        """
            获取其他账单数据。
        :return:
        """
        columns = ",".join(["ProductName", ])
        sql = """
            select 'Ec2Other',sum(Cost) as Ec2OtherCost
            from bill 
            where ResourceId not like 'i-%%'
            and ResourceId not like 'vol-%%'
            and ResourceId not like '%%/snap-%%'
            and ResourceId not like '%%:reserved-instances/%%'
            group by %(columns)s
            """ % locals()
        return sqldf(sql, {"bill": self.get_summary_bill()})

    @show_running_time
    def _init_on_demand_price(self):
        from libs.aws.price import Ec2OnDemandPrice
        ep = Ec2OnDemandPrice()
        self._on_demand_price = ep.on_demand_price


# main


if __name__ == '__main__':
    b = Ec2Bill()
    # logging.info(b.get_instance_run_info())
    # bb = b.bill["ResourceId"]
    # bb = bb.drop_duplicates()
    # logging.info(bb)
    # bb = b.bill
    # logging.info(bb[(bb.ResourceId == 'i-073e498103d0b82b5')])
    from libs.ri_record import RIRecord

    #
    rr = RIRecord()
    logging.info(b.get_instance_run_info())

    # logging.info(b.get_ec2_ebs_bill())
    # logging.info(b.get_no_ec2_ebs_bill())

    # ri_bill = rr.ec2_record()
    # logging.info(b.merge_instance_id_to_ebs_bill())
    # logging.info(b.get_ec2_ebs_bill())
    # logging.info(b.get_no_ec2_ebs_bill())

    # logging.info(b.get_summary_bill())
    # logging.info(b.get_ec2_all_bill())
    # logging.info(b.get_ebs_all_bill())
    # logging.info(b.get_snap_all_bill())
    # logging.info(b.get_other_bill())
    #
    #
    # logging.info(b.get_ec2_all_bill())
    # logging.info(b.get_ec2_transfer_bill())
    # logging.info(b.get_ec2_other_bill())
    # logging.info(b.get_summary_bill())

    # logging.info(b.get_dep_ebs_bill())
    #
    # logging.info(b.get_ec2_running_bill())
    # logging.info(b.get_service_running_bill_info())
    # logging.info(b.merge_instance_id_to_snap_bill())
    # logging.info(b.get_ec2_snap_bill())
    # logging.info(b.get_no_ec2_snap_bill())
