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


class LocalImage(Base):
    __tablename__ = 'clair_local_images_db'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    REPOSITORY = Column('REPOSITORY', String(128), nullable=True)
    is_scan = Column('is_scan', Boolean(), default=False)
    TAG = Column('TAG', String(64), nullable=True)
    IMAGE_ID = Column('IMAGE_ID', String(64), nullable=True)
    CREATED = Column('CREATED', String(64), nullable=True)
    SIZE = Column('SIZE', String(64), nullable=True)
    last_scan_time = Column('last_scan_time', String(32), nullable=True)


class ScanResult(Base):
    __tablename__ = 'clair_scan_result'

    id = Column('id', String(32), primary_key=True, default=shortuuid.uuid())
    image = Column('image', String(128), nullable=True)
    featurename = Column('featurename', String(56), nullable=True)
    featureversion = Column('featureversion', String(56), nullable=True)
    vulnerability = Column('vulnerability', String(56), nullable=True)
    namespace = Column('namespace', String(56), nullable=True)
    description = Column('description', TEXT(1024), nullable=True)
    link = Column('link', String(226), nullable=True)
    severity = Column('severity', String(56), nullable=True)
    fixedby = Column('fixedby', String(56), nullable=True)
    scan_time = Column('last_scan_time', String(32), nullable=True)
