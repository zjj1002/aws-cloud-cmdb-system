# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from pocsuite3.api import init_pocsuite
from pocsuite3.api import start_pocsuite
from pocsuite3.api import get_results


def pocsuite_scanner(_poc_config):
    init_pocsuite(_poc_config)
    start_pocsuite()
    result = get_results()
    return result

if __name__ == '__main__':
    config = {
        # 'url': 'https://www.baidu.com/',
        'url': 'https://cmdb.jncapp.com:8443',
        # 'poc': os.path.join(paths.POCSUITE_ROOT_PATH, "../tests/login_demo.py"),
        # 'poc': "G:\code_test\pro\procs\login_demo1.py",
        'poc': "G:\project\cmdb-compliance\pocsuite\procs\hikvision-2013-4976_web_login-bypass.py",
        # 'poc': login_demo,
        'username': "asd",
        'password': 'asdss',
        'verbose': 0
    }
    pocsuite_scanner(config)
