import fire
from libs.aws.com_nat import ComplianceNatGateWayApi
from models.nat import DB
from libs.web_logs import ins_log
from libs.db_context import DBContext
from libs.aws.session import get_aws_session
from settings import settings


def sync_cmdb(api):
    """
    将nat信息入库
    :return:
    """
    nat_list = api.main()

    with DBContext('w') as session:
        # 清除数据库数据
        try:
            session.query(DB).delete()
            session.commit()
        except:
            session.rollback()
        # 写入新数据
        for rds in nat_list:
            ins_log.read_log('info', 'nat信息：{}'.format(rds))
            new_db = DB(natgatewayid=rds.get('natgatewayid'),
                        state=rds.get('state', ),
                        subnetId=rds.get('subnetId'),
                        vpcid=rds.get('vpcid'),
                        is_use=rds.get('is_use'),
                        createTime=rds.get("createTime"))
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'nat写入数据库共{}条'.format(len(nat_list)))


def main():
    """
    从接口获取配置
    :return:
    """
    session = get_aws_session(**settings.get("aws_key"))
    elb_api = ComplianceNatGateWayApi(session)
    sync_cmdb(elb_api)


if __name__ == '__main__':
    fire.Fire(main)
