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
    __tablename__ = 'elb'

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
    account_id = Column('account_id', String(64))


