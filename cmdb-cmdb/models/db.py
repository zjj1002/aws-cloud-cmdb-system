#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 13:48
# @Author  : Fred Yangxiaofei
# @File    : db.py
# @Role    : ORM


from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class DBTag(Base):
    __tablename__ = 'asset_db_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    db_id = Column('db_id', Integer)
    tag_id = Column('tag_id', Integer)


class DB(Base):
    __tablename__ = 'asset_db'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    idc = Column('idc', String(128))  # IDC
    db_instance_id = Column('db_instance_id', String(128))  #RDS实例ID
    db_code = Column('db_code', String(255))  ### 名称 代号 编码
    db_class = Column('db_class', String(255))  ### DB实例类型
    db_host = Column('db_host', String(255), nullable=False) ### DB主机地址
    db_public_ip = Column('db_public_ip', String(255)) ### DB主机外网地址,只有少量的才会开启
    db_port = Column('db_port', String(10), nullable=False, default=3306)  ### DB端口
    db_user = Column('db_user', String(128), nullable=False, default='root') ### DB用户
    db_pwd = Column('db_pwd', String(128))   ### DB的密码
    db_disk = Column('db_disk', String(128))  ### DB的磁盘，主要RDS有
    db_region = Column('db_region', String(128)) ### DB的区域 可用区
    db_env = Column('db_env', String(128), default='release')  ### 环境/release/dev
    db_type = Column('db_type', String(128))  ### 标记类型如：MySQL/Redis
    db_version = Column('db_version', String(128)) ###DB版本
    db_mark = Column('db_mark', String(255))  ### 标记读写备
    state = Column('state', String(128))   ### DB的状态
    db_detail = Column('db_detail', String(255))  ### 描述
    proxy_host = Column('proxy_host', String(128))  ### 代理主机 适配多云,预留
    tag = Column('tag', String(512))  ### tag
    db_multiaz = Column('db_multiaz', String(128))  ### 显示是否多可用区部署
    Iops = Column('Iops', String(128))  ### iops
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间

class Security_Host(Base):
    __tablename__ = 'security_host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column('server_name', String(128)) ###主机名
    server_instance_id = Column('server_instance_id', String(128),default='')  #实例ID
    server_private_ip = Column('server_private_ip', String(255), nullable=False) ### 内网ip
    server_public_ip = Column('server_public_ip', String(255),default='') ### 外网地址
    server_Project = Column('server_Project', String(128), default='')  ### 此机器属于哪个项目
    server_mark = Column('server_mark', String(255),default='')  ### 是否确认这些打开的端口安全
    security_state = Column('security_state', String(128),default='')   ### server的安全备注
    risk_port = Column('risk_port', String(255),default='') ###风险端口
    security_group = Column('security_group', Text) ###attach的安全组

class Unattach_Ebs(Base):
    __tablename__ = 'Unattach_Ebs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Attachments = Column('Attachments', String(128)) 
    AvailabilityZone = Column('AvailabilityZone', String(128),default='')  
    CreateTime = Column('CreateTime', String(255), nullable=False) 
    Encrypted = Column('Encrypted', String(255),default='') 
    Size = Column('Size', Integer, default=0)  
    SnapshotId = Column('SnapshotId', String(255),default='')  
    State = Column('State', String(255),default='')   
    VolumeId = Column('VolumeId', String(255),default='') 
    Iops = Column('Iops', Integer,default=0) 
    VolumeType = Column('VolumeType', String(255),default='') 


class S3(Base):
    __tablename__ = 'asset_s3'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    bucket_name = Column('bucket_name', String(128),nullable=False)
    bucket_tags = Column('bucket_tags', String(255))
    bucket_acl = Column('bucket_acl', Integer(),nullable=False)
    bucket_lifecycle = Column('bucket_lifecycle', Integer(), nullable=False)
    bucket_mark = Column('bucket_mark', Boolean(),default=0)
    bucket_remark = Column('bucket_remark', String(255), default="")
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间

class Dns(Base):
    __tablename__ = 'asset_dns'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    dns_name = Column('dns_name', String(255),nullable=False)
    dns_status = Column('dns_status', String(255))
    dns_type = Column('dns_type', String(255),nullable=False)
    dns_value = Column('dns_value', String(255), nullable=False)
    dns_ttl = Column('dns_ttl',Integer(),default=600)
    dns_remark = Column('dns_remark',String(255),default="")

# class ProxyInfo(Base):
#     __tablename__ = 'asset_proxy_info'
#
#     ### 代理主机  通过此主机来连接数据库
#     id = Column('id', Integer, primary_key=True, autoincrement=True)
#     proxy_host = Column('proxy_host', String(60), unique=True, nullable=False)
#     inception = Column('inception', String(300))
#     salt = Column('salt', String(300))
#     detail = Column('detail', String(20))


class ElastiCache(Base):
    __tablename__ = 'asset_elcaticache'
    ### 数据库集群
    id = Column(Integer, primary_key=True, autoincrement=True)
    idc = Column('idc', String(128))  # IDC
    db_code = Column('db_code', String(255))  ### 名称 代号 编码
    db_class = Column('db_class', String(255))  ### DB实例类型
    db_host = Column('db_host', String(255), ) ### DB主机地址
    db_port = Column('db_port', String(10))  ### DB端口
    db_user = Column('db_user', String(128)) ### DB用户
    db_region = Column('db_region', String(128)) ### DB的区域 可用区
    db_type = Column('db_type', String(128))  ### 标记类型如：MySQL/Redis
    db_version = Column('db_version', String(128)) ###DB版本
    state = Column('state', String(128))   ### DB的状态
    db_detail = Column('db_detail', String(255))  ### 描述
    tag_list = Column('tag_list', String(512))  ### tag
    db_node_num = Column('db_node_num', String(128))  ### 节点个数
    db_shard_num = Column('db_shard_num', String(128))  ### 分片个数
    cluster_enabled = Column('cluster_enabled', String(128))  ### 是否开启cluster
    create_time = Column('create_time', DateTime(), default=datetime.now)  # 创建时间
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)  # 记录更新时间
