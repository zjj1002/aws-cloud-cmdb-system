#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/26 14:30

# @File    : auto_update_app.py
# @Role    : 一些定时执行的程序


import tornado
from websdk.application import Application as myApplication
from biz.timed_program import run_task_programs as task_program
from biz.timed_program import tail_data as my_timed_program


class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        crond_program_callback = tornado.ioloop.PeriodicCallback(task_program, 10000)  # 1分钟
        my_program_callback = tornado.ioloop.PeriodicCallback(my_timed_program, 3600000)  # 1小时
        my_program_callback.start()
        crond_program_callback.start()
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
