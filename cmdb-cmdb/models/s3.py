#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 13:48
# @Author  : Fred Yangxiaofei
# @File    : s3.py
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

class S3(Base):
    __tablename__ = 'asset_s3'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    bucket_name = Column('bucket_name', String(128),nullable=False)
    bucket_tags = Column('bucket_tags', String(255))
    bucket_acl = Column('bucket_acl', Integer(),nullable=False)
    bucket_lifecycle = Column('bucket_lifecycle', Integer(), nullable=False)
    bucket_mark = Column('bucket_mark',Integer(),default=0)
    bucket_remark = Column('bucket_remark',String(255),default="")
    size = Column('size',String(255))
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间
