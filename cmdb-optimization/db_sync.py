#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/12/24
Desc    : 
"""

from models.rds import Base as RDSBase
from models.elb import Base as ELBBase
from models.nat import Base as NATBase
from models.ebs import Base as EBSBase
from models.eip import Base as FreeEipBase
from websdk.consts import const
from settings import settings as app_settings
# ORM创建表结构
from sqlalchemy import create_engine

default_configs = app_settings[const.DB_CONFIG_ITEM][const.DEFAULT_DB_KEY]
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    default_configs.get(const.DBUSER_KEY),
    default_configs.get(const.DBPWD_KEY),
    default_configs.get(const.DBHOST_KEY),
    default_configs.get(const.DBPORT_KEY),
    default_configs.get(const.DBNAME_KEY),
), encoding='utf-8', echo=True)


def create():
    RDSBase.metadata.create_all(engine)
    ELBBase.metadata.create_all(engine)
    NATBase.metadata.create_all(engine)
    EBSBase.metadata.create_all(engine)
    FreeEipBase.metadata.create_all(engine)
    print('[Success] 表结构创建成功!')


def drop():
    pass


if __name__ == '__main__':
    create()
