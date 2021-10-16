#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 15:16
# @Author : jianxlin
# @Site : 
# @File : base.py
# @Software: PyCharm

from pandasql import sqldf

from libs.tools import get_lower_case_name
from settings import const

from libs.db_context import get_db_engine
from libs.config import config
from libs.date.report_date import report_date


def get_report_db_date_copy(data):
    """
        将报告数据转换成数据库格式。
    :return:
    """
    data = data.copy()
    columns = data.columns
    new_col = {
        c: get_lower_case_name(c) for c in columns
    }
    data.rename(columns=new_col, inplace=True)
    return data


class ReportData(object):
    _BILL_DB_TABLE_NAME = 'aws_service_bill_report'
    _NAME = "Base"
    _STORAGE_COST_NAME = None

    def __init__(self, *args, **kwargs):
        self._dep_tag_name = "userproject"
        self._report_data = None

    @property
    def name(self):
        return self._NAME

    @property
    def dep_tag_name(self):
        return self._dep_tag_name

    @property
    def report_data(self):
        return self._report_data

    @report_data.setter
    def report_data(self, value):
        self._report_data = value

    def insert_to_db(self):
        """
            将报告写入数据库
        :return:
        """
        d = self.report_data[[
            "ResourceId",
            self.dep_tag_name,
            "TotalCost"
        ]]
        d['bill_date'] = report_date.report_date_as_str
        d['service_name'] = self._NAME
        d = get_report_db_date_copy(d)

        engine = get_db_engine(db_key=const.DEFAULT_DB_KEY)
        clean_sql = """
            delete from %s
            where bill_date = '%s'
            and service_name = '%s'
        """ % (self._BILL_DB_TABLE_NAME, report_date.report_date_as_str, self._NAME)

        engine.execute(clean_sql)
        d.to_sql(self._BILL_DB_TABLE_NAME, engine, index=False, if_exists='append')

    def merge_bill_data(self, data, on=None):
        """
            合并账单到报告。
        :param on:
        :param data:
        :return:
        """
        if on is None:
            on = ["ResourceId"]
        self._report_data = self.report_data.merge(data, how="left", on=on)

    def get_dep_cost(self, cost_names=None):
        """
            获取部门cost_name的汇总账单信息。
        :return:
        """
        dep_tag_name = self.dep_tag_name
        assert isinstance(cost_names, (tuple, list))
        cost_names = ",".join(["sum(%s) as %s" % (n, n) for n in cost_names])
        sql = """
            select %(dep_tag_name)s,%(cost_names)s
            from bill
            group  by %(dep_tag_name)s
        """ % locals()
        return sqldf(sql, env={"bill": self.report_data})

    def get_dep_service_pay_bill(self):
        """
            获取服务支付账单信息
        :return:
        """
        cost_names = ["OnDemandCost", "OnDemandTheoreticCost", "RiEffectiveDateCost", "RiPurchaseDateCost",
                      "EbsPrepaidCost", "DeductibleStorageCost"]
        bill = self.get_dep_cost(cost_names=cost_names)
        return bill

    # def merge_storage_deductible_cost(self):
    #     """
    #         增加存储减免费用信息。
    #     :return:
    #     """
    #
    #     self.merge_bill_data(self._ri_record.get_ri_time_percent(name=self._NAME))
    #
    #     _ = self.report_data
    #     self._report_data["DeductibleStorageCost"] = _["EbsCost"] * _["RiRunningPercent"]

    def get_total_cost(self, cost_name):
        """
            获取cost_name总和
        :param cost_name:
        :return:
        """
        return float(self.report_data[[cost_name]].sum())
