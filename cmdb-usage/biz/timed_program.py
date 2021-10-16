#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-03-13 11:08
# @Author : jianxlin
# @Site :
# @File : host.py
# @Software: PyCharm
import logging
from datetime import datetime, timedelta
import math
from time import sleep

from libs.aws.bill import get_project_budget, update_project_budget
from libs.aws.ec2 import EC2
from libs.aws.elasticache_ri_coverage import main as elasticache_ri_coverage_main
from libs.aws.price import Ec2OnDemandPrice
from websdk.consts import const

from libs.aws.ec2_client import AwsEc2Client
from libs.common import get_instance_type_info
from libs.common import catch_exception
from libs.zbx.host import UserZbx
# from libs.db_context import DBContext
from websdk.db_context import DBContext
from models.db import UsageReport, AWSRiUsageReport, AwsTaskQueue
from libs.date.report_date import report_date
from models.db import ResourceUsage
from libs.aws.resource import get_ec2_resource
from libs.task.task import run_task
from libs.aws.rds_ri_coverage import main as rds_ri_coverage
from libs.aws.rds_ri import main as rds_main
from libs.aws.elasticache_ri import main as elasticache_main

#定义一个类 可以根据ec2ID获取其他信息
class Ec2Report(object):
    def __init__(self, ec2_id=None):
        self.ec2_id = ec2_id
        self._host_name = ""
        self._project_name = ""
        self._curr_inst_type = ""
        self._suggest_inst_type = ""
        self._is_available_instance = True
        self._cost_gap =0
        self._usage_list = {
            "cpu": [],
            "mem": [],
            "disk": [],
        }
        self.__setter()

    @property
    def host_name(self):
        return self._host_name

    @property
    def project_name(self):
        return self._project_name

    @property
    def curr_inst_type(self):
        return self._curr_inst_type

    @property
    def suggest_inst_type(self):
        return self._suggest_inst_type

    @property
    def is_available_instance(self):
        return self._is_available_instance

    @property
    def cost_gap(self):
        return self._cost_gap

    #返回使用率数据
    @property
    def has_usage_data(self):
        return len(self._usage_list["cpu"]) > 0 \
               and len(self._usage_list["cpu"]) > 0 \
               and len(self._usage_list["cpu"]) > 0

    #根据实例的tags设置host_name
    def __set_name(self, tags):
        for tag in tags:
            if tag["Key"] == "Name":
                self._host_name = tag["Value"]

            if tag["Key"] == "Project":
                self._host_name = tag["Value"]

    def set_suggest_type(self, cpu, mem):
        ec2 = EC2()
        ret = ec2.get_instance_type_dict()
        su_list = {}
        for i in ret.keys():
            if "t3." in i or "m5." in i or "c5." in i or "r5." in i:
                su_list.update({i: ret[i]})
        if self._curr_inst_type not in ret.keys():
            self._suggest_inst_type = ""
            return self._suggest_inst_type
        cpu_num = ret[self._curr_inst_type]["cpu_num"] #当前类型cpu个数
        mem_num = ret[self._curr_inst_type]["mem"] #当前类型内存大小
        cpu_suggest = cpu_num*cpu /0.65  # 建议类型的cpu个数
        men_suggest = mem_num*mem/0.65    #建议类型的内存大小
        #筛选出满足cpu和mem大于建议配置的实例
        suggest_type_list = { k:v for k,v in su_list.items() if v["cpu_num"] >= cpu_suggest and v["mem"] >=men_suggest}
        #在直角坐标系中找出离建议配置最近的点的实例类型（cup个数放大10000倍）
        re_list = {k: (math.pow(v["cpu_num"]*10000 - cpu_suggest*10000,2) + math.pow(v["mem"] - men_suggest,2)) for k,v in suggest_type_list.items()}
        #找出距离最近的点 即为推荐类型
        suggest_type_list_sort = sorted(re_list.items(), key=lambda x: x[1])
        for k in suggest_type_list_sort:
            cost_gap = self.get_cost_gap(self._curr_inst_type, k[0])
            if cost_gap > 0:
                self._suggest_inst_type = k[0]
                break
        # self._suggest_inst_type = min(re_list,key=re_list.get)
        if self._suggest_inst_type == self._curr_inst_type:
            self._suggest_inst_type = ""
            return self._suggest_inst_type
        self._cost_gap = self.get_cost_gap(self._curr_inst_type,self._suggest_inst_type)
        return self._suggest_inst_type ,self._cost_gap

    def get_cost_gap(self,curr_type,suggest_type):
        p = Ec2OnDemandPrice()
        o = p.on_demand_price
        pd_data = o[["UsageType", "Operation", "Region", "Platform", 'OnDemandPrice']]
        curr_type = 'CNW1-BoxUsage:'+ curr_type
        suggest_type = 'CNW1-BoxUsage:'+ suggest_type
        try:
            curr_type_cost = pd_data[(pd_data['UsageType'] == curr_type) & (pd_data['Platform'] == 'Linux')][
                'OnDemandPrice'].values[0]
            suggest_type_coust = pd_data[(pd_data['UsageType'] == suggest_type) & (pd_data['Platform'] == 'Linux')][
                'OnDemandPrice'].values[0]
            self._cost_gap = float(curr_type_cost - suggest_type_coust)
        except Exception as e:
            return 0
        return self._cost_gap*30

    def __set_project_name(self, tags):
        for tag in tags:
            if tag["Key"].lower() == "project":
                self._project_name = tag["Value"]

    def __setter(self):
        instance = get_ec2_resource(self.ec2_id)
        try:
            self._curr_inst_type = instance.instance_type
            self.__set_name(instance.tags)
            self.__set_project_name(instance.tags)
        except Exception as e:
            self._is_available_instance = False

    #添加使用率
    def add_usage(self, ResourceUsage):
        if isinstance(ResourceUsage.cpu_usage, (int, float)):
            self._usage_list["cpu"].append(ResourceUsage.cpu_usage)
        if isinstance(ResourceUsage.mem_usage, (int, float)):
            self._usage_list["mem"].append(ResourceUsage.mem_usage)
        if isinstance(ResourceUsage.disk_usage, (int, float)):
            self._usage_list["disk"].append(ResourceUsage.disk_usage)

    #返回使用率的平均数
    def get_avg_usage(self, name):
        return sum(self._usage_list[name]) / len(self._usage_list[name]) if len(self._usage_list[name]) > 0 else None

