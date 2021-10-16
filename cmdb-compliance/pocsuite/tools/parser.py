# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

import re
import os
import sys

from libs.web_logs import ins_log
from models.pocsutie_db import PocsuitePlugin
from libs.db_context import DBContext
import shortuuid


def poc_parser(poc_str):
    name_pattern = re.compile(r'name\s*=\s*[\'\"\[](.*)[\'\"\]]')
    app_pattern = re.compile(r'appName\s*=\s*[\'\"\[](.*)[\'\"\]]')
    type_pattern = re.compile(r'vulType\s*=\s*[\'\"\[](.*)[\'\"\]]')
    plugin_info = {
        "name": 'unknown',
        "type": 'unknown',
        "app": 'unknown',
    }
    try:
        plugin_info['name'] = name_pattern.findall(poc_str)[0]
        plugin_info['type'] = type_pattern.findall(poc_str)[0]
        plugin_info['app'] = app_pattern.findall(poc_str)[0]
    except Exception as e:
        ins_log.read_log('info', "pocsuite plugin parser failed: %s" % e)
    return plugin_info


def databases_init():
    try:
        with DBContext('w') as session:
            try:
                session.query(PocsuitePlugin).delete()
                session.commit()
            except:
                session.rollback()
            _poc_path = os.path.abspath(os.path.dirname(__file__)) + "/../pocs"
            if os.path.exists(_poc_path):
                for poc_filename in os.listdir(_poc_path):
                    with open(_poc_path + "/" + poc_filename, "r", encoding="UTF-8") as poc_read:
                        poc_str = poc_read.read()
                        poc_data = poc_parser(poc_str)
                        new_db = PocsuitePlugin(
                            id='poc_' + shortuuid.uuid(),
                            name=poc_data['name'],
                            poc_str=poc_str,
                            filename=poc_filename,
                            app=poc_data['app'],
                            poc_type=poc_data['type'],
                            op="")
                    session.add(new_db)
                    session.commit()
    except Exception as e:
        ins_log.read_log('info', "pocsuite plugin parser failed: %s" % e)
        sys.exit(0)


if __name__ == '__main__':
    databases_init()
