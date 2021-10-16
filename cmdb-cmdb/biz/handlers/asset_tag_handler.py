#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 9:28
# @Author  : Fred Yangxiaofei
# @File    : asset_tag_handler.py
# @Role    : Tag


import json
from libs.base_handler import BaseHandler
from opssdk.operate import MyCryptV2
from sqlalchemy import or_
from models.server import Tag, TagRule, Server, ServerTag, model_to_dict
from tornado.web import RequestHandler, HTTPError
from models.db import DB, DBTag
from websdk.db_context import DBContext
from websdk.web_logs import ins_log
import tornado.web
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor



#class TAGHandler(BaseHandler):
class TAGHandler(RequestHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default="888", strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        tag_list = []

        with DBContext('r') as session:
            if key :
                all_tags = session.query(Tag).filter(or_(Tag.tag_name.like('%{}%'.format(key)),
                                                Tag.tag_name.like('%{}%'.format(key)),
                                                Tag.tag_value.like('%{}%'.format(key)),
                                                Tag.tag_description.like('%{}%'.format(key)),
                                                Tag.tag_aws_service.like('%{}%'.format(key)))).order_by(Tag.id).offset(limit_start).limit(int(limit))
                count = all_tags.count() 
            else:
                all_tags = session.query(Tag).order_by(Tag.id).offset(limit_start).limit(int(limit))
                count = all_tags.count()   
            for data in all_tags:
                data_dict = model_to_dict(data)      
                tag_list.append(data_dict)
        self.write(dict(code=0, msg='获取成功', count=count, data=tag_list))




tag_urls = [
    (r"/v1/cmdb/tag/", TAGHandler),
]
