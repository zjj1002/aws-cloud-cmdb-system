import fire
from models.eip import FreeEip
from libs.aws.eip import get_eip_list
from opssdk.operate import MyCryptV2
from libs.db_context import DBContext, KEYDBContext
from models.key import KEY, model_to_dict
from libs.web_logs import ins_log


def eip_sync_cmdb(config,account_id,region):
    """eip数据同步"""
    eip_list = get_eip_list(config)
    with DBContext('w') as session:
        session.query(FreeEip).filter(FreeEip.account_id==account_id,FreeEip.region==region).delete(synchronize_session=False)  # 清空数据库的所有记录
        for eip in eip_list:
            public_ip = eip.get("PublicIp", "")
            allocation_id = eip.get("AllocationId", "")
            public_ipv4_pool = eip.get("PublicIpv4Pool", "")
            network_border_group = eip.get("NetworkBorderGroup", "")
            is_used = 1
            if not eip.get("InstanceId") and not eip.get("NetworkInterfaceId"):
                is_used = 0
            new_eip = FreeEip(
                public_ip=public_ip,
                allocation_id=allocation_id,
                public_ipv4_pool=public_ipv4_pool,
                network_border_group=network_border_group,
                is_used=is_used,
                account_id=account_id,
                region=region
            )
            session.add(new_eip)
        session.commit()

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
        eip_sync_cmdb(config,account_id,region)

if __name__ == '__main__':
    fire.Fire(main)