#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 13:48

# @File    : db.py
# @Role    : ORM
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

from libs.common import get_factor_num_with_xlarge

Base = declarative_base()


def model_to_dict(model, time_strf=None):
    model_dict = {}
    time_strf = time_strf or "%Y-%m-%d %H:%M:%S"
    for key, column in class_mapper(model.__class__).c.items():
        value = getattr(model, key, None)
        if isinstance(value, datetime):
            value = value.strftime(time_strf)
        model_dict[column.name] = value
    return model_dict


class ResourceUsage(Base):
    __tablename__ = 'resource_usage'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    ec2_id = Column('ec2_id', String(128), nullable=False)  # 实例ID
    cpu_usage = Column('cpu_usage', Integer(), nullable=True)  # CPU使用率
    mem_usage = Column('mem_usage', Integer(), nullable=True)  # 内存使用率
    disk_usage = Column('disk_usage', Integer(), nullable=True)  # 磁盘使用率
    date = Column('date', DateTime(), nullable=False)  # 月份
    __table_args__ = (
        UniqueConstraint('ec2_id', 'date', name='uix_ec2_date'),
    )


class UsageReport(Base):
    __tablename__ = 'usage_report'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    ec2_id = Column('ec2_id', String(128), nullable=False)  # 实例ID
    host_name = Column('host_name', String(128), nullable=False)  # 实例名字
    project_name = Column('project_name', String(128), nullable=False)  # 项目名称
    cpu_avg_usage = Column('cpu_avg_usage', Integer(), nullable=False)  # CPU当月平均使用率
    mem_avg_usage = Column('mem_avg_usage', Integer(), nullable=False)  # 内存当月平均使用率
    disk_avg_usage = Column('disk_avg_usage', Integer(), nullable=False)  # 磁盘当月平均使用率
    curr_inst_type = Column('curr_inst_type', String(128), nullable=False)  # 当前实例类型
    suggest_inst_type = Column('suggest_inst_type', String(128), nullable=False)  # 建议实例类型
    cost_gap = Column('cost_gap', DECIMAL(10, 5), nullable=True)  # 费用差
    month = Column('month', DateTime(), nullable=False)  # 月份
    __table_args__ = (
        UniqueConstraint('ec2_id', 'month', name='uix_ec2_month'),
    )


class AWSRiUsageReport(Base):
    __tablename__ = 'aws_ri_usage_report'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    family = Column('family', String(128), nullable=True)  # 家族
    size = Column('size', String(128), nullable=True)  # 实例大小,Linux平台默认为xlarge
    platform = Column('platform', String(128), nullable=True)  # 平台：
    # available_zone = Column('available_zone', String(128), nullable=True)  # 区
    total_running = Column('total_running', DECIMAL(10, 5), nullable=True)  # 当前运行数量
    total_ri = Column('total_ri', DECIMAL(10, 5), nullable=True)  # RI购买数量
    coverage_rate = Column('coverage_rate', DECIMAL(10, 5), nullable=True)  # RI覆盖率
    date = Column('date', DateTime(), nullable=True)  # 月份
    __table_args__ = (
        UniqueConstraint('family', 'size', 'platform', 'date', name='uix_date'),
    )

    def merge(self, AWSRiUsageReport):
        if self.family == AWSRiUsageReport.family \
                and self.platform == AWSRiUsageReport.platform:
            if self.platform == "UNIX/Linux":
                total_running = get_factor_num_with_xlarge(AWSRiUsageReport.size) * AWSRiUsageReport.total_running
                total_ri = get_factor_num_with_xlarge(AWSRiUsageReport.size) * AWSRiUsageReport.total_running
            elif self.size == AWSRiUsageReport.size:
                total_running = AWSRiUsageReport.total_running
                total_ri = AWSRiUsageReport.total_ri
            else:
                return False
            self.total_running += total_running
            self.total_ri += total_ri
            return True


