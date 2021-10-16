#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:23
# @Author : jianxlin
# @Site : 
# @File : config.py
# @Software: PyCharm

import os
from datetime import datetime
from libs.date.report_date import report_date
import yaml

Conf = None


class Config(object):
    def __init__(self):
        self._conf = None
        # self.__read_conf()

    def __read_conf(self):
        """
            读取配置
        :return:
        """
        _ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        config_file = "/".join([_ROOT, "conf", "config.yaml"])
        with open(config_file, 'r') as c:
            self._conf = yaml.load(c, Loader=yaml.FullLoader)
        self._conf["report_month"] = report_date.report_month_as_str
        print(report_date.report_month_as_str)
        self._conf["_ROOT"] = _ROOT
        self._conf["_TMP"] = "/".join([_ROOT, "tmp"])
        self._conf["_LOG"] = "/".join([_ROOT, "log"])
        self._conf["_REPORT"] = "/".join([_ROOT, "reports"])

    @property
    def department_tag_name(self):
        return self.get_config("tag.dep_tag_name")

    @property
    def aws_account_id(self):
        return self.get_config("aws_account_id")

    @property
    def region(self):
        return self.get_config("aws_key.region_name")

    @property
    def aws_s3_bucket_name(self):
        """
            获取s3桶名
        :return:
        """
        name = self.get_config("aws_bucket_name")
        return name % self._conf

    @property
    def report_name(self):
        """
            获取报告文件名称。
        :return:
        """
        name = self.get_config("file_name.reports")
        return name % self._conf

    @property
    def report_path(self):
        """
            获取报告文件路径。
        :return:
        """
        return "/".join([self.get_config("_REPORT"), self.report_name])

    @property
    def cloud_bill_record(self):
        """
            获取云账单记录文件名
        :return:
        """
        name = self.get_config("file_name.cloud_bill_record")
        # name = "%(aws_account_id)s-aws-billing-detailed-line-items-with-resources-and-tags-ACTS-Ningxia-%(report_month)s.csv.zip"
        return name % self._conf

    @property
    def cloud_bill_record_path(self):
        """
            获取云账单记录文件路径。
        :return:
        """

        return "/".join([self.get_config("_TMP"), self.cloud_bill_record])

    @property
    def ri_record_path(self):
        """
            获取预留实例记录文件路径。
        :return:
        """
        name = self.get_config("file_name.ri_record")
        name = name % self._conf
        return "/".join([self.get_config("_TMP"), name])

    @property
    def additional_cost_path(self):
        """
            获取附加费用文件路径。
        :return:
        """
        name = self.get_config("file_name.additional_cost")
        name = name % self._conf
        return "/".join([self.get_config("_TMP"), name])

    @property
    def nbu_size_report_path(self):
        """
            获取NBU备份数据报告文件路径。
        :return:
        """
        name = self.get_config("file_name.nbu_size_report")
        name = name % self._conf
        return "/".join([self.get_config("_TMP"), name])

    @property
    def report_month(self):
        """
            获取报告时间。
        :return:
        """
        d = self.get_config("report_month")
        return datetime.strptime(d, "%Y-%m")

    @property
    def debug_mode(self):
        """
            debug开关状态。
        :return:
        """
        return self.get_config("Debug")

    @property
    def cache_expire_days(self):
        return self._conf.get("cache_expire_days")

    def get_disk_threshold(self, size=None):
        """
            根据size获取阈值。
        :param size:
        :return:
        """
        threshold = self.get_config("free_resource.disk").copy()
        ret = threshold["default"]
        if size is None:
            return ret

        del threshold["default"]
        for s in sorted(int(n) for n in threshold.keys()):
            if size > int(s):
                ret = threshold[str(s)]
            else:
                break
        return ret

    def get_config(self, name=None):
        """
            读取配置。
        :param name:
        :return:
        """
        if self._conf is None:
            self.__read_conf()
        conf = self._conf
        if not name:
            return conf

        name = name.split(".")
        for n in name:
            conf = conf[n]
        return conf

    def get_aws_conf(self):
        return self.get_config(name="aws_key")

    def get_on_demand_price(self, service):
        return self.get_config("aws_on_demand_price")[service]


config = Config()

if __name__ == '__main__':
    c = Config()
