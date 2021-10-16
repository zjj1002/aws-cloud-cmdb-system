#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :2020/9/24
# @Author  : Fred liuchuanhao
# @File    : elasticsearch.py
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


class ElasticSearch(Base):
    __tablename__ = 'asset_elasticsearch'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_id = Column('domain_id', String(255), nullable=False)
    domain_name = Column('domain_name', String(255), nullable=False)
    ARN = Column('ARN', String(255), nullable=False)
    created = Column('created', String(255), nullable=False)
    deleted = Column('deleted', String(255), nullable=False)
    vpc = Column('vpc', String(255), nullable=False)
    processing = Column('processing', String(255))
    version = Column('version', String(255), nullable=False)
    instance_count = Column('instance_count', String(255), nullable=False)
    instance_type = Column('instance_type', String(255), nullable=False)
    dedicated_master_enabled = Column('dedicated_master_enabled', String(255), nullable=False)
    zone_awareness_enabled = Column('zone_awareness_enabled', String(255), nullable=False)
    ebs_enabled = Column('ebs_enabled', String(255))
    volume_type = Column('volume_type', String(255))
    volume_size = Column('volume_size', String(255))
    access_policies = Column('access_policies', String(255), nullable=False)
    automated_snapshot_start_hour = Column('automated_snapshot_start_hour', String(255), nullable=False)
    subnetids = Column('subnetids', String(255))
    availability_zones = Column('availability_zones', String(255))
    security_group_ids = Column('security_group_ids', String(255))
    encryption_at_rest_options = Column('encryption_at_rest_options', String(255), nullable=False)
    tag_list = Column('tag_list', String(512))  ### tag

