
# -*- coding: utf-8 -*-
# @Time    : 2020/9/10
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :


from tornado.web import RequestHandler

from kube_bench.main import kube_daily_scan
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.kube_bench import KUBECONFIG, model_to_dict, BENCHDB
from websdk.db_context import DBContext


class GetkubeBenchconfig(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        config_project_list = []
        with DBContext('w') as session:
            if key:
                git_project_info = session.query(KUBECONFIG).filter(
                    or_(KUBECONFIG.kube_config_name.like('%{}%'.format(key)),
                        KUBECONFIG.server.like('%{}%'.format(key)),
                        KUBECONFIG.current_context.like('%{}%'.format(key)),
                        KUBECONFIG.date.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                git_project_info = session.query(KUBECONFIG).all()
        for data in git_project_info:
            data_dict = model_to_dict(data)
            config_project_list.append(data_dict)
            # 返回数据
        return config_project_list


class GetKubeBenchScanResult(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        config_name = self.get_argument('config_name', default="config.a", strip=True)
        mastr_or_node = self.get_argument('mastr_or_node', default="master", strip=True)
        with DBContext('w') as session:
            kube_config_info = session.query(KUBECONFIG).first()
            if kube_config_info:
                kube_config_info = model_to_dict(kube_config_info)
            else:
                return []
        if config_name == "":
            config_name=kube_config_info["kube_config_name"]
        scan_result_list = []
        with DBContext('w') as session:
            result_data = session.query(BENCHDB) \
                .filter(BENCHDB.config_name ==config_name,BENCHDB.mastr_or_node ==mastr_or_node).all()
        for data in result_data:
            data_dict = model_to_dict(data)
            scan_result_list.append(data_dict)
            # 返回数据
        return scan_result_list

class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        kube_daily_scan()
        return "测试中"

aws_kube_scan_urls = [
    (r"/v1/cmdb/kube_config/", GetkubeBenchconfig),
    (r"/v1/cmdb/kube_scan_result/", GetKubeBenchScanResult),
    (r"/v1/cmdb/kubeapitest/", ApiTest),
]


