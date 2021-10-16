#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-07-22 16:46
# @Author : jianxlin
# @Site : 
# @File : ri_record_compare.py
# @Software: PyCharm
import logging

from libs.bill.ec2_bill import Ec2Bill
from libs.bill.rds_bill import RDSBill
# from libs.excel.reports import Report
from libs.ri_record import RIRecord
from libs.aws.price import Ec2OnDemandPrice
from libs.tools import instance_type_format, get_instance_series, get_instance_type_from_usage_type, get_operation_name

# reports = Report("~/Desktop/show.xlsx")


def compare_ri_record():
    """
        对比RI记录
    :return:
    """
    ep = Ec2OnDemandPrice()
    eb = Ec2Bill()
    rr = RIRecord()
    ec2_bill_ri_info = eb.get_ec2_ri_value()
    ri_record_info = rr.get_ri_hours(name="EC2")

    ri_record_info["UsageType"] = ri_record_info["UsageType"].apply(lambda o: ":".join(["CNN1-BoxUsage", o]))

    ec2_bill_ri_info = ec2_bill_ri_info.merge(ri_record_info, how="left", on=("ResourceId", "UsageType", "Operation"))

    ec2_bill_ri_info = ec2_bill_ri_info.merge(ep.on_demand_price, how="left",
                                              on=("UsageType", "Operation"))

    ec2_bill_ri_info = ec2_bill_ri_info.fillna(0)
    ec2_bill_ri_info["Compare"] = ec2_bill_ri_info.apply(lambda e: e.RunHours - e.RiOnRecordHours, axis=1)
    ec2_bill_ri_info["UnMatchedRiCost"] = ec2_bill_ri_info.apply(lambda e: e.Compare * e.OnDemandPrice, axis=1)

    ec2_bill_ri_info = ec2_bill_ri_info[
        ["ResourceId", "UsageType", "Operation", "RunHours", "RiOnRecordHours", "Compare",
         "UnMatchedRiCost"]]

    logging.info(ec2_bill_ri_info[(ec2_bill_ri_info.UnMatchedRiCost != 0)])
    logging.info("UnMatchedRiCost:不明RI匹配费用！！")


def get_bill_reserved_info_by_date(bill):
    """
        按日期统计预留实例
    :param bill:
    :return:
    """
    bill["Series"] = bill["InstanceType"].apply(lambda c: get_instance_series(usage_type=c))
    bill["UsageQuantity"] = bill.apply(lambda b: b.UsageQuantity * instance_type_format(instance_type=b.InstanceType),
                                       axis=1)
    bill = bill.groupby(["UsageStartDate", "Operation", "Series"])["UsageQuantity"].sum()
    return bill.reset_index()


def get_diff_between_conf_and_bill(operation=None, series=None):
    eb = Ec2Bill()
    rr = RIRecord()

    ec2_reserved_info = eb.get_service_matched_reserved_info()
    ec2_ri_table_info = rr.ec2_record()

    ret = ec2_ri_table_info[["UsageStartDate"]].drop_duplicates()

    ec2_reserved_info["InstanceType"] = ec2_reserved_info.apply(
        lambda e: get_instance_type_from_usage_type(e.UsageType), axis=1)
    ec2_ri_table_info["UsageQuantity"] = (ec2_ri_table_info.Rate + 1) % 2

    ec2_ri_table_info = get_bill_reserved_info_by_date(ec2_ri_table_info)
    ec2_reserved_info = get_bill_reserved_info_by_date(ec2_reserved_info)

    for rti in ec2_ri_table_info.groupby(["Operation", "Series"]):
        rti_series_index = rti[0]
        rti_operation_name = get_operation_name(rti_series_index[0])
        rti_series_name = rti_series_index[1]
        rti_series_data = rti[1]

        if operation is not None and operation != rti_operation_name:
            continue
        if series is not None and series != rti_series_name:
            continue

        diff_name = ":".join(["Diff", rti_operation_name, rti_series_name])

        rti_name = ":".join(["Config", rti_operation_name, rti_series_name])

        rti_series_data.rename(columns={"UsageQuantity": rti_name}, inplace=True)

        ret = ret.merge(rti_series_data[["UsageStartDate", rti_name]], how="left", on="UsageStartDate")

        for eri in ec2_reserved_info.groupby(["Operation", "Series"]):

            eri_series_index = eri[0]
            eri_operation_name = get_operation_name(eri_series_index[0])
            eri_series_name = eri_series_index[1]
            eri_series_data = eri[1]

            if rti_operation_name != eri_operation_name or rti_series_name != eri_series_name:
                continue

            eri_name = ":".join(["Bill", eri_operation_name, eri_series_name])
            eri_series_data.rename(columns={"UsageQuantity": eri_name}, inplace=True)

            ret = ret.merge(eri_series_data[["UsageStartDate", eri_name]], how="left", on="UsageStartDate")

            ret[diff_name] = ret.apply(lambda r: r[rti_name] - r[eri_name], axis=1)
    return ret


def show_reserved_info(_=None, operation=None, series=None, date=None):
    diff = get_diff_between_conf_and_bill(operation=operation, series=series)

    if date:
        diff["date"] = diff["UsageStartDate"].apply(lambda u: u.split(" ")[0])
        diff = diff[(diff.date == date)]
        diff = diff.drop(['date'], axis=1)
    else:
        diff["UsageStartDate"] = diff["UsageStartDate"].apply(lambda u: u.split(" ")[0])
        diff = diff.groupby(["UsageStartDate"]).sum()
    diff.fillna(0, inplace=True)
    logging.info(diff)


def show_operation():
    rb = RDSBill()
    ret = rb.get_ec2_ri_value()
    logging.info(ret)
    rb = Ec2Bill()
    ret = rb.get_ec2_ri_value()
    logging.info(ret)


def show_instance_daily_bill():
    eb = Ec2Bill()
    rr = RIRecord()
    run_info = eb.get_instance_run_info(rr.ec2_record())
    ret = run_info[["UsageStartDate"]].drop_duplicates()

    for instance_bill in run_info.groupby(["ResourceId", "InstanceType"]):
        if instance_bill[0][0] != "i-03689494f5cee98bc":
            continue
        name = "_".join(instance_bill[0])
        data = instance_bill[1]
        data[name] = data.apply(lambda d: d.OnDemandPrice * d.UsageQuantity, axis=1)
        ret = ret.merge(data[["UsageStartDate", name]], how="left", on="UsageStartDate")
    return ret


if __name__ == '__main__':
    # show_reserved_info(operation="Linux", series="m4", date="2019-05-06")
    logging.info(show_instance_daily_bill())
    # reports.append_sheet(show_instance_daily_bill(), "B")
    # reports.save()