#使用zabbix工具监控实例的cpu使用率，内存使用率，磁盘使用率，并写入ResourceUsage表中
@catch_exception
def sync_host_usage_from_zabbix():
    uz = UserZbx()
    usage_info = uz.get_ec2_usage_info()
    d = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    with DBContext('w', const.DEFAULT_DB_KEY, need_commit=True) as session:
        for k, v in usage_info.items():
            exist_usage = session \
                .query(ResourceUsage) \
                .filter(ResourceUsage.ec2_id == v["ec2_id"],
                        ResourceUsage.date == d,
                        ).first()
            if exist_usage:
                session \
                    .query(ResourceUsage) \
                    .filter(ResourceUsage.ec2_id == v["ec2_id"],
                            ResourceUsage.date == d,
                            ).update(
                    {
                        ResourceUsage.ec2_id: v["ec2_id"],
                        ResourceUsage.cpu_usage: v["cpu"],
                        ResourceUsage.mem_usage: v["mem"],
                        ResourceUsage.disk_usage: v["disk"],
                        ResourceUsage.date: d,
                    }
                )
            else:
                new_record = ResourceUsage(ec2_id=v["ec2_id"],
                                           cpu_usage=v["cpu"],
                                           mem_usage=v["mem"],
                                           disk_usage=v["disk"],
                                           date=d)
                session.add(new_record)
            session.commit()

#更新使用率报告表单
@catch_exception
def update_usage_report():
    #起止时间为月初1号到昨天
    last_day = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    last_day_month_first_day = last_day.replace(day=1)

    with DBContext('wr', const.DEFAULT_DB_KEY, need_commit=True) as session:
        # 查询当月所有主机资源使用率信息
        usage_data = session.query(ResourceUsage) \
            .filter(ResourceUsage.date >= last_day_month_first_day) \
            .filter(ResourceUsage.date <= last_day) \
            .all()

        # 按ec2id整主机资源使用信息。
        ec2_reports = {}
        for ud in usage_data:
            if ud.ec2_id not in ec2_reports.keys():
                #使用Ec2Report类查询ec2信息并保存在字典中
                ec2_reports[ud.ec2_id] = Ec2Report(ec2_id=ud.ec2_id)
            eu = ec2_reports[ud.ec2_id]
            #判断ec2实例是否有效 有效则添加使用率信息
            if eu.is_available_instance:
                eu.add_usage(ud)

        # 计算资源使用信息，并写如资源使用报表
        for ec2_id, ec2_report in ec2_reports.items():
            if not ec2_report.is_available_instance:
                continue

            #判断有没有资源使用率的数据
            if not ec2_report.has_usage_data:
                continue

            #推荐实例类型
            cpu_avg_usage = ec2_report.get_avg_usage("cpu")
            mem_avg_usage = ec2_report.get_avg_usage("mem")
            ec2_report.set_suggest_type(cpu_avg_usage*0.01,mem_avg_usage*0.01)

            #判断库中这个月是否有ec2的使用率报表
            exist_usage = session \
                .query(UsageReport) \
                .filter(UsageReport.ec2_id == ec2_id, UsageReport.month == last_day_month_first_day) \
                .first()
            #存在则更新
            if exist_usage:
                session.query(UsageReport) \
                    .filter(UsageReport.ec2_id == ec2_id, UsageReport.month == last_day_month_first_day) \
                    .update(
                    {
                        UsageReport.cpu_avg_usage: ec2_report.get_avg_usage("cpu"),
                        UsageReport.mem_avg_usage: ec2_report.get_avg_usage("mem"),
                        UsageReport.disk_avg_usage: ec2_report.get_avg_usage("disk"),
                        UsageReport.host_name: ec2_report.host_name,
                        UsageReport.project_name: ec2_report.project_name,
                        UsageReport.curr_inst_type: ec2_report.curr_inst_type,
                        UsageReport.suggest_inst_type: ec2_report.suggest_inst_type,
                        UsageReport.cost_gap: ec2_report.cost_gap
                    }
                )
            #不存在则新加
            else:
                new_record = UsageReport(ec2_id=ec2_id,
                                         cpu_avg_usage=ec2_report.get_avg_usage("cpu"),
                                         mem_avg_usage=ec2_report.get_avg_usage("mem"),
                                         disk_avg_usage=ec2_report.get_avg_usage("disk"),
                                         month=last_day_month_first_day,
                                         host_name=ec2_report.host_name,
                                         project_name=ec2_report.project_name,
                                         curr_inst_type=ec2_report.curr_inst_type,
                                         suggest_inst_type=ec2_report.suggest_inst_type,
                                         cost_gap=ec2_report.cost_gap
                                         )
                session.add(new_record)
            session.commit()



