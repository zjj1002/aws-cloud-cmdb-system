# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.iam import DB, model_to_dict
from websdk.db_context import DBContext
from biz.ds.ds_iam import main as  aws_iam_refresh


class GetIamHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        button = int(self.get_argument('button', default='0', strip=True))
        if button == 1:
            aws_iam_refresh()
        iam_list = []
        with DBContext('w') as session:
            if key:
                iam_info = session.query(DB).filter(
                    or_(DB.user_id.like('%{}%'.format(key)),
                        DB.user_name.like('%{}%'.format(key)),
                        DB.arn.like('%{}%'.format(key)),

                        )
                ).filter(or_(DB.is_90_signin == False,
                             DB.is_2_keys == False, )
                         ).all()

            else:
                iam_info = session.query(DB).filter(
                    or_(DB.is_90_signin == False,
                        DB.is_2_keys == False, )
                ).all()

        for data in iam_info:
            data_dict = model_to_dict(data)
            data_dict.pop("update_time")
            iam_list.append(data_dict)
        return iam_list


aws_iam_urls = [
    (r"/v1/cmdb/iam/", GetIamHandler),
]
