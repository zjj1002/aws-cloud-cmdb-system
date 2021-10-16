# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

import fire
from libs.aws.com_ebs import ComplianceEbsApi
from models.ebs import DB
from libs.web_logs import ins_log
from libs.db_context import DBContext
from libs.aws.session import get_aws_session
from settings import settings


def sync_cmdb(api):
    """
    将ebs信息入库
    :return:
    """
    ebs_list = api.main()

    with DBContext('w') as session:
        # 清除数据库数据
        try:
            session.query(DB).delete()
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
                        )
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'ebs写入数据库共{}条'.format(len(ebs_list)))


def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    ebs_api = ComplianceEbsApi(session)
    sync_cmdb(ebs_api)


if __name__ == '__main__':
    fire.Fire(main)
