# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from tornado.web import RequestHandler
from gitsecrets.main import daily_scan_task
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.git_secrets import GitProject, model_to_dict, GitScanResult
from websdk.db_context import DBContext


class GetGitProject(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        git_project_list = []
        with DBContext('w') as session:
            if key:
                git_project_info = session.query(GitProject).filter(
                    or_(GitProject.name.like('%{}%'.format(key)),
                        GitProject.branch.like('%{}%'.format(key)),
                        GitProject.project_team.like('%{}%'.format(key)),
                        GitProject.source.like('%{}%'.format(key)),
                        GitProject.path.like('%{}%'.format(key)),
                        GitProject.last_scan_time.like('%{}%'.format(key)),
                        GitProject.add_date.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                git_project_info = session.query(GitProject).all()
        for data in git_project_info:
            data_dict = model_to_dict(data)
            git_project_list.append(data_dict)
            # 返回数据
        return git_project_list


class GetGitScanResult(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        git_result_list = []
        with DBContext('w') as session:
            if key:
                git_result_info = session.query(GitScanResult).filter(
                    or_(GitScanResult.name.like('%{}%'.format(key)),
                        GitScanResult.branch.like('%{}%'.format(key)),
                        GitScanResult.project_team.like('%{}%'.format(key)),
                        GitScanResult.source.like('%{}%'.format(key)),
                        GitScanResult.risk_index.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                git_result_info = session.query(GitScanResult).all()
        for data in git_result_info:
            data_dict = model_to_dict(data)
            git_result_list.append(data_dict)
            # 返回数据
        return git_result_list

#测试用 后续会删除---lch
class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        daily_scan_task()
        return "测试中"


aws_code_scan_urls = [
    (r"/v1/cmdb/code_scan/project/", GetGitProject),
    (r"/v1/cmdb/code_scan/scan_result/", GetGitScanResult),
    (r"/v1/cmdb/gittest/", ApiTest),
]
