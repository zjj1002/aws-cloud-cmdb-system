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


class KUBECONFIG(Base):
    __tablename__ = 'kube_config'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    kube_config_name = Column('kube_config_name', String(128), nullable=True)
    server = Column('server', String(128), default="master")
    current_context = Column("current_context", String(512), nullable=True)
    date = Column('add_date', String(64), nullable=True)


class BENCHDB(Base):
    __tablename__ = 'kube_result'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    config_name = Column('config_name', String(128), nullable=True)
    mastr_or_node = Column('mastr_or_node', String(128), nullable=True)
    stats = Column('stats', String(128), nullable=True)
    version = Column('version', String(128), default="master")
    description = Column("description", String(512), nullable=True)
    remediation = Column('remediation', String(2048), nullable=True)
    date = Column('add_date', String(64), nullable=True)
