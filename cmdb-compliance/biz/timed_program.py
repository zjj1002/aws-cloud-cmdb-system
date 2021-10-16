#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : timed_program.py
# @Author: Fred Yangxiaofei
# @Date  : 2019/9/12
# @Role  : 需要定时执行的程序

import time
from datetime import datetime

from biz.ds.ds_asg import asg_sync_cmdb
from biz.ds.ds_com_ec2 import com_ec2_sync_cmdb
from biz.ds.ds_eip import eip_sync_cmdb
from biz.ds.ds_iam_permission_data import iam_permission_sync_cmdb
from biz.ds.ds_sgs import sgs_sync_cmdb
from clair.main import scan_images_by_day
from pocsuite.main import run_scan_task, dayly_san_taks
from websdk.web_logs import ins_log
from biz.ds.ds_uncom_ec2 import uncom_ec2_sync_cmdb
from biz.ds.ds_uncom_vpc import uncom_vpc_sync_cmdb
from biz.ds.ds_uncom_vpc_peering import uncom_vpc_peering_sync_cmdb
from biz.ds.ds_vpc import vpc_sync_cmdb
from biz.ds.ds_vpc_endpoint import vpc_endpoint_sync_cmdb
from biz.ds.ds_vpc_peering import vpc_peering_sync_cmdb
from biz.ds.ds_ebs import main as ebs_sync
from biz.ds.ds_iam import main as iam_sync
from biz.ds.ds_elb import main as elb_sync
from biz.ds.ds_rds import main as rds_sync
from biz.ds.ds_nat import main as nat_sync
from biz.ds.ds_target import main as ds_target_sync
from prowler.ds_gdpr import gdpr_sync_cmdb
from prowler.ds_hipaa import hipaa_sync_cmdb
from prowler.ds_prowler import prowler_sync_cmdb
from prowler.get_gdpr_data import run_get_gdpr_data
from prowler.get_hipaa_data import run_get_hipaa_data
from prowler.get_prowler_data import run_get_prowler_data


def tail_data():
    server_start_time = datetime.strptime(str(datetime.now().date()) + '00:30', '%Y-%m-%d%H:%M')
    server_end_time = datetime.strptime(str(datetime.now().date()) + '01:30', '%Y-%m-%d%H:%M')

    erver_start_time_1 = datetime.strptime(str(datetime.now().date()) + '01:30', '%Y-%m-%d%H:%M')
    server_end_time_1 = datetime.strptime(str(datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')

    erver_start_time_2 = datetime.strptime(str(datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')
    server_end_time_2 = datetime.strptime(str(datetime.now().date()) + '07:30', '%Y-%m-%d%H:%M')

    now_time = datetime.now()
    if server_start_time < now_time <= server_end_time:
        scan_images_by_day()
        ins_log.read_log('info', 'docker镜像扫描执行完成')
        time.sleep(10)
        run_scan_task()
        time.sleep(10)
        ds_target_sync()
        time.sleep(10)
        ebs_sync()
        time.sleep(10)
        iam_sync()
        time.sleep(10)
        elb_sync()
        time.sleep(10)
        rds_sync()
        time.sleep(10)
        nat_sync()
        time.sleep(10)
        dayly_san_taks()


    elif erver_start_time_1 < now_time <= server_end_time_1:
        run_get_prowler_data()
        time.sleep(5)
        prowler_sync_cmdb()
        time.sleep(5)

        run_get_gdpr_data()
        time.sleep(5)
        gdpr_sync_cmdb()
        time.sleep(5)

        run_get_hipaa_data()
        time.sleep(5)
        hipaa_sync_cmdb()
        time.sleep(5)

    elif erver_start_time_2 < now_time <= server_end_time_2:
        eip_sync_cmdb()
        time.sleep(5)
        sgs_sync_cmdb()
        time.sleep(5)
        asg_sync_cmdb()
        time.sleep(5)
        vpc_endpoint_sync_cmdb()
        time.sleep(5)
        vpc_peering_sync_cmdb()
        time.sleep(5)
        vpc_sync_cmdb()
        time.sleep(5)
        uncom_vpc_sync_cmdb()
        time.sleep(5)
        uncom_vpc_peering_sync_cmdb()
        time.sleep(10)
        com_ec2_sync_cmdb()
        time.sleep(5)
        uncom_ec2_sync_cmdb()
        time.sleep(10)
        iam_permission_sync_cmdb()

    else:
        pass


if __name__ == '__main__':
    tail_data()
