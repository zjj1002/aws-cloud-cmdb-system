# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

import fire
from libs.aws.com_iam import ComplianceIamApi
from models.iam import DB
from libs.web_logs import ins_log
from libs.db_context import DBContext
from libs.aws.session import get_aws_session
from settings import settings


def sync_cmdb(api):
    """
    将elb信息入库
    :return:
    """
    iam_list = api.main()

    with DBContext('w') as session:
        # 清除数据库数据
        try:
            session.query(DB).delete()
            session.commit()
        except:
            session.rollback()
        # 写入新数据
        for rds in iam_list:
            ins_log.read_log('info', 'iam信息：{}'.format(rds))
            new_db = DB(user_id=rds.get('user_id'),
                        user_name=rds.get('user_name', ),
                        arn=rds.get('arn'),
                        is_90_signin=rds.get('is_90_signin'),
                        is_2_keys=rds.get('is_2_keys'),
                        aksk_90_used=rds.get('aksk_90_used'))
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'iam写入数据库共{}条'.format(len(iam_list)))


def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    iam_api = ComplianceIamApi(session)
    sync_cmdb(iam_api)


if __name__ == '__main__':
    fire.Fire(main)
