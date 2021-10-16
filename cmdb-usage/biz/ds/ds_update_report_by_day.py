# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from datetime import datetime
import math
from libs.aws.ec2 import EC2
from libs.aws.price import Ec2OnDemandPrice
from websdk.consts import const
from libs.common import catch_exception
from websdk.db_context import DBContext
from models.db import UsageReport
from models.db import ResourceUsage
from libs.aws.resource import get_ec2_resource
import datetime
from libs.web_logs import ins_log

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
        if self._curr_inst_type not in ret.keys():
            self._suggest_inst_type = ""
            return self._suggest_inst_type
        cpu_num = ret[self._curr_inst_type]["cpu_num"]
        mem_num = ret[self._curr_inst_type]["mem"]
        cpu_suggest = cpu_num*cpu /0.65
        men_suggest = mem_num*mem/0.65
        #筛选出满足cpu和mem大于建议配置的实例
        suggest_type_list = { k:v for k,v in ret.items() if v["cpu_num"] >= cpu_suggest and v["mem"] >=men_suggest}
        #在直角坐标系中找出离建议配置最近的点的实例类型（cup个数放大10000倍）
        re_list = {k: (math.pow(v["cpu_num"]*10000 - cpu_suggest*10000,2) + math.pow(v["mem"] - men_suggest,2)) for k,v in suggest_type_list.items()}
        #找出距离最近的点 即为推荐类型
        self._suggest_inst_type = min(re_list,key=re_list.get)
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
        curr_type_cost = pd_data[(pd_data['UsageType'] == curr_type) & (pd_data['Platform'] == 'Linux')][
            'OnDemandPrice'].values[0]
        suggest_type_coust = pd_data[(pd_data['UsageType'] == suggest_type) & (pd_data['Platform'] == 'Linux')][
            'OnDemandPrice'].values[0]
        self._cost_gap = float(curr_type_cost - suggest_type_coust)
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

    def add_usage(self, ResourceUsage):
        if isinstance(ResourceUsage.cpu_usage, (int, float)):
            self._usage_list["cpu"].append(ResourceUsage.cpu_usage)
        if isinstance(ResourceUsage.mem_usage, (int, float)):
            self._usage_list["mem"].append(ResourceUsage.mem_usage)
        if isinstance(ResourceUsage.disk_usage, (int, float)):
            self._usage_list["disk"].append(ResourceUsage.disk_usage)

    def get_avg_usage(self, name):
        return sum(self._usage_list[name]) / len(self._usage_list[name]) if len(self._usage_list[name]) > 0 else None

# 更新使用率报告表单
@catch_exception
def update_usage_report_by_day(date):
    first_day = datetime.datetime(date.year, date.month, 1)
    first_day_of_next_month = date
    with DBContext('wr', const.DEFAULT_DB_KEY, need_commit=True) as session:
        # 查询当月所有主机资源使用率信息
        usage_data = session.query(ResourceUsage) \
            .filter(ResourceUsage.date >= first_day) \
            .filter(ResourceUsage.date < first_day_of_next_month) \
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

            exist_usage = session \
                .query(UsageReport) \
                .filter(UsageReport.ec2_id == ec2_id, UsageReport.month == first_day_of_next_month) \
                .first()
            if exist_usage:
                session.query(UsageReport) \
                    .filter(UsageReport.ec2_id == ec2_id, UsageReport.month == first_day_of_next_month) \
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
            else:
                new_record = UsageReport(ec2_id=ec2_id,
                                         cpu_avg_usage=ec2_report.get_avg_usage("cpu"),
                                         mem_avg_usage=ec2_report.get_avg_usage("mem"),
                                         disk_avg_usage=ec2_report.get_avg_usage("disk"),
                                         month=first_day_of_next_month,
                                         host_name=ec2_report.host_name,
                                         project_name=ec2_report.project_name,
                                         curr_inst_type=ec2_report.curr_inst_type,
                                         suggest_inst_type=ec2_report.suggest_inst_type,
                                         cost_gap=ec2_report.cost_gap
                                         )
                session.add(new_record)
            session.commit()
        ins_log.read_log('info', '表单更新成功')

if __name__ == '__main__':
    update_usage_report_by_day()
