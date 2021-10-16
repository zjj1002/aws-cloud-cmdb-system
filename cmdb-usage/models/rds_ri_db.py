#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :2020/9/24
# @Author  : Fred liuchuanhao
# @File    : rds_ri_db.py
# @Role    : ORM


from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class RiRds(Base):
    __tablename__ = 'ri_rds'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    ReservedDBInstanceId = Column('ReservedDBInstanceId', String(128))
    ReservedDBInstancesOfferingId = Column('ReservedDBInstancesOfferingId', String(255))
    DBInstanceClass = Column('DBInstanceClass', String(255))
    Duration = Column('Duration', String(255), )
    FixedPrice = Column('FixedPrice', String(128))
    UsagePrice = Column('UsagePrice', String(128))
    CurrencyCode = Column('CurrencyCode', String(128))
    DBInstanceCount = Column('DBInstanceCount', String(128))
    ProductDescription = Column('ProductDescription', String(128))
    OfferingType = Column('OfferingType', String(128))
    MultiAZ = Column('MultiAZ', String(255))
    State = Column('State', String(128))
    RecurringCharges = Column('RecurringCharges', String(128))
    ReservedDBInstanceArn = Column('ReservedDBInstanceArn', String(128))
    create_time = Column('create_time', DateTime(), default=datetime.now)
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class AWSRdsRiUsageReport(Base):
    __tablename__ = 'aws_rds_ri_usage_report'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    dbclass = Column('dbclass', String(128), nullable=True)  # db类型
    dbsize = Column('dbsize', String(128), nullable=True)  # 实例大小
    dbengine = Column('dbengine', String(128), nullable=True)  # db引擎
    total_running = Column('total_running', DECIMAL(10, 5), nullable=True)  # 当前运行数量
    total_ri = Column('total_ri', DECIMAL(10, 5), nullable=True)  # RI购买数量
    coverage_rate = Column('coverage_rate', DECIMAL(10, 5), nullable=True)  # rds_ri覆盖率
    date = Column('date', DateTime(), nullable=True)  # 月份
    __table_args__ = (
        UniqueConstraint('dbclass', 'dbsize', 'dbengine', 'date',name='uix_date'),
    )

    def merge(self, AWSRiUsageReport):
        if self.dbclass == AWSRiUsageReport.dbclass and self.dbengine == AWSRiUsageReport.dbengine:
            if self.dbsize == AWSRiUsageReport.dbsize:
                total_running = AWSRiUsageReport.total_running
                total_ri = AWSRiUsageReport.total_ri
            else:
                return False
            self.total_running += total_running
            self.total_ri += total_ri
            return True