#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-06-26 11:31
# @Author : jianxlin
# @Site : 
# @File : report_date.py
# @Software: PyCharm
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class ReportDate(object):
    def __init__(self):
        self._date = None
        self._usage_start_date = None
        self._usage_end_date = None
        self._report_month = None

    @property
    def date(self):
        return self._date

    @property
    def report_month(self):
        return self._report_month

    @property
    def report_month_as_str(self):
        return self._report_month.strftime("%Y-%m")

    @property
    def report_full_month_as_str(self):
        return self._report_month.strftime("%Y-%m-01 00:00:00")

    @property
    def report_last_month(self):
        return self._report_month + relativedelta(months=1)

    @property
    def report_last_month_as_full_str(self):
        month = self._report_month + relativedelta(months=1)
        return month.strftime("%Y-%m-01 00:00:00")

    @property
    def report_date_as_str(self):
        return self.usage_start_date.strftime("%Y-%m-%d 00:00:00")

    @property
    def usage_start_date(self):
        return self._usage_start_date

    @property
    def usage_end_date(self):
        return self._usage_end_date

    @property
    def usage_start_date_as_str(self):
        return self._usage_start_date.strftime("%Y-%m-%d 00:00:00")

    @property
    def usage_end_date_as_str(self):
        return self._usage_end_date.strftime("%Y-%m-%d 00:00:00")

    def set_date(self, date):
        self._usage_start_date = date or datetime.now() - timedelta(days=6)
        self._usage_start_date = datetime.strptime(self._usage_start_date.strftime("%Y-%m-%d"), '%Y-%m-%d')
        self._usage_end_date = self._usage_start_date + timedelta(days=1)
        self._report_month = datetime.strptime(self._usage_start_date.strftime("%Y-%m"), '%Y-%m')


report_date = ReportDate()