#更新预留实例的数据表
@catch_exception
def update_ri_usage():
    ec = AwsEc2Client()
    # 获取实例的数据
    ec2_instances = ec.get_ec2_list()
    #获取预留实例的数据
    ec2_ri_instances = ec.get_reserved_instances()
    ri_usage_data = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)#今天日期 格式:2020-06-17 00:00:00

    for ei in ec2_instances:
        #判断实例状态 如果是不是running则忽略 进行下一次循环
        if ei.State["Name"] != 'running':
            continue
        family, size, num = get_instance_type_info(ei.Platform, ei.InstanceType)
        ru = AWSRiUsageReport(family=family,
                              size=size,
                              platform=ei.Platform,
                              total_ri=0,
                              date=today,
                              total_running=num)
        #一致则合并，不一致则新建
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
        # 一致则合并，不一致则新建
        for i in range(len(ri_usage_data)):
            if ri_usage_data[i].merge(ru):
                break
        else:
            ri_usage_data.append(ru)
    with DBContext('wr', const.DEFAULT_DB_KEY, need_commit=True) as session:
        for rud in ri_usage_data:
            #计算覆盖率
            rud.coverage_rate = rud.total_ri / rud.total_running if rud.total_running > 0 else -0.1
            session.add(rud)


#更新四天前的账单
@catch_exception
def update_the_bill_four_days_ago():
    from libs.main import NewReport
    date = datetime.now()
    fourDayAgo = date - timedelta(days=4)
    report_date.set_date(date=fourDayAgo)
    new_report = NewReport()
    new_report.create_report()
    logging.info("更新四天前的账单完成")


#设置定时更新时间段
def tail_data():
    server_start_time = datetime.strptime(str(datetime.now().date()) + '00:30', '%Y-%m-%d%H:%M')
    server_end_time = datetime.strptime(str(datetime.now().date()) + '01:30', '%Y-%m-%d%H:%M')

    update_bill_start_time = datetime.strptime(str(datetime.now().date()) + '02:30', '%Y-%m-%d%H:%M')
    update_bill_end_time = datetime.strptime(str(datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')

    now_time = datetime.now()
    if server_start_time < now_time <= server_end_time:
        sync_host_usage_from_zabbix()
        update_usage_report()
        update_ri_usage()

    elif update_bill_start_time < now_time <= update_bill_end_time:
        update_the_bill_four_days_ago()
        rds_main()
        elasticache_main()
        get_project_budget()
        update_project_budget()
        rds_ri_coverage()
        elasticache_ri_coverage_main()

    else:
        pass


def run_task_programs():
    """
        执行队列中的任务
    :return:
    """
    with DBContext('wr', const.DEFAULT_DB_KEY, need_commit=True) as session:
        msg = session.query(AwsTaskQueue).filter(AwsTaskQueue.status < 2).first()
        if msg:
            logging.info("Run Task:" + str(msg.id))
            t = run_task(name=msg.task_name, date=msg.date)
            status = 2 if t else 1
            session.query(AwsTaskQueue) \
                .filter(AwsTaskQueue.id == msg.id) \
                .update(
                {
                    AwsTaskQueue.status: status
                })
            logging.info("Task end:" + str(msg.id))


if __name__ == '__main__':
    update_the_bill_four_days_ago()
    # ret = update_ri_usage()
    # print(ret)
    # sync_host_usage_from_zabbix()
    # update_usage_report()
    # a = Ec2Report("i-0dc802bd6b27c2843")
    # a.get_cost_gap("c5.xlarge","c4.xlarge")



