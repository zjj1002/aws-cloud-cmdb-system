#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class AssetIDC(Base):
    __tablename__ = 'asset_idc'
    # IDC管理
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    name = Column('name', String(255), unique=True, nullable=False)  # 名称
    contact = Column('contact', String(255))  # 机房联系人姓名
    email = Column('email', String(255))  # 机房联系人邮箱
    phone = Column('phone', String(255))  # 机房电话
    address = Column('address', String(255))  # 机房地址
    network = Column('network', String(255))  # 机房网络
    bandwidth = Column('bandwidth', String(255))  # 机房带宽大小
    ip_range = Column('ip_range', Text())  # IP地址段
    remarks = Column('remarks', String(150))  # 备注信息


class AssetOperationalAudit(Base):
    __tablename__ = 'asset_operational_audit'
    # 操作审计、操作记录
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    username = Column('username', String(255), nullable=False)  # 用户名
    request_object = Column('request_object', String(255))  # 请求对象
    request_host = Column('request_host', String(255))  # 请求Host
    request_method = Column('request_method', String(255))  # 请求方法
    original_data = Column('original_data', JSON)  # 原数据
    modify_data = Column('modify_data', JSON)  # 修改后的数据
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)
