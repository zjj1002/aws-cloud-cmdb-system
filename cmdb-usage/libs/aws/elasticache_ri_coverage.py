#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-20-28
# @Author : liuchuanhao
# @Site :
# @File :
# @Software: PyCharm


import fire
from libs.common import get_relasticache_instance_type_info
from libs.aws.session import get_aws_session
from models.elasticache_ri_db import AWSElastiCacheRiUsageReport
from settings import settings
from datetime import datetime
from libs.db_context import DBContext


class RiElastiCacheApi():
    def __init__(self, session):
        self.ec_ri_list = []
        # 获取elasticache的client
        self.ec_client = session.client('elasticache')

    def get_describe_reserved_cache_nodes_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.ec_client.describe_reserved_cache_nodes()

        except Exception as e:
            err = e
        return response_data, err

    def get_describe_cache_clusters_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.ec_client.describe_cache_clusters()

        except Exception as e:
            err = e
        return response_data, err

    def update_ec_ri_usage(self):
        ec_ri, _ = self.get_describe_reserved_cache_nodes_response()
        ec, _ = self.get_describe_cache_clusters_response()
        ec_ri_list = ec_ri['ReservedCacheNodes']
        ec_list = ec['CacheClusters']
        print(ec_ri_list)
        print(ec_list)
        ri_usage_data = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        b = []
        for r in ec_list:
            b.append(r['CacheNodeType'].split(".")[1] + r["Engine"])
            print(r['CacheNodeType'], r["Engine"],r['CacheClusterStatus'])
            if r['CacheClusterStatus'] != 'available':
                continue
            dbclass, dbsize, num = get_relasticache_instance_type_info(r["CacheNodeType"])
            ru = AWSElastiCacheRiUsageReport(dbclass=dbclass,
                                     dbsize=dbsize,
                                     dbengine=r["Engine"],
                                     total_ri=0,
                                     date=today,
                                     total_running=num)
            for i in range(len(ri_usage_data)):
                if ri_usage_data[i].merge(ru):
                    break
            else:
                ri_usage_data.append(ru)
        a = []
        for ri in ec_ri_list:
            a.append(ri['CacheNodeType'].split(".")[1]+ri['ProductDescription'])
            print(ri["CacheNodeType"], ri['ProductDescription'], ri['CacheNodeCount'])
            dbclass, dbsize, num = get_relasticache_instance_type_info(ri["CacheNodeType"])
            if ri['State'] != 'active':
                continue
            dbengine = ri['ProductDescription']
            ru = AWSElastiCacheRiUsageReport(dbclass=dbclass,
                                     dbsize=dbsize,
                                     dbengine=dbengine,
                                     total_ri=num * ri['CacheNodeCount'],
                                     date=today,
                                     total_running=0)

            for i in range(len(ri_usage_data)):
                if ri_usage_data[i].merge(ru):
                    break
            else:
                ri_usage_data.append(ru)

        with DBContext('w') as session:
            for rud in ri_usage_data:
                # 计算覆盖率
                rud.coverage_rate = rud.total_ri / rud.total_running if rud.total_running > 0 else -0.1
                session.add(rud)
            session.commit()

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        pass

def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    ec_api = RiElastiCacheApi(session)
    ec_api.update_ec_ri_usage()


if __name__ == '__main__':
    fire.Fire(main)
