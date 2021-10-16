#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/13 16:35
# @Author  : Fred Yangxiaofei
# @File    : ec2.py
# @Role    : 获取AWS Ec2信息推送到cmdb


import boto3
import re
from libs.db_context import DBContext
from models.server import Server, ServerDetail, AssetConfigs, model_to_dict,Tag
from opssdk.operate import MyCryptV2
from libs.web_logs import ins_log
from libs.aws.ec2 import Ec2Api
from itertools import chain
from copy import deepcopy


class ForDangersHandler(Ec2Api):
    def get_server_info(self):

        response = self.get_response()
        if not response:
            ins_log.read_log('error', 'Not fount response, please check your access_id and access_key...')
            # print('[Error]: Not fount response, please check your access_id and access_key...')
            return False

        ret = response['Reservations']
        server_list = []
        if ret:
            for r in ret:
                for i in r['Instances']:
                    asset_data = dict()
                    for tag in i.get("Tags"):
                        if tag["Key"] == "project":
                            asset_data['server_Project'] = tag["Value"]
                        elif tag["Key"] == "Name":
                            asset_data['server_name'] = tag["Value"]
                    asset_data['server_instance_id'] = i.get('InstanceId', 'Null')
                    asset_data['server_private_ip'] = i.get('PrivateIpAddress', 'Null')
                    asset_data['server_public_ip'] = i.get('PublicIpAddress', 'Null')  # 没有公网就给私网IP
                    asset_data['security_group'] = i.get('SecurityGroups', 'Null')
                    asset_data['risk_port'] = []
                    asset_data['server_mark'] = ''
                    asset_data['security_state'] = ''
                    # print(asset_data)
                    server_list.append(asset_data)

        return server_list
    
    def get_tags(self):
        result = []
        self.client = boto3.client('resourcegroupstaggingapi', region_name=self.region, aws_access_key_id=self.access_id,
                                   aws_secret_access_key=self.access_key)
        try:
            paginator = self.client.get_paginator('get_resources')
            tag_mapping = chain.from_iterable(page['ResourceTagMappingList'] for page in paginator.paginate())
            for resource in tag_mapping:
                tags_collection = {}
                tags_collection.clear()
                tags_collection['tag_aws_service'] = resource['ResourceARN'].split(':')[2]
                tags_collection['tag_description'] = resource['ResourceARN'].split(':')[5:]
                tags_collection['tag_description'] = ":".join(tags_collection['tag_description'])###字符串格式入库
                for pairs in resource['Tags']:
                    tags_dict = deepcopy(tags_collection)
                    tags_dict['tag_name'] = pairs['Key']
                    tags_dict['tag_value'] = pairs['Value']
                    result.append(tags_dict)
            print(len(result))
            return result
        except Exception as e:
            ins_log.read_log('error', e)
            # print(e)
            return False
        

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response = self.client.describe_instances()
        return response


def get_configs():
    """
    get id / key / region info
    :return:
    """

    aws_configs_list = []
    with DBContext('r') as session:
        aws_configs_info = session.query(AssetConfigs).filter(AssetConfigs.account == 'AWS',
                                                              AssetConfigs.state == 'true').all()
        for data in aws_configs_info:
            data_dict = model_to_dict(data)
            data_dict['create_time'] = str(data_dict['create_time'])
            data_dict['update_time'] = str(data_dict['update_time'])
            aws_configs_list.append(data_dict)
    return aws_configs_list

def main():
    mc = MyCryptV2()
    aws_configs_list = get_configs()
    if not aws_configs_list:
        ins_log.write_log('error', '没有获取到AWS资产配置信息，跳过')
        return False
    for config in aws_configs_list:
        access_id = config.get('access_id')
        access_key = mc.my_decrypt(config.get('access_key'))  # 解密后使用
        region = config.get('region')
        default_admin_user = config.get('default_admin_user')

        obj = ForDangersHandler(access_id, access_key, region, default_admin_user)
        result = [i for i in obj.get_tags()] 
    with DBContext('w', None) as session:
        session.execute( '''TRUNCATE TABLE asset_tag''' )
        session.bulk_insert_mappings(Tag,result)  
        session.commit() 



