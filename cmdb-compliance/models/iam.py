# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

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
    __tablename__ = 'iam_db'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', String(64), nullable=False)
    user_name = Column('user_name', String(64), nullable=False)
    arn = Column('arn', String(128), nullable=False)
    aksk_90_used = Column('aksk_90_used', Boolean(), default=False)  # 判断用户的所有ak/sk是否在90天内有使用 True：有使用 False:未使用
    is_90_signin = Column('is_90_signin', Boolean(), default=True)  # 判断用户是否符合在90天内登录 True：符合 False：不符合
    is_2_keys = Column('is_2_keys', Boolean(), default=True)  # 判断用户 是否符合未拥有两个keys， True：符合 false：不符合
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)
