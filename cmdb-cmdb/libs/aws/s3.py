#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 16:35
# @Author  : liang
# @File    : s3.py
# @Role    : 获取AWS S3信息推送到cmdb
import math

import boto3
import re
from libs.db_context import DBContext
from models.server import AssetConfigs, model_to_dict
from models.s3 import *
from opssdk.operate import MyCryptV2
from libs.web_logs import ins_log
import fire
from datetime import timedelta


class S3Api():
    def __init__(self, access_id = '', access_key = '', region = 'cn-northwest-1'):
        self.access_id = access_id
        self.access_key = access_key
        self.region = region
        self.client = boto3.client('s3', region_name=self.region, aws_access_key_id=self.access_id,
                                   aws_secret_access_key=self.access_key)
        self.cloudwatch_client = boto3.client('cloudwatch', region_name=self.region, aws_access_key_id=self.access_id,
                                   aws_secret_access_key=self.access_key)

    def get_bucket_acl_status(self,bucket):
        response = self.client.get_bucket_acl(Bucket=bucket)
        public_status = 0
        grant_list = response["Grants"]

        for grant in grant_list:
            public_access_group_uri = "http://acs.amazonaws.com/groups/global/AllUsers"

            if public_access_group_uri == grant["Grantee"].get("URI",0):
                public_status = 1
                break
        return public_status

    def get_bucket_tags(self,bucket):
        try:
            response = self.client.get_bucket_tagging(Bucket=bucket)
        except Exception as e:
            print(e)
            response = dict()

        tag_list = response.get("TagSet","Null")

        return tag_list

    def get_bucket_lifecycle_status(self,bucket):
        try:
            response = self.client.get_bucket_lifecycle(Bucket=bucket)
        except Exception as e:
            print(e)
            response = dict()

        lifecycle_status = 0
        rules = response.get("Rules",0)

        if rules:
            lifecycle_status = 1
        return lifecycle_status

    def get_bucket_info(self):
        try:
            response = self.client.list_buckets()
            print(response)
        except Exception as e:
            print(e)
            response = dict()
        # owner = response["Owner"]
        bucket_list = response.get("Buckets","")
        buckets_result = []

        if len(bucket_list)>= 1:
            for bucket in bucket_list:
                asset_data = dict()
                asset_data["Name"] = bucket.get("Name")
                asset_data["CreationDate"] = bucket.get("CreationDate")
                asset_data["Tags"] = self.get_bucket_tags(bucket.get("Name"))
                asset_data["Acl"] = self.get_bucket_acl_status(bucket.get("Name"))
                asset_data["LifeCycle"] = self.get_bucket_lifecycle_status(bucket.get("Name"))
                asset_data["size"] = self.get_bucket_size_by_cloudwatch(bucket.get("Name"))
                buckets_result.append(asset_data)
        else:
            print("Not fount S3 buckets info.......")

        return buckets_result

    def get_all_s3_objects(self, **base_kwargs):
        continuation_token = None
        while True:
            list_kwargs = dict(MaxKeys=1000, **base_kwargs)
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token
            response = self.client.list_objects_v2(**list_kwargs)
            yield from response.get('Contents', [])

            if not response.get('IsTruncated'):  # At the end of the list?
                break
            continuation_token = response.get('NextContinuationToken')


    def get_bucket_size(self,bucket):
        size = int()
        s3_object =  self.get_all_s3_objects(Bucket=bucket)
        for file in s3_object:
            size += file['Size']
        return size

    def get_bucket_size_by_cloudwatch(self,bucket):
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                                                                    Namespace='AWS/S3', MetricName='BucketSizeBytes',
                                                                    StartTime=datetime.utcnow() - timedelta(days=2),
                                                                    EndTime= datetime.utcnow(),
                                                                    Period=60 * 60 * 24 * 2,
                                                                    Statistics=['Average'], Unit='Bytes',
                                                                    Dimensions=[
                                                                        {'Name': 'BucketName', 'Value': bucket},
                                                                        {u'Name': 'StorageType', u'Value': 'StandardStorage'}
                                                                    ])
        except Exception as e:
            print(e)
            response ={}

        if response["Datapoints"]:
            return response.get("Datapoints")[0].get("Average")/math.pow(1024, 3)
        else:
            return 0

    def sync_cmdb(self):
        bucket_list = self.get_bucket_info()
        if not bucket_list:
            ins_log.read_log('info', 'Not fount S3 buckets info...')
            return False
        with DBContext('w') as session:
            # 清除数据库数据
            try:
                session.query(S3).delete()
                session.commit()
            except:
                session.rollback()
            for bucket in bucket_list:
                ins_log.read_log('info', 'S3 bucket 信息：{}'.format(bucket))
                bucket_name = bucket.get('Name')
                bucket_acl = bucket.get('Acl')
                bucket_lifecycle = bucket.get('LifeCycle')
                bucket_tags = str(bucket.get('Tags'))
                bucket_create_time = bucket.get('CreationDate')
                size = bucket.get('size')

                exist_bucket = session.query(S3).filter(S3.bucket_name == bucket_name).first()

                if exist_bucket:
                    session.query(S3).filter(S3.bucket_name == bucket_name).update({
                        S3.bucket_acl:bucket_acl,S3.bucket_lifecycle:bucket_lifecycle,S3.bucket_tags:bucket_tags,
                        S3.size:size
                    })
                else:
                    new_S3 = S3(bucket_name=bucket_name,bucket_acl=bucket_acl,bucket_tags=bucket_tags,
                                bucket_lifecycle=bucket_lifecycle,create_time=bucket_create_time,size=size)
                    session.add(new_S3)
            session.commit()


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
    """
    从接口获取已经启用的配置
    :return:
    """

    mc = MyCryptV2()
    aws_configs_list = get_configs()
    if not aws_configs_list:
        ins_log.read_log('error', '没有获取到AWS资产配置信息，跳过')
        return False
    for config in aws_configs_list:
        access_id = config.get('access_id')
        access_key = mc.my_decrypt(config.get('access_key'))  # 解密后使用
        region = config.get('region')
        default_admin_user = config.get('default_admin_user')

        obj = S3Api(access_id, access_key, region)
        obj.sync_cmdb()


if __name__ == '__main__':
    fire.Fire(main)
