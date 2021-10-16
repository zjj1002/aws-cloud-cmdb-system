# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
import shortuuid

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class AwsSts(Base):
    __tablename__ = 'aws_sts'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    AccessKeyId = Column('AccessKeyId', String(128), nullable=True)
    SecretAccessKey = Column('SecretAccessKey', String(128))
    SessionToken = Column('SessionToken', String(512), nullable=True)
    bucket = Column('bucket', String(128), nullable=True)
    Action= Column('Action', String(128), nullable=True)
    RoleArn= Column('RoleArn', String(128), nullable=True)
    RoleSessionName = Column('RoleSessionName', String(128), nullable=True)
    externalid = Column('externalid', String(128), nullable=True)
    durationseconds = Column('durationseconds', Integer, nullable=True)
    region_name = Column('region_name', String(128), nullable=True)
    add_date = Column('add_date', String(128), nullable=True)





