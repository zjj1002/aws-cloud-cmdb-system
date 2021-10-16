#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/24
# @Author  : Fred liuchunhao
# @File    : asset_elasticsearch_handler.py
# @Role    : es管理


from sqlalchemy import or_
from libs.base_handler import BaseHandler
from libs.common import data_sort

from models.elasticsearch import ElasticSearch ,model_to_dict
from websdk.db_context import DBContext
from tornado.web import RequestHandler
from libs.aws.elasticsearch import main


class ElasticSearchHandler(BaseHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        pageNum = int(self.get_argument('page', default='1', strip=True))
        pageSize = int(self.get_argument('limit', default='10', strip=True))
        with DBContext('r') as session:
            if key:
                ElasticSearch_data = session.query(ElasticSearch).filter(
                    or_(ElasticSearch.domain_id.like('%{}%'.format(key)),
                        ElasticSearch.domain_name.like('%{}%'.format(key)),
                        ElasticSearch.ARN.like('%{}%'.format(key)),
                        ElasticSearch.created.like('%{}%'.format(key)),
                        ElasticSearch.deleted.like('%{}%'.format(key)),
                        ElasticSearch.vpc.like('%{}%'.format(key)),
                        ElasticSearch.processing.like('%{}%'.format(key)),
                        ElasticSearch.version.like('%{}%'.format(key)),
                        ElasticSearch.instance_count.like('%{}%'.format(key)),
                        ElasticSearch.instance_type.like('%{}%'.format(key)),
                        ElasticSearch.dedicated_master_enabled.like('%{}%'.format(key)),
                        ElasticSearch.zone_awareness_enabled.like('%{}%'.format(key)),
                        ElasticSearch.volume_type.like('%{}%'.format(key)),
                        ElasticSearch.access_policies.like('%{}%'.format(key)),
                        ElasticSearch.automated_snapshot_start_hour.like('%{}%'.format(key)),
                        ElasticSearch.subnetids.like('%{}%'.format(key)),
                        ElasticSearch.availability_zones.like('%{}%'.format(key)),
                        ElasticSearch.security_group_ids.like('%{}%'.format(key)),
                        ElasticSearch.encryption_at_rest_options.like('%{}%'.format(key)),
                        ElasticSearch.tag_list.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                ElasticSearch_data = session.query(ElasticSearch).all()
            data_dict=list()
            for msg in ElasticSearch_data:
                msg = model_to_dict(msg)
                data_dict.append(msg)
            data_dict = data_sort(data_dict, "domain_name")
            ElasticSearch_data_list_re = data_dict[(pageNum - 1) * pageSize:pageNum * pageSize]
        self.write(dict(code=0, msg='获取成功', count=len(data_dict), data=ElasticSearch_data_list_re))

class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        main()
        return "测试中"

asset_elasticsearch_urls = [
    (r"/v1/cmdb/elasticsearch/", ElasticSearchHandler),
    (r"/v1/cmdb/elasticsearch/test/", ApiTest),
]

if __name__ == "__main__":
    pass
