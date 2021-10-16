#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-09-28
# @Author : liuchuanhao
# @Site :
# @File : elasticeache_ri.py
# @Software: PyCharm


import fire
from libs.web_logs import ins_log
from libs.aws.session import get_aws_session
from settings import settings
from libs.db_context import DBContext
from models.elasticache_ri_db import RiElastiCache as DB


class RiElastiCacheApi():
    def __init__(self, session):

        self.elasticache_ri_list = []
        # 获取elasticeache的client
        self.client = session.client('elasticache')

    def get_describe_reserved_cache_nodes_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.client.describe_reserved_cache_nodes()

        except Exception as e:
            err = e
        return response_data, err

    def get_describe_reserved_cache_nodes_data(self):
        """
        获取返回值
        :return:
        """
        response_data, err = self.get_describe_reserved_cache_nodes_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False
        for each in response_data['ReservedCacheNodes']:
            data = {}
            data['ReservedCacheNodeId'] = each.get('ReservedCacheNodeId')
            data['ReservedCacheNodesOfferingId'] = each.get('ReservedCacheNodesOfferingId')
            data['CacheNodeType'] = each.get('CacheNodeType')
            data['Duration'] = each.get('Duration')
            data['FixedPrice'] = each.get('FixedPrice')
            data['UsagePrice'] = each.get('UsagePrice')
            data['CacheNodeCount'] = each.get('CacheNodeCount')
            data['ProductDescription'] = each.get('ProductDescription')
            data['OfferingType'] = each.get('OfferingType')
            data['State'] = each.get('State')
            data['RecurringCharges'] = str(each.get('RecurringCharges'))
            self.elasticache_ri_list.append(data)
        return self.elasticache_ri_list


    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.client.describe_reserved_cache_nodes()

        return response_data


    def sync_cmdb(self):
        """
        将elasticeache信息入库
        :return:
        """
        elasticahce_list = self.get_describe_reserved_cache_nodes_data()

        if not elasticahce_list:
            ins_log.read_log('error', 'Not Fount elasticeache info...')
            return False

        with DBContext('w') as session:
            # 清除数据库数据
            try:
                session.query(DB).delete()
                session.commit()
            except:
                session.rollback()
            # 写入新数据
            for elasticeache in elasticahce_list:
                ins_log.read_log('info', 'RI_elasticeache信息：{}'.format(elasticeache))
                new_db = DB(ReservedCacheNodeId=elasticeache.get('ReservedCacheNodeId'),
                            ReservedCacheNodesOfferingId=elasticeache.get('ReservedCacheNodesOfferingId', ""),
                            CacheNodeType=elasticeache.get('CacheNodeType'),
                            Duration=elasticeache.get('Duration'),
                            FixedPrice=elasticeache.get('FixedPrice'),
                            UsagePrice=elasticeache.get('UsagePrice'),
                            CacheNodeCount=elasticeache.get("CacheNodeCount"),
                            ProductDescription=elasticeache.get('ProductDescription'),
                            OfferingType=elasticeache.get('OfferingType'),
                            State=elasticeache.get('State'),
                            RecurringCharges=elasticeache.get('RecurringCharges'),
                            )
                session.add(new_db)
            session.commit()
            ins_log.read_log('info', 'elasticache_ri写入数据库共{}条'.format(len(elasticeache)))


def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    elasticache_api = RiElastiCacheApi(session)
    elasticache_api.sync_cmdb()


if __name__ == '__main__':
    fire.Fire(main)
