import fire
from libs.aws.com_elb import ComplianceELBApi
from models.elb import ElbDB
from libs.web_logs import ins_log
from libs.db_context import DBContext
from libs.aws.session import get_aws_session
from settings import settings


def sync_cmdb(api):
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
            session.query(ElbDB).delete()
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
                           is_encry_trans=rds.get('is_encry_trans'))
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'elb写入数据库共{}条'.format(len(elb_list)))


def main():
    """
    从接口获取配置
    :return:
    """
    session = get_aws_session(**settings.get("aws_key"))
    elb_api = ComplianceELBApi(session)
    sync_cmdb(elb_api)


if __name__ == '__main__':
    fire.Fire(main)
