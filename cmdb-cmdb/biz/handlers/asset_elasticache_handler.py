#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/24
# @Author  : Fred liuchuanhao
# @File    : asset_elasticache_handler.py
# @Role    : 缓存管理


import json
from sqlalchemy import or_

from libs.aws.elasticache import main
from libs.base_handler import BaseHandler
from libs.common import data_sort

from models.db import ElastiCache ,model_to_dict
from websdk.db_context import DBContext
from tornado.web import RequestHandler


class ElastiCacheHandler(BaseHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        pageNum = int(self.get_argument('page', default='1', strip=True))
        pageSize = int(self.get_argument('limit', default='10', strip=True))
        with DBContext('r') as session:
            if key:
                elasticache_data = session.query(ElastiCache).filter(
                    or_(ElastiCache.idc.like('%{}%'.format(key)),
                        ElastiCache.db_code.like('%{}%'.format(key)),
                        ElastiCache.db_class.like('%{}%'.format(key)),
                        ElastiCache.db_host.like('%{}%'.format(key)),
                        ElastiCache.db_port.like('%{}%'.format(key)),
                        ElastiCache.db_user.like('%{}%'.format(key)),
                        ElastiCache.db_region.like('%{}%'.format(key)),
                        ElastiCache.db_type.like('%{}%'.format(key)),
                        ElastiCache.db_version.like('%{}%'.format(key)),
                        ElastiCache.state.like('%{}%'.format(key)),
                        ElastiCache.db_detail.like('%{}%'.format(key)),
                        ElastiCache.tag_list.like('%{}%'.format(key)),
                        ElastiCache.db_node_num.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                elasticache_data = session.query(ElastiCache).all()
            data_dict=list()
            for msg in elasticache_data:
                msg = model_to_dict(msg)
                msg.pop("create_time")
                msg.pop("update_time")
                data_dict.append(msg)
            data_dict = data_sort(data_dict, "db_code")
            elasticache_list_re = data_dict[(pageNum - 1) * pageSize:pageNum * pageSize]
        self.write(dict(code=0, msg='获取成功', count=len(data_dict), data=elasticache_list_re))

class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        main()
        return "测试中"


asset_elasticache_urls = [
    (r"/v1/cmdb/elasticache/", ElastiCacheHandler),
    (r"/v1/cmdb/elasticache/test/", ApiTest),
]

if __name__ == "__main__":
    pass
