#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : timed_program.py
# @Author: Fred Yangxiaofei
# @Date  : 2019/9/12
# @Role  : 需要定时执行的程序

import time
import datetime
from websdk.web_logs import ins_log

from biz.ds.change_aws_value import change_aws_value
from biz.ds.check_out_services import check_tag_services
from biz.ds.ds_detail_data import get_detail_data
from biz.ds.ds_ec2_instances import ec2_instance_sync_cmdb
from libs.aws.ec2 import main as aws_server_tail
from libs.aliyun.dns import main as aliyun_dns_refresh
from libs.aws.s3 import main as aws_s3_refresh
#from libs.aliyun.ecs import main as aliyun_server_tail
#from libs.qcloud.cvm import main as qcloud_server_tail
#from libs.huaweiyun.huawei_ecs import main as huaweicloud_server_tail

from libs.aws.rds import main as aws_db_tail
from biz.ds.ds_elb import main as instance_dns
#from libs.aliyun.rds import main as aliyun_db_tail
#from libs.qcloud.cdb import main as qcloud_db_tail

from libs.aws.elasticache import main as aws_cache_tail
from libs.aws.tags import main as aws_tags_tail
#from libs.aliyun.redis import main as aliyun_cache_tail
#from libs.qcloud.redis import main as qcloud_cache_tail

from libs.aws.events import main as aws_event_tail
from libs.redis_conn import redis_conn
from libs.server.sync_to_tagtree import main as tagtree_tail_data
from libs.server.asset_auto_update import true_tail_data as true_server_tail
from inventory.aws_inventory1 import get_inventory_data


def tail_data():
    # server
    server_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '00:30', '%Y-%m-%d%H:%M')
    server_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')

    # db and cache
    db_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '03:40', '%Y-%m-%d%H:%M')
    db_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '05:00', '%Y-%m-%d%H:%M')

    # start_services_start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f'{get_uptime()[0]}', '%Y-%m-%d%H:%M')
    # start_services_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f'{get_uptime()[1]}', '%Y-%m-%d%H:%M')
    # stop_services_start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f'{get_downtime()[0]}', '%Y-%m-%d%H:%M')
    # stop_services_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f'{get_downtime()[1]}', '%Y-%m-%d%H:%M')
    # other
    other_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '05:30', '%Y-%m-%d%H:%M')
    other_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '08:00', '%Y-%m-%d%H:%M')
    # now_time
    now_time = datetime.datetime.now()
    if now_time > server_start_time and now_time < server_end_time:
        # update_server
        # ins_log.read_log('info', 'Update Server')
        time.sleep(10)
        aws_server_tail()
        time.sleep(10)
        aliyun_dns_refresh()
        time.sleep(10)
        aws_s3_refresh()
        time.sleep(10)
        aliyun_dns_refresh()
        time.sleep(15)
        instance_dns()

    elif now_time > db_start_time and now_time < db_end_time:
        # update db and cache
        ins_log.read_log('info', 'Update Cache and RDS')
        aws_db_tail()
        aws_cache_tail()
        time.sleep(10)
        aws_tags_tail()

    elif now_time > other_start_time and now_time < other_end_time:
        # update true\tag_tree\aws_events
        ins_log.read_log('info', 'Update True and TagTree and AwsEvnets')
        aws_event_tail()
        time.sleep(5)
        tagtree_tail_data()
        time.sleep(5)
        true_server_tail()

    # elif stop_services_start < now_time < stop_services_end:
    #     ins_log.read_log('info', '关机服务')
        # if not redis_conn.get('stop_key'):
        #     stop_services()
        #     redis_conn.set('stop_key', 1, 60)

    # elif start_services_start < now_time < start_services_end:
    #     ins_log.read_log('info', '开机服务')
        # if not redis_conn.get('start_key'):
        #     start_service()
        #     redis_conn.set('start_key', 1, 60)

    else:
        ins_log.read_log('info', 'No scheduled task execution')
        ins_log.read_log('info', '开始执行定时任务')
        ec2_instance_sync_cmdb()
        time.sleep(15)
        check_tag_services()

        # get_detail_data()
        # time.sleep(15)
        # get_inventory_data()
        # time.sleep(15)
        # time.sleep(15)
        # change_aws_value()


if __name__ == '__main__':
    tail_data()
