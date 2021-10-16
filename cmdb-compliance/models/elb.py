from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class ElbDB(Base):
    __tablename__ = 'ec2_elb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(64), nullable=False)
    dnsname = Column('dnsname', String(128), nullable=False)
    region = Column('region', String(64))
    vpcid = Column('vpcid', String(64))
    scheme = Column('scheme', String(64))
    is_use = Column('is_use', Boolean(), default=True, )  # 判断elb是否在使用 True：在使用 False：未使用
    type = Column('type', String(64))  # 判断负载均衡的类型 nlb/alb/lb
    is_encry_trans = Column('is_encry_trans', Boolean(), default=True)  # 判断公网传输是否加密True：已加密 False：未加密
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class TargetGroupDB(Base):
    __tablename__ = 'target_groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_group_arn = Column('target_group_arn', String(128), nullable=True)
    target_group_name = Column('target_group_name', String(128), nullable=True)
    protocol = Column('protocol', String(64), nullable=True)
    port = Column('port', Integer())
    vpc_id = Column('vpc_id', String(64), nullable=True)
    target_type = Column('target_type', String(64), nullable=True)
    is_use = Column('is_use', Boolean(), default=True)  # 判断目标群组是否在使用 True：在使用 False：未使用
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)