class AwsTaskQueue(Base):
    __tablename__ = 'aws_task_queue'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    date = Column('date', DateTime(), nullable=True)  # 任务时间
    task_name = Column('task_name', String(128), nullable=True)  # 任务类型
    status = Column('status', Integer, nullable=True)  # 状态，0：等待执行，1：执行失败，2：已完成。


class AwsProjectBillReport(Base):
    __tablename__ = 'aws_project_bill_report'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    userproject = Column('userproject', String(32), nullable=True)  # 项目
    ec2_cost = Column('ec2_cost', DECIMAL(10, 5), nullable=True)  # ec2
    ebs_cost = Column('ebs_cost', DECIMAL(10, 5), nullable=True)  # ebs
    snapshot_cost = Column('snapshot_cost', DECIMAL(10, 5), nullable=True)  # snapshot
    s3_cost = Column('s3_cost', DECIMAL(10, 5), nullable=True)  # s3
    rds_cost = Column('rds_cost', DECIMAL(10, 5), nullable=True)  # rds
    elasticache_cost = Column('elasticache_cost', DECIMAL(10, 5), nullable=True)  # ElastiCache
    credit = Column('credit', DECIMAL(10, 5), nullable=True)  # Credit
    no_reserved_ri_cost = Column('no_reserved_ri_cost', DECIMAL(10, 5), nullable=True)  # no_reserved_ri_cost
    support_cost = Column('support_cost', DECIMAL(10, 5), nullable=True)  # Support费用
    t_a_x = Column('t_a_x', DECIMAL(10, 5), nullable=True)  # 税费
    aws_total_cost = Column('aws_total_cost', DECIMAL(10, 5), nullable=True)  # 总费用
    bill_date = Column('bill_date', DateTime(), nullable=True)  # 账单日期
    __table_args__ = (
        UniqueConstraint('userproject', 'bill_date', name='unix'),
    )


class AwsServiceBillReport(Base):
    __tablename__ = 'aws_service_bill_report'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    resource_id = Column('resource_id', String(64), nullable=True)  # 资源id
    Tag_AppName = Column('Tag_AppName', String(64), nullable=True)  #应用名称
    Tag_Center = Column('Tag_Center', String(64), nullable=True) #数据中心名称
    Tag_Team = Column('Tag_Team', String(64), nullable=True)  #组织架构名称
    Traffic_charges = Column('Traffic_charges', DECIMAL(10, 5), nullable=True) #流量费用
    service_name = Column('service_name', String(64), nullable=True)  # 服务名
    userproject = Column('userproject', String(32), nullable=True)  # 项目名
    total_cost = Column('total_cost', DECIMAL(10, 5), nullable=True)  # 费用
    bill_date = Column('bill_date', DateTime(), nullable=True)  # 账单日期
    __table_args__ = (
        UniqueConstraint('userproject', 'service_name', 'resource_id', 'bill_date', name='unix'),
    )


class AWSRiDateDB(Base):
    __tablename__ = 'aws_ri_date_num'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    family = Column('family', String(128), nullable=True)  # 家族
    size = Column('size', String(128), nullable=True)  # 实例大小,Linux平台默认为xlarge
    platform = Column('platform', String(128), nullable=True)  # 平台：
    total_ri = Column('total_ri', DECIMAL(10, 5), nullable=True)  # RI购买数量
    end = Column('end', String(128), nullable=True) #过期时间


class AwsProjectBudgetControl(Base):
    __tablename__ = 'aws_project_budget'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    userproject = Column('userproject', String(32), nullable=True)  # 项目
    aws_total_cost = Column('aws_total_cost', DECIMAL(10, 5), nullable=True)  # 总费用
    aws_budget_cost = Column('aws_budget_cost', DECIMAL(10, 5), nullable=True)  # 预算费用
    aws_alert_percentage = Column('aws_alert_percentage', DECIMAL(10, 5), default=1.2)  # 警戒百分比
    aws_percentage = Column('aws_percentage', DECIMAL(10, 5), nullable=True)  # 费用百分比
    bill_date = Column('bill_date', DateTime(), nullable=True)  # 账单日期
