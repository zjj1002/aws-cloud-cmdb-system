# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from datetime import datetime

import shortuuid
from tornado.web import RequestHandler
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.pocsutie_db import Target, model_to_dict, PocsuiteTask, PocsuitePlugin, Result
from pocsuite.main import dayly_san_taks
from websdk.db_context import DBContext


class GetTargetHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        target_list = []
        with DBContext('w') as session:
            if key:
                elb_info = session.query(Target).filter(
                    or_(Target.url.like('%{}%'.format(key)),
                        Target.last_modifield.like('%{}%'.format(key)),
                        Target.vul_count.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                elb_info = session.query(Target).all()

        for data in elb_info:
            data_dict = model_to_dict(data)
            target_list.append(data_dict)
            # 返回数据
        return target_list

    def post(self, *args, **kwargs):
        url = self.get_body_argument("url", default=None, strip=True)
        with DBContext('w') as session:
            re = session.query(Target).filter(Target.url == url).all()
            if re:
                session.query(Target).filter(Target.url == url).update({
                    Target.id: "target_" + shortuuid.uuid(),
                    Target.url: url,
                    Target.last_modifield: str(datetime.now()),
                    Target.vul_count: 0
                })

            else:
                new_db = Target(
                    id="target_" + shortuuid.uuid(),
                    url=url,
                    last_modifield=str(datetime.now()),
                    vul_count=0, )
                session.add(new_db)
            session.commit()
        return self.write(dict(code=0,
                               msg='添加成功', ))

    def delete(self, *args, **kwargs):
        url = self.get_body_argument('url', default=None, strip=True)
        with DBContext('r') as session:
            session.query(Target).filter(Target.url == url).delete()
            session.commit()
        return self.write(dict(code=0,
                               msg='删除成功', ))


class GetPluginHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        plugin_list = []
        with DBContext('w') as session:
            if key:
                traget_group_info = session.query(PocsuitePlugin).filter(
                    or_(PocsuitePlugin.app.like('%{}%'.format(key)),
                        PocsuitePlugin.date.like('%{}%'.format(key)),
                        PocsuitePlugin.name.like('%{}%'.format(key)),
                        PocsuitePlugin.op.like('%{}%'.format(key)),
                        PocsuitePlugin.pid.like('%{}%'.format(key)),
                        PocsuitePlugin.type.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                traget_group_info = session.query(PocsuitePlugin).all()
        for data in traget_group_info:
            data_dict = model_to_dict(data)
            plugin_list.append(data_dict)
        return plugin_list


class GetTaskHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        task_list = []
        with DBContext('w') as session:
            if key:
                traget_group_info = session.query(PocsuiteTask).filter(
                    or_(PocsuiteTask.name.like('%{}%'.format(key)),
                        PocsuiteTask.target.like('%{}%'.format(key)),
                        PocsuiteTask.status.like('%{}%'.format(key)),
                        PocsuiteTask.vul_count.like('%{}%'.format(key)),
                        PocsuiteTask.vul_count.like('%{}%'.format(key)),
                        PocsuiteTask.op.like('%{}%'.format(key)),
                        )
                ).all()

            else:
                traget_group_info = session.query(PocsuiteTask).all()
        for data in traget_group_info:
            data_dict = model_to_dict(data)
            task_list.append(data_dict)
        return task_list

    #删除任务
    def delete(self, *args, **kwargs):
        task_id = self.get_body_argument('task_id', default=None, strip=True)
        with DBContext('r') as session:
            session.query(PocsuiteTask).filter(PocsuiteTask.id == task_id).delete()
            session.commit()
        return self.write(dict(code=0,
                               msg='删除成功', ))

    #添加任务
    def post(self, *args, **kwargs):
        name = self.get_body_argument("name",default="add_task_" + str(datetime.now())[:10],strip=True)
        target_list = self.get_body_arguments("target_list", strip=True)
        plugin_list = self.get_body_arguments("plugin_list",  strip=True)
        id = "task_" + shortuuid.uuid()
        with DBContext('w') as session:
            new_db = PocsuiteTask(id=id,
                                  target=','.join(target_list),
                                  poc=','.join(plugin_list),
                                  status="未扫描",
                                  name=name,
                                  date=str(datetime.now()),
                                  vul_count="0"
                                  )
            session.add(new_db)
            session.commit()
        return self.write(dict(msg='ok'))


class GetResultHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        task_id = self.get_argument('task_id', default=None, strip=True)
        with DBContext('w') as session:
            task_info = session.query(PocsuiteTask).filter(PocsuiteTask.status == "已扫描").first()
            if task_info:
                task_info = model_to_dict(task_info)
            else:
                return []
        if task_id == None:
            task_id = task_info["id"]
        scan_result_list = []
        with DBContext('w') as session:
            result_data = session.query(Result) \
                .filter(Result.tid == task_id).all()
        for data in result_data:
            data_dict = model_to_dict(data)
            scan_result_list.append(data_dict)
        return scan_result_list

    def post(self, *args, **kwargs):
        pass


#测试用 后续会删除---lch
class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        dayly_san_taks()
        return "测试中"


aws_poc_urls = [
    (r"/v1/cmdb/poc/target/", GetTargetHandler),
    (r"/v1/cmdb/poc/plugin/", GetPluginHandler),
    (r"/v1/cmdb/poc/task/", GetTaskHandler),
    (r"/v1/cmdb/poc/result/", GetResultHandler),
    (r"/v1/cmdb/poc/test/", ApiTest),
]
