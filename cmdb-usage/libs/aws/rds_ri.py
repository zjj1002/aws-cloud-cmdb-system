#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-09-28
# @Author : liuchuanhao
# @Site :
# @File : rds_ri.py
# @Software: PyCharm


import fire
from libs.web_logs import ins_log
from libs.aws.session import get_aws_session
from settings import settings
from libs.db_context import DBContext
from models.rds_ri_db import RiRds as DB

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


    def get_describe_reserved_db_data(self):
        """
        获取返回值
        :return:
        """
        response_data, err = self.get_describe_reserved_db_instances_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False
        for each in response_data['ReservedDBInstances']:
            rds_data = {}
            rds_data['ReservedDBInstanceId'] = each.get('ReservedDBInstanceId')
            rds_data['ReservedDBInstancesOfferingId'] = each.get('ReservedDBInstancesOfferingId')
            rds_data['DBInstanceClass'] = each.get('DBInstanceClass')
            rds_data['Duration'] = each.get('Duration')
            rds_data['FixedPrice'] = each.get('FixedPrice')
            rds_data['UsagePrice'] = each.get('UsagePrice')
            rds_data['CurrencyCode'] = each.get('CurrencyCode')
            rds_data['DBInstanceCount'] = each.get('DBInstanceCount')
            rds_data['ProductDescription'] = each.get('ProductDescription')
            rds_data['OfferingType'] = each.get('OfferingType')
            rds_data['MultiAZ'] = each.get('MultiAZ')
            rds_data['State'] = each.get('State')
            rds_data['RecurringCharges'] = str(each.get('RecurringCharges'))
            rds_data['ReservedDBInstanceArn'] = each.get('ReservedDBInstanceArn')
            self.rds_ri_list.append(rds_data)
        return self.rds_ri_list



    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.rds_client.describe_reserved_db_instances()

        return response_data

    def sync_cmdb(self):
        """
        将RDS信息入库
        :return:
        """
        rds_list = self.get_describe_reserved_db_data()

        if not rds_list:
            ins_log.read_log('error', 'Not Fount rds info...')
            return False

        with DBContext('w') as session:
            # 清除数据库数据
            try:
                session.query(DB).delete()
                session.commit()
            except:
                session.rollback()
            # 写入新数据
            for rds in rds_list:
                ins_log.read_log('info', 'RI_RDS信息：{}'.format(rds))
                new_db = DB(ReservedDBInstanceId=rds.get('ReservedDBInstanceId'),
                            ReservedDBInstancesOfferingId=rds.get('ReservedDBInstancesOfferingId', ""),
                            DBInstanceClass=rds.get('DBInstanceClass'),
                            Duration=rds.get('Duration'),
                            FixedPrice=rds.get('FixedPrice'),
                            UsagePrice=rds.get('UsagePrice'),
                            CurrencyCode=rds.get("CurrencyCode"),
                            DBInstanceCount=rds.get('DBInstanceCount'),
                            ProductDescription=rds.get('ProductDescription'),
                            OfferingType=rds.get('OfferingType'),
                            MultiAZ=rds.get('MultiAZ'),
                            State=rds.get('State'),
                            RecurringCharges=rds.get('RecurringCharges'),
                            ReservedDBInstanceArn=rds.get('ReservedDBInstanceArn'),
                            )
                session.add(new_db)
            session.commit()
            ins_log.read_log('info', 'RI_RDS写入数据库共{}条'.format(len(rds_list)))


def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    rds_api = RiRdsApi(session)
    rds_api.sync_cmdb()


if __name__ == '__main__':
    fire.Fire(main)