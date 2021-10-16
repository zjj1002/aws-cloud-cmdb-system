#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-20-26
# @Author : liuchuanhao
# @Site :
# @File : rds_ri.py
# @Software: PyCharm
from datetime import datetime

import fire

from libs.common import  get_rds_instance_type_info
from libs.web_logs import ins_log
from libs.aws.session import get_aws_session
from settings import settings
from libs.db_context import DBContext
from models.rds_ri_db import RiRds as DB, AWSRdsRiUsageReport


class RiRdsApi():
    def __init__(self, session):

        self.rds_ri_list = []
        # 获取rds的client
        self.rds_client = session.client('rds')

    def get_describe_reserved_db_instances_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.rds_client.describe_reserved_db_instances()

        except Exception as e:
            err = e
        return response_data, err

    def get_describe_db_instances_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.rds_client.describe_db_instances()

        except Exception as e:
            err = e
        return response_data, err

    def update_rds_ri_usage(self):
        rds_ri, _ = self.get_describe_reserved_db_instances_response()
        rds, _ = self.get_describe_db_instances_response()
        rds_ri_list = rds_ri['ReservedDBInstances']
        rds_list = rds['DBInstances']
        print(rds_ri_list)
        print(rds_list)
        ri_usage_data = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        b = []
        for r in rds_list:
            b.append(r["DBInstanceClass"].split(".")[1] + r["Engine"])
            print(r["DBInstanceClass"], r["Engine"],r['MultiAZ'])
            if r['DBInstanceStatus'] != 'available':
                continue
            dbclass, dbsize, num = get_rds_instance_type_info(r["DBInstanceClass"],r['MultiAZ'])
            ru = AWSRdsRiUsageReport(dbclass=dbclass,
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
        for ri in rds_ri_list:
            a.append(ri["DBInstanceClass"].split(".")[1]+ri['ProductDescription'])
            print(ri["DBInstanceClass"], ri['ProductDescription'], ri['DBInstanceCount'])
            dbclass, dbsize, num = get_rds_instance_type_info(ri["DBInstanceClass"],ri['MultiAZ'])
            if ri['State'] != 'active':
                continue
            if ri['ProductDescription'] == 'postgresql':
                dbengine = "postgres"
            elif ri['ProductDescription'] == 'oracle-ee(byol)':
                dbengine = "oracle-ee"
            else:
                dbengine = ri['ProductDescription']
            ru = AWSRdsRiUsageReport(dbclass=dbclass,
                                     dbsize=dbsize,
                                     dbengine=dbengine,
                                     total_ri=num * ri['DBInstanceCount'],
                                     date=today,
                                     total_running=0)

            for i in range(len(ri_usage_data)):
                if ri_usage_data[i].merge(ru):
                    break
            else:
                ri_usage_data.append(ru)
        print("__")

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
        response_data = self.rds_client.describe_reserved_db_instances()

        return response_data

def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    rds_api = RiRdsApi(session)
    rds_api.update_rds_ri_usage()


if __name__ == '__main__':
    fire.Fire(main)
