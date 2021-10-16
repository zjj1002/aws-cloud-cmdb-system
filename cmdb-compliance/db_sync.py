#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/12/24
Desc    : 
"""

from models.server import Base
from models.db import Base as ABase
from models.dns import Base as DnsBase
from models.s3 import Base as S3Base
from models.rds import Base as RDSBase
from models.elb import Base as ELBBase
from models.nat import Base as NATBase
from models.iam import Base as IAMBase
from models.ebs import Base as EBSBase
from models.pocsutie_db import Base as POCBase
from models.clair_db import Base as CLAIRbase
from models.git_secrets import Base as GITbase
from models.aws_sts import Base as STSEbase
from models.kube_bench import Base as KUBEEbase
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
    Base.metadata.create_all(engine)
    DnsBase.metadata.create_all(engine)
    S3Base.metadata.create_all(engine)
    ABase.metadata.create_all(engine)
    RDSBase.metadata.create_all(engine)
    ELBBase.metadata.create_all(engine)
    NATBase.metadata.create_all(engine)
    IAMBase.metadata.create_all(engine)
    EBSBase.metadata.create_all(engine)
    CLAIRbase.metadata.create_all(engine)
    POCBase.metadata.create_all(engine)
    GITbase.metadata.create_all(engine)
    STSEbase.metadata.create_all(engine)
    KUBEEbase.metadata.create_all(engine)
    print('[Success] 表结构创建成功!')


def drop():
    Base.metadata.drop_all(engine)
    ABase.metadata.drop_all(engine)



if __name__ == '__main__':
    create()
