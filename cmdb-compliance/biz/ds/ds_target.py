import fire

from libs.aws.com_elb import ComplianceTargetGroupsApi
from models.elb import TargetGroupDB
from libs.web_logs import ins_log
from libs.db_context import DBContext
from libs.aws.session import get_aws_session
from settings import settings


def sync_cmdb(api):
    """
    将target信息入库
    :return:
    """
    elb_list = api.main()

    if not elb_list:
        ins_log.read_log('error', 'Not Fount target info...')
        return False
    with DBContext('w') as session:
        # 清除数据库数据
        try:
            session.query(TargetGroupDB).delete()
            session.commit()
        except:
            session.rollback()
        # 写入新数据
        for rds in elb_list:
            ins_log.read_log('info', 'target信息：{}'.format(rds))
            new_db = TargetGroupDB(target_group_name=rds.get('target_group_name'),
                                   target_group_arn=rds.get('target_group_arn', ),
                                   protocol=rds.get('protocol'),
                                   port=rds.get('port'),
                                   vpc_id=rds.get('vpc_id'),
                                   is_use=rds.get('is_use'),
                                   target_type=rds.get("target_type"), )
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'target写入数据库共{}条'.format(len(elb_list)))


def main():
    """
    从接口获取配置
    :return:
    """
    session = get_aws_session(**settings.get("aws_key"))
    target_api = ComplianceTargetGroupsApi(session)
    sync_cmdb(target_api)


if __name__ == '__main__':
    fire.Fire(main)
