import fire
from models.rds import DB
from libs.web_logs import ins_log
from libs.aws.com_rds import ComplianceRDSApi
from models.server import AssetConfigs, model_to_dict
from libs.db_context import DBContext
from libs.aws.session import get_aws_session
from settings import settings


def sync_cmdb(api):
    """
    将RDS信息入库
    :return:
    """
    rds_list = api.get_all_db_info()

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
            ins_log.read_log('info', 'RDS信息：{}'.format(rds))
            new_db = DB(db_public_access=rds.get('db_public_access'),
                        db_Identifier=rds.get('db_Identifier', ""),
                        db_host=rds.get('db_host'),
                        db_region=rds.get('db_region'),
                        db_conn=rds.get('db_conn'),
                        db_backup=rds.get('db_backup'),
                        db_backup_period=rds.get("db_backup_period"),
                        db_instance_id=rds.get('db_instance_id'))
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'RDS写入数据库共{}条'.format(len(rds_list)))

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
    aws_configs_list.append({"access_id":settings.AWS_ACCESS_KEY_ID,
                             "access_key":settings.AWS_SECRET_ACCESS_KEY,
                             "region":settings.AWS_DEFAULT_REGION})
    return aws_configs_list


def main():
    """
    从接口获取配置
    :return:
    """

    session = get_aws_session(**settings.get("aws_key"))
    rds_api = ComplianceRDSApi(session)
    sync_cmdb(rds_api)


if __name__ == '__main__':
    fire.Fire(main)
