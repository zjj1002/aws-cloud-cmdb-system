# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

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



class DB(Base):
    __tablename__ = 'ebs_db'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Attachments = Column('Attachments', String(128))#关联
    AvailabilityZone = Column('AvailabilityZone', String(128),default='')
    CreateTime = Column('CreateTime', String(255), nullable=False)#
    Encrypted = Column('Encrypted', String(255),default='') #是否加密
    Size = Column('Size', Integer, default=0)
    SnapshotId = Column('SnapshotId', String(255),default='')
    State = Column('State', String(255),default='')
    VolumeId = Column('VolumeId', String(255),default='')
    Snapshot_overtime = Column('snapshot_overtime', String(255),default='')
    Iops = Column('Iops', Integer,default=0)
    VolumeType = Column('VolumeType', String(255),default='')
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)
