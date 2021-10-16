#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-15 10:06
# @Author : jianxlin
# @Site : 
# @File : decorate.py
# @Software: PyCharm
import logging

from datetime import datetime

from libs.config import config


def cache(func):
    def _cache(self, *args, **kwargs):
        _name = func.__name__
        if _name in self._bill_cache.keys():
            return self._bill_cache[_name]
        ret = func(self, *args, **kwargs)
        self._bill_cache[_name] = ret

        if config.debug_mode:
            logging.info("##################")
            logging.info(_name)
            logging.info(len(ret))
            logging.info(ret.iloc[:, -1].sum())
            logging.info("")

        return ret

    return _cache


def show_running_time(func):
    def _show(*args, **kwargs):
        _name = func.__name__

        start_time = datetime.now()
        logging.info("##### Run function: %s" % _name)
        logging.info("StartTime: %s" % start_time)

        ret = func(*args, **kwargs)

        end_time = datetime.now()
        logging.info("EndTime: %s" % end_time)
        logging.info("TotalTime: %s" % str(end_time - start_time))
        return ret

    return _show
