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


class DB(Base):
    __tablename__ = 'nat_gate_way'

    id = Column(Integer, primary_key=True, autoincrement=True)
    natgatewayid = Column('natgatewayid', String(64), nullable=False)
    state = Column('state', String(64), nullable=False)
    subnetId = Column('subnetId', String(64), nullable=False)
    vpcid = Column('vpcid', String(64), nullable=False)
    is_use = Column('is_use', Boolean(), default=True)  # 判断nat_gate_way 是否符合能使用 True：能使用 false：不能使用
    createTime = Column('createTime', DateTime())
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)
    account_id = Column('account_id', String(64))
    region = Column('region', String(64))