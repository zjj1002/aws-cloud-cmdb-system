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


class PocsuiteTask(Base):

    __tablename__ = 'pocsuite_task'

    id = Column('id', String(32), primary_key=True,  default = shortuuid.uuid())
    name = Column('name', String(56), nullable=True)
    target = Column('target',TEXT(65535), nullable=True)
    poc = Column('poc',TEXT(65535), nullable=True)
    thread = Column('thread', String(18), nullable=True)
    date = Column('date', String(32), nullable=True)
    end_date = Column('end_date', String(64), nullable=True)
    status = Column('status', String(18), nullable=True)
    vul_count = Column('vul_count', String(32), nullable=True)
    op = Column('op', Float, nullable=True)



class PocsuitePlugin(Base):

    __tablename__ = 'pocsuite_plugin'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    app = Column('app', String(56), nullable=True)
    date = Column('date', String(56), nullable=True)
    name = Column('name', String(128), nullable=True)
    op = Column('op', String(32), nullable=True)
    poc_str = Column('poc_str', TEXT(65535), nullable=True)
    filename = Column('filename', String(128), nullable=True)
    poc_type = Column('poc_type', String(56), nullable=True)
    pid = Column('pid', String(56), nullable=True)
    type = Column('type', String(56), nullable=True)


class Target(Base):

    __tablename__ = 'pocsuite_target'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    url = Column('url', String(56), nullable=False)
    vul_count = Column('vul_count', Integer, nullable=False)
    last_modifield = Column('last_modifield', String(64), nullable=False)


class Result(Base):

    __tablename__ = 'pocsuite_result'

    id = Column('id', String(32), primary_key=True,  default = shortuuid.uuid())
    tid = Column('tid', String(32), nullable=True)
    poc = Column('poc', TEXT(512), nullable=True)
    task_name = Column('task_name', String(128), nullable=True)
    status = Column('status', String(56), nullable=True)
    result = Column('result', String(512), nullable=True)
    url = Column('url', String(56), nullable=True)
    mode = Column('mode', String(56), nullable=True)
    vul_id = Column('vul_id', String(56), nullable=True)
    name = Column('name', String(128), nullable=True)
    app_name = Column('app_name', String(56), nullable=True)
    app_version = Column('app_version', String(56), nullable=True)
    target = Column('target', String(56), nullable=True)
    poc_name = Column('poc_name', String(128), nullable=True)
    created = Column('created', String(56), nullable=True)




