#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date    : 2018/12/24
Desc    : 
"""

from models.db import Base as ABase
from websdk.consts import const
from settings import settings as app_settings
# ORM创建表结构
from sqlalchemy import create_engine
from models.rds_ri_db import Base as RIRDSBASE
from models.elasticache_ri_db import Base as ECBASE
from models.server import Base as IBCBASE

default_configs = app_settings[const.DB_CONFIG_ITEM][const.DEFAULT_DB_KEY]
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    default_configs.get(const.DBUSER_KEY),
    default_configs.get(const.DBPWD_KEY),
    default_configs.get(const.DBHOST_KEY),
    default_configs.get(const.DBPORT_KEY),
    default_configs.get(const.DBNAME_KEY),
), encoding='utf-8', echo=True)


def create():
    ABase.metadata.create_all(engine)
    RIRDSBASE.metadata.create_all(engine)
    ECBASE.metadata.create_all(engine)
    IBCBASE.metadata.create_all(engine)
    print('[Success] 表结构创建成功!')


def drop():
    ABase.metadata.drop_all(engine)


if __name__ == '__main__':
    create()
