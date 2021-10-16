import fire
from libs.aws.com_elb import ComplianceELBApi
from models.elb import ElbDB
from libs.web_logs import ins_log
from libs.aws.session import get_aws_session
from opssdk.operate import MyCryptV2
from libs.db_context import DBContext, KEYDBContext
from models.key import KEY, model_to_dict


def sync_cmdb(api,account_id,region):
    """
    将elb信息入库
    :return:
    """
    elb_list = api.main()

    if not elb_list:
        ins_log.read_log('error', 'Not Fount elb info...')
        return False
    with DBContext('w') as session:
        # 清除数据库数据
        try:
            session.query(ElbDB).filter(ElbDB.account_id==account_id,ElbDB.region==region).delete()
            session.commit()
        except:
            session.rollback()
        # 写入新数据
        for rds in elb_list:
            ins_log.read_log('info', 'elb信息：{}'.format(rds))
            new_db = ElbDB(name=rds.get('name'),
                           dnsname=rds.get('dnsname', ),
                           region=rds.get('region'),
                           vpcid=rds.get('vpcid'),
                           scheme=rds.get('scheme'),
                           is_use=rds.get('is_use'),
                           type=rds.get("type"),
                           is_encry_trans=rds.get('is_encry_trans'),
                           account_id=account_id,
                           )
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'elb写入数据库共{}条'.format(len(elb_list)))


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
        rds_api = ComplianceELBApi(session)
        sync_cmdb(rds_api,account_id,region)


if __name__ == '__main__':
    fire.Fire(main)
