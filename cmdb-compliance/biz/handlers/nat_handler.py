# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : nat_handler.py
# @Role    :


from tornado.web import RequestHandler
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.nat import DB, model_to_dict
from websdk.db_context import DBContext
from biz.ds.ds_nat import main as  aws_nat_refresh


class GetNatHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        button = int(self.get_argument('button', default='0', strip=True))
        if button == 1:
            aws_nat_refresh()
        nat_list = []
        with DBContext('w') as session:
            if key:
                nat_info = session.query(DB).filter(
                    or_(DB.natgatewayid.like('%{}%'.format(key)),
                        DB.state.like('%{}%'.format(key)),
                        DB.subnetId.like('%{}%'.format(key)),
                        DB.vpcid.like('%{}%'.format(key)),
                        )
                ).filter(or_(DB.is_use == False, )
                         ).all()

            else:
                nat_info = session.query(DB).filter(
                    or_(DB.is_use == False, )
                ).all()

        for data in nat_info:
            data_dict = model_to_dict(data)
            data_dict.pop("update_time")
            data_dict.pop("createTime")
            nat_list.append(data_dict)
        return nat_list


aws_nat_urls = [
    (r"/v1/cmdb/natgateway/", GetNatHandler),
]
