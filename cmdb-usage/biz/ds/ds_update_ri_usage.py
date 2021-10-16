# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
from datetime import datetime
from libs.web_logs import ins_log
from websdk.consts import const
from libs.aws.ec2_client import AwsEc2Client
from libs.common import get_instance_type_info
from libs.common import catch_exception
from websdk.db_context import DBContext
from models.db import AWSRiUsageReport


@catch_exception
def update_ri_usage_by_day():
    ec = AwsEc2Client()
    ec2_instances = ec.get_ec2_list()
    ec2_ri_instances = ec.get_reserved_instances()
    ri_usage_data = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for ei in ec2_instances:
        if ei.State["Name"] != 'running':
            continue
        family, size, num = get_instance_type_info(ei.Platform, ei.InstanceType)
        ru = AWSRiUsageReport(family=family,
                              size=size,
                              platform=ei.Platform,
                              total_ri=0,
                              date=today,
                              total_running=num)

        for i in range(len(ri_usage_data)):
            if ri_usage_data[i].merge(ru):
                break
        else:
            ri_usage_data.append(ru)

    for eri in ec2_ri_instances:
        family, size, num = get_instance_type_info(eri.ProductDescription, eri.InstanceType)
        ru = AWSRiUsageReport(family=family,
                              size=size,
                              platform=eri.ProductDescription,
                              total_ri=num * eri.InstanceCount,
                              date=today,
                              total_running=0)

        for i in range(len(ri_usage_data)):
            if ri_usage_data[i].merge(ru):
                break
        else:
            ri_usage_data.append(ru)
    with DBContext('wr', const.DEFAULT_DB_KEY, need_commit=True) as session:
        for rud in ri_usage_data:
            rud.coverage_rate = rud.total_ri / rud.total_running if rud.total_running > 0 else -0.1
            exist_usage = session \
                .query(AWSRiUsageReport) \
                .filter(AWSRiUsageReport.family == rud.family,
                        AWSRiUsageReport.size == rud.size,
                        AWSRiUsageReport.platform == rud.platform,
                        AWSRiUsageReport.date == rud.date,
                        ).first()
            if exist_usage:
                session \
                    .query(AWSRiUsageReport) \
                    .filter(AWSRiUsageReport.family == rud.family,
                            AWSRiUsageReport.size == rud.size,
                            AWSRiUsageReport.platform == rud.platform,
                            AWSRiUsageReport.date == rud.date,
                            ).update(
                    {
                        AWSRiUsageReport.family: rud.family,
                        AWSRiUsageReport.size: rud.size,
                        AWSRiUsageReport.platform: rud.platform,
                        AWSRiUsageReport.date: rud.date,
                        AWSRiUsageReport.coverage_rate: rud.coverage_rate,
                        AWSRiUsageReport.total_running: rud.total_running,
                        AWSRiUsageReport.total_ri: rud.total_ri,
                    }
                )
            else:
                session.add(rud)
    ins_log.read_log('info', '预留实例写入数据库共{}条'.format(len(ri_usage_data)))

if __name__ == '__main__':
    update_ri_usage_by_day()
