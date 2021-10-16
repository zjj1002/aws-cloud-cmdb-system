#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
Date   : 2017-10-11 12:58:26
Desc   : 配置文件
"""

import os
from websdk.consts import const

ROOT_DIR = os.path.dirname(__file__)
debug = True
xsrf_cookies = False
expire_seconds = 365 * 24 * 60 * 60

ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY', '')
ADMIN_TOKEN_SECRET = os.getenv('ADMIN_TOKEN_SECRET', '')
ADMIN_COOKIES_SECRET = os.getenv('ADMIN_COOKIES_SECRET', '')

DEFAULT_DB_DBHOST = os.getenv('DEFAULT_DB_DBHOST', '172.16.0.223')
DEFAULT_DB_DBPORT = os.getenv('DEFAULT_DB_DBPORT', '3306')
DEFAULT_DB_DBUSER = os.getenv('DEFAULT_DB_DBUSER', 'root')
DEFAULT_DB_DBPWD = os.getenv('DEFAULT_DB_DBPWD', 'ljXrcyn7chaBU4F')
DEFAULT_DB_DBNAME = os.getenv('DEFAULT_DB_DBNAME', 'cmdb_admin')

READONLY_DB_DBHOST = os.getenv('READONLY_DB_DBHOST', '172.16.0.223')
READONLY_DB_DBPORT = os.getenv('READONLY_DB_DBPORT', '3306')
READONLY_DB_DBUSER = os.getenv('READONLY_DB_DBUSER', 'root')
READONLY_DB_DBPWD = os.getenv('READONLY_DB_DBPWD', 'ljXrcyn7chaBU4F')
READONLY_DB_DBNAME = os.getenv('READONLY_DB_DBNAME', 'cmdb_admin')

DEFAULT_REDIS_HOST = os.getenv('DEFAULT_REDIS_HOST', '172.16.0.223')
DEFAULT_REDIS_PORT = os.getenv('DEFAULT_REDIS_PORT', '6379')
DEFAULT_REDIS_DB = 8
DEFAULT_REDIS_AUTH = True
DEFAULT_REDIS_CHARSET = 'utf-8'
DEFAULT_REDIS_PASSWORD = os.getenv('DEFAULT_REDIS_PASSWORD', '123456')

SMTP_SERVER = os.getenv('SMTP_SERVER', '')
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

try:
    from local_settings import *
except:
    pass

settings = dict(
    debug=debug,
    xsrf_cookies=xsrf_cookies,
    cookie_secret=ADMIN_COOKIES_SECRET,
    token_secret=ADMIN_TOKEN_SECRET,
    secret_key=ADMIN_SECRET_KEY,
    expire_seconds=expire_seconds,
    app_name='do_mg',
    databases={
        const.DEFAULT_DB_KEY: {
            const.DBHOST_KEY: DEFAULT_DB_DBHOST,
            const.DBPORT_KEY: DEFAULT_DB_DBPORT,
            const.DBUSER_KEY: DEFAULT_DB_DBUSER,
            const.DBPWD_KEY: DEFAULT_DB_DBPWD,
            const.DBNAME_KEY: DEFAULT_DB_DBNAME,
        },
        const.READONLY_DB_KEY: {
            const.DBHOST_KEY: READONLY_DB_DBHOST,
            const.DBPORT_KEY: READONLY_DB_DBPORT,
            const.DBUSER_KEY: READONLY_DB_DBUSER,
            const.DBPWD_KEY: READONLY_DB_DBPWD,
            const.DBNAME_KEY: READONLY_DB_DBNAME,
        }
    },
    redises={
        const.DEFAULT_RD_KEY: {
            const.RD_HOST_KEY: DEFAULT_REDIS_HOST,
            const.RD_PORT_KEY: DEFAULT_REDIS_PORT,
            const.RD_DB_KEY: DEFAULT_REDIS_DB,
            const.RD_AUTH_KEY: DEFAULT_REDIS_AUTH,
            const.RD_CHARSET_KEY: DEFAULT_REDIS_CHARSET,
            const.RD_PASSWORD_KEY: DEFAULT_REDIS_PASSWORD
        }
    },
    smtp={
        "mail_host": SMTP_SERVER,
        "mail_user": SMTP_USER,
        "mail_password": SMTP_PASSWORD,
        "mail_port": 465,
        "mail_ssl": True
    }
)
