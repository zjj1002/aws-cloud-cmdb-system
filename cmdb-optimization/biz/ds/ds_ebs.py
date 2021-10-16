# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

import fire
from libs.aws.com_ebs import ComplianceEbsApi
from models.ebs import DB
from libs.web_logs import ins_log
from libs.aws.session import get_aws_session
from opssdk.operate import MyCryptV2
from libs.db_context import DBContext, KEYDBContext
from models.key import KEY, model_to_dict


def sync_cmdb(api,account_id,region):
    """
    将ebs信息入库
    :return:
    """
    ebs_list = api.main()

    with DBContext('w') as session:
        # 清除数据库数据
        try:
            session.query(DB).filter(DB.account_id==account_id,DB.region==region).delete()
            session.commit()
        except:
            session.rollback()
        # 写入新数据
        for rds in ebs_list:
            ins_log.read_log('info', 'ebs信息：{}'.format(rds))
            new_db = DB(Attachments=rds.get('Attachments'),
                        AvailabilityZone=rds.get('AvailabilityZone', ),
                        CreateTime=rds.get('CreateTime'),
                        Encrypted=rds.get('Encrypted'),
                        Size=rds.get('Size'),
                        SnapshotId=rds.get('SnapshotId'),
                        State=rds.get('State'),
                        VolumeId=rds.get('VolumeId'),
                        Iops=rds.get('Iops'),
                        VolumeType=rds.get('VolumeType'),
                        Snapshot_overtime=rds.get('Snapshot_overtime'),
                        update_time=rds.get('update_time'),
                        account_id=account_id,
                        region=region,
                        )
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'ebs写入数据库共{}条'.format(len(ebs_list)))


def get_configs():
    """
    get id / key / region info
    :return:
    """

    aws_configs_list = []
    with KEYDBContext() as session:
        aws_configs_info = session.query(KEY).filter(KEY.account == 'AWS',
                                                              KEY.state == 'true').all()
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
        aws_session_token = config.get('aws_session_token')
        account_id = config.get('account_id')
        config = {
            "region_name": region,
            "aws_access_key_id": access_id,
            "aws_secret_access_key": access_key,
            "profile_name": None,
            "aws_session_token": aws_session_token}
        session = get_aws_session(config)
        rds_api = ComplianceEbsApi(session)
        sync_cmdb(rds_api,account_id,region)


if __name__ == '__main__':
    fire.Fire(main)
