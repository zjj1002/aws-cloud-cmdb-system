#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : elasticsearch.py
# @Author: Fred liuchuanhao
# @Date  : 2020/9/24
# @Role  : 获取AWS elasticsearch信息


import boto3
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.elasticsearch import ElasticSearch as DB
from models.server import AssetConfigs, model_to_dict
from opssdk.operate import MyCryptV2
import fire


class ElasticSearchApi():
    def __init__(self, access_id, access_key, region):
        self.idc = 'AWS'
        self.access_id = access_id
        self.access_key = access_key
        self.region = region
        self.client = self.conn()

    def conn(self):
        try:
            client = boto3.client('es', region_name=self.region, aws_access_key_id=self.access_id,
                                  aws_secret_access_key=self.access_key)
            return client
        except Exception as err:
            ins_log.read_log('error', 'Error:{err}'.format(err=err))
            return False

    def list_domain_names(self):
        """
        """
        try:
            response = self.client.list_domain_names()
            DomainNames = response.get('DomainNames')
            if not DomainNames: return []
            res = list(map(self.format_DomainNames, DomainNames))
            return res
        except Exception as err:
            ins_log.read_log('error', 'Error:{err}'.format(err=err))
            return []

    def format_DomainNames(self, DomainNames):
        """
        format memcached
        :return:
        """
        if not isinstance(DomainNames, dict):
            raise TypeError
        response = self.client.describe_elasticsearch_domains(DomainNames=[DomainNames["DomainName"]])

        DomainStatusList = response.get('DomainStatusList')[0]

        asset_data = dict()
        asset_data['domain_id'] = DomainStatusList.get('DomainId')
        asset_data['domain_name'] = DomainStatusList.get('DomainName')
        asset_data['ARN'] = DomainStatusList.get('ARN')
        response = self.client.list_tags(
            ARN= DomainStatusList.get('ARN'))
        asset_data['tag_list'] = str(response.get("TagList"))
        asset_data['created'] = DomainStatusList.get('Created')
        asset_data['deleted'] = DomainStatusList.get('Deleted')
        asset_data['vpc'] = DomainStatusList.get('Endpoints').get("vpc")
        asset_data['processing'] = DomainStatusList.get('Processing')
        asset_data['version'] = DomainStatusList.get('ElasticsearchVersion')
        asset_data['instance_type'] = DomainStatusList.get('ElasticsearchClusterConfig').get('InstanceType')
        asset_data['instance_count'] = DomainStatusList.get('ElasticsearchClusterConfig').get('InstanceCount')
        asset_data['dedicated_master_enabled'] = DomainStatusList.get('ElasticsearchClusterConfig').get(
            'DedicatedMasterEnabled')
        asset_data['zone_awareness_enabled'] = DomainStatusList.get('ElasticsearchClusterConfig').get(
            'ZoneAwarenessEnabled')
        asset_data['ebs_enabled'] = DomainStatusList.get('EBSOptions').get("EBSEnabled")
        asset_data['volume_type'] = DomainStatusList.get('EBSOptions').get("VolumeType")
        asset_data['volume_size'] = DomainStatusList.get('EBSOptions').get("VolumeSize")
        asset_data['access_policies'] = DomainStatusList.get('AccessPolicies')
        asset_data['automated_snapshot_start_hour'] = DomainStatusList.get('SnapshotOptions').get(
            "AutomatedSnapshotStartHour")
        asset_data['subnetids'] = ' '.join(DomainStatusList.get("VPCOptions").get('SubnetIds'))
        asset_data['availability_zones'] = ' '.join(DomainStatusList.get("VPCOptions").get("AvailabilityZones"))
        asset_data['security_group_ids'] = ' '.join(DomainStatusList.get("VPCOptions").get("SecurityGroupIds"))
        asset_data['encryption_at_rest_options'] = DomainStatusList.get("EncryptionAtRestOptions").get("Enabled")

        return asset_data

    def sync_cmdb(self):
        """
        入库
        :return:
        """

        domain_names_list = self.list_domain_names()
        if not domain_names_list:
            return False

        with DBContext('w') as session:
            for i in domain_names_list:
                ins_log.read_log('info', 'domain_names_list info：{}'.format(i))
                domain_id = i.get('domain_id')

                exist_redis = session.query(DB).filter(DB.domain_id == domain_id).first()

                if exist_redis:
                    session.query(DB).filter(DB.domain_id == domain_id).update({
                        DB.domain_name: i.get('domain_name'), DB.ARN: i.get('ARN'), DB.created: i.get('created'),
                        DB.deleted: i.get('deleted'), DB.vpc: i.get('vpc'),
                        DB.processing: i.get('processing'), DB.version: i.get('version'),
                        DB.instance_count: i.get('instance_count'), DB.instance_type: i.get('instance_type'),
                        DB.dedicated_master_enabled: i.get('dedicated_master_enabled'),
                        DB.zone_awareness_enabled: i.get('zone_awareness_enabled'),
                        DB.ebs_enabled: i.get('ebs_enabled'), DB.volume_type: i.get('volume_type'),
                        DB.volume_size: i.get('volume_size'), DB.access_policies: i.get('access_policies'),
                        DB.automated_snapshot_start_hour: i.get('automated_snapshot_start_hour'),
                        DB.subnetids: i.get('subnetids'),
                        DB.availability_zones: i.get('availability_zones'),
                        DB.security_group_ids: i.get('security_group_ids'),
                        DB.encryption_at_rest_options: i.get('encryption_at_rest_options'),
                        DB.tag_list: i.get('tag_list')
                    })
                else:
                    new_db = DB(domain_id=domain_id,
                                domain_name=i.get('domain_name'), ARN=i.get('ARN'),
                                created=i.get('created'), deleted=i.get('deleted'),
                                vpc=i.get('vpc'), processing=i.get('processing'),
                                version=i.get('version'), instance_count=i.get('instance_count'),
                                instance_type=i.get('instance_type'),
                                dedicated_master_enabled=i.get('dedicated_master_enabled'),
                                zone_awareness_enabled=i.get('zone_awareness_enabled'),
                                ebs_enabled=i.get('ebs_enabled'),
                                volume_type=i.get('volume_type'), volume_size=i.get('volume_size'),
                                access_policies=i.get('access_policies'),
                                automated_snapshot_start_hour=i.get('automated_snapshot_start_hour'),
                                subnetids=i.get('subnetids'), availability_zones=i.get('availability_zones'),
                                security_group_ids=i.get('security_group_ids'),
                                encryption_at_rest_options=i.get('encryption_at_rest_options'),
                                tag_list=i.get('tag_list'),
                                )
                    session.add(new_db)
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

        obj = ElasticSearchApi(access_id, access_key, region)
        obj.sync_cmdb()


if __name__ == '__main__':
    fire.Fire(main)
