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
    __tablename__ = 'dns_instance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    LoadBalancerArn = Column('LoadBalancerArn', String(128), nullable=True)
    dnsname = Column('dnsname', String(128), nullable=True)
    name = Column('name', String(128), nullable=True)
    instance = Column('instance', String(256), nullable=True)
    update_time = Column('update_time',String(128), nullable=False )

