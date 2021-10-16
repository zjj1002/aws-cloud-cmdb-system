#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 13:48
# @Author  : Fred Yangxiaofei
# @File    : dns.py
# @Role    : ORM


from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class Dns(Base):
    __tablename__ = 'asset_dns'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    dns_name = Column('dns_name', String(255), nullable=False)
    dns_status = Column('dns_status', String(255))
    dns_type = Column('dns_type', String(255), nullable=False)
    dns_value = Column('dns_value', String(255), nullable=False)
    dns_ttl = Column('dns_ttl', Integer(), default=600)
    dns_remark = Column('dns_remark', String(255), default="")
