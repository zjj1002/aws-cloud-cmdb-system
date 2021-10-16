# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
from datetime import datetime
from libs.common import catch_exception
from libs.web_logs import ins_log
from libs.zbx.host import UserZbx
from models.db import ResourceUsage
from websdk.consts import const
from websdk.db_context import DBContext


@catch_exception
def sync_host_usage_from_zabbix_by_day(date):
    uz = UserZbx(time=date)
    usage_info = uz.get_ec2_usage_info()
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    with DBContext('w', const.DEFAULT_DB_KEY, need_commit=True) as session:
        for k, v in usage_info.items():
            exist_usage = session \
                .query(ResourceUsage) \
                .filter(ResourceUsage.ec2_id ==v["ec2_id"],
                        ResourceUsage.date == date,
                        ).first()
            if exist_usage:
                session \
                    .query(ResourceUsage) \
                    .filter(ResourceUsage.ec2_id ==v["ec2_id"],
                            ResourceUsage.date == date,
                            ).update(
                    {
                        ResourceUsage.ec2_id: v["ec2_id"],
                        ResourceUsage.cpu_usage: v["cpu"],
                        ResourceUsage.mem_usage: v["mem"],
                        ResourceUsage.disk_usage:v["disk"],
                        ResourceUsage.date: date,
                    }
                )
            else:
                new_record = ResourceUsage(ec2_id=v["ec2_id"],
                                           cpu_usage=v["cpu"],
                                           mem_usage=v["mem"],
                                           disk_usage=v["disk"],
                                           date=date)
                session.add(new_record)
            session.commit()
    ins_log.read_log('info', '添加{}的数据成功'.format(date))