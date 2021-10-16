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


class GitProject(Base):
    __tablename__ = 'git_projects'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    name = Column('name', String(128), nullable=True)
    branch = Column('branch', String(128), default="master")
    project_team = Column('project_team', String(64), nullable=True)
    source= Column('source', String(128), nullable=True)
    path= Column('path', String(128), nullable=True)
    last_scan_time = Column('last_scan_time', String(64), nullable=True)
    add_date = Column('add_date', String(64), nullable=True)



class GitScanResult(Base):
    __tablename__ = 'git_scan_result'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    name = Column('name', String(128), nullable=True)
    result = Column('result', TEXT(60000), nullable=True)
    risk_index = Column('risk_index', String(128), default="low")
    branch = Column('branch', String(128), default="master")
    project_team = Column('project_team', String(64), nullable=True)
    source = Column('source', String(128), nullable=True)
    Last_scan_time = Column('Last_scan_time', String(64), nullable=True)

