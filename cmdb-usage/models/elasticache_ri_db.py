#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :2020/9/24
# @Author  : Fred liuchuanhao
# @File    : elasticache_ri_db.py
# @Role    : ORM


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint, DECIMAL
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class RiElastiCache(Base):
    __tablename__ = 'ri_elasticache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ReservedCacheNodeId = Column('ReservedCacheNodeId', String(128))
    ReservedCacheNodesOfferingId = Column('ReservedCacheNodesOfferingId', String(255))
    CacheNodeType = Column('CacheNodeType', String(255))
    Duration = Column('Duration', String(255), )
    FixedPrice = Column('FixedPrice', String(128))
    UsagePrice = Column('UsagePrice', String(128))
    CacheNodeCount = Column('CacheNodeCount', String(128))
    ProductDescription = Column('ProductDescription', String(128))
    OfferingType = Column('OfferingType', String(128))
    State = Column('State', String(128))
    RecurringCharges = Column('RecurringCharges', String(128))
    create_time = Column('create_time', DateTime(), default=datetime.now)
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class AWSElastiCacheRiUsageReport(Base):
    __tablename__ = 'aws_elasticache_ri_usage_report'

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

    def merge(self, AWSElastiCacheRiUsageReport):
        if self.dbclass == AWSElastiCacheRiUsageReport.dbclass and self.dbengine == AWSElastiCacheRiUsageReport.dbengine:
            if self.dbsize == AWSElastiCacheRiUsageReport.dbsize:
                total_running = AWSElastiCacheRiUsageReport.total_running
                total_ri = AWSElastiCacheRiUsageReport.total_ri
            else:
                return False
            self.total_running += total_running
            self.total_ri += total_ri
            return True