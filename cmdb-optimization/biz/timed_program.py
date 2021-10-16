#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : timed_program.py
# @Author: Fred Yangxiaofei
# @Date  : 2019/9/12
# @Role  : 需要定时执行的程序

import time
from datetime import datetime
from biz.ds.ds_ebs import main as ebs_sync
from biz.ds.ds_elb import main as elb_sync
from biz.ds.ds_rds import main as rds_sync
from biz.ds.ds_nat import main as nat_sync
from biz.ds.ds_eip import main as eip_sync

def tail_data():
    server_start_time = datetime.strptime(str(datetime.now().date()) + '00:30', '%Y-%m-%d%H:%M')
    server_end_time = datetime.strptime(str(datetime.now().date()) + '01:30', '%Y-%m-%d%H:%M')

    erver_start_time_1 = datetime.strptime(str(datetime.now().date()) + '01:30', '%Y-%m-%d%H:%M')
    server_end_time_1 = datetime.strptime(str(datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')

    erver_start_time_2 = datetime.strptime(str(datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')
    server_end_time_2 = datetime.strptime(str(datetime.now().date()) + '07:30', '%Y-%m-%d%H:%M')

    now_time = datetime.now()
    if server_start_time < now_time <= server_end_time:
        time.sleep(10)
        ebs_sync()
        time.sleep(10)
        elb_sync()
        time.sleep(10)
        rds_sync()
        time.sleep(10)
        nat_sync()
        time.sleep(10)
        eip_sync()

    elif erver_start_time_1 < now_time <= server_end_time_1:
      pass
    elif erver_start_time_2 < now_time <= server_end_time_2:
       pass
    else:
      pass


if __name__ == '__main__':
    tail_data()
