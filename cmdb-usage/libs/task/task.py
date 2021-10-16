#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-06-17 11:09
# @Author : jianxlin
# @Site : 
# @File : task.py
# @Software: PyCharm
from biz.ds.ds_update_ri_usage import update_ri_usage_by_day
from biz.ds.ds_update_usage_by_day import sync_host_usage_from_zabbix_by_day
from libs.config import config
from libs.date.report_date import report_date
from libs.common import catch_exception

TASKS = {}


def implements(name):
    def wrapper(cls):
        TASKS[name] = cls
        return cls

    return wrapper


class Task(object):
    def __init__(self, date=None, *args, **kwargs):
        self._date = date

    def run_task(self, *args, **kwargs):
        pass

@implements("add_ri_usage")
class AddRiUsagetTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @catch_exception
    def run_task(self, date=None, *args, **kwargs):
        update_ri_usage_by_day()
        return True

@implements("add_usage")
class AddUsageTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @catch_exception
    def run_task(self, date=None, *args, **kwargs):
        sync_host_usage_from_zabbix_by_day(date)
        return True

@implements("billing")
class AwsBillingTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @catch_exception
    def run_task(self, date=None, *args, **kwargs):
        from libs.main import NewReport
        report_date.set_date(date=date)
        new_report = NewReport()
        new_report.create_report()
        return True


def run_task(name, *args, **kwargs):
    tk = TASKS.get(name, Task)()
    return tk.run_task(*args, **kwargs)
