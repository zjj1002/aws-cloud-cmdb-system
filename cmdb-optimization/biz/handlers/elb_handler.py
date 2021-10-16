# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : elb_hanlder.py
# @Role    :


from tornado.web import RequestHandler
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.elb import ElbDB, model_to_dict
from websdk.db_context import DBContext
from biz.ds.ds_elb import main as aws_elb_refresh


class GetElbHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        button = int(self.get_argument('button', default='0', strip=True))
        if button == 1:
            aws_elb_refresh()
        elb_list = []
        with DBContext('w') as session:
            if key:
                elb_info = session.query(ElbDB).filter(
                    or_(ElbDB.name.like('%{}%'.format(key)),
                        ElbDB.dnsname.like('%{}%'.format(key)),
                        ElbDB.region.like('%{}%'.format(key)),
                        ElbDB.vpcid.like('%{}%'.format(key)),
                        ElbDB.scheme.like('%{}%'.format(key)),
                        ElbDB.type.like('%{}%'.format(key)),
                        )
                ).filter(or_(ElbDB.is_encry_trans == False,
                             ElbDB.is_use == False,
                             )
                         ).all()

            else:
                elb_info = session.query(ElbDB).filter(
                    or_(ElbDB.is_encry_trans == False,
                        ElbDB.is_use == False, )
                ).all()

        for data in elb_info:
            data_dict = model_to_dict(data)
            data_dict.pop("update_time")
            elb_list.append(data_dict)
        return elb_list


aws_elb_urls = [
    (r"/v1/cmdb/elb/", GetElbHandler),
]
