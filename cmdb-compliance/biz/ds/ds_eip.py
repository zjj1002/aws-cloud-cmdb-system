
from libs.db_context import DBContext
from models.eip import FreeEip
from libs.aws.eip import get_eip_list


def eip_sync_cmdb():
    """eip数据同步"""
    eip_list = get_eip_list()
    with DBContext('w') as session:
        session.query(FreeEip).delete(synchronize_session=False)  # 清空数据库的所有记录
        for eip in eip_list:
            public_ip = eip.get("PublicIp", "")
            allocation_id = eip.get("AllocationId", "")
            public_ipv4_pool = eip.get("PublicIpv4Pool", "")
            network_border_group = eip.get("NetworkBorderGroup", "")
            is_used = 1
            if not eip.get("InstanceId") and not eip.get("NetworkInterfaceId"):
                is_used = 0
            new_eip = FreeEip(
                public_ip=public_ip, allocation_id=allocation_id, public_ipv4_pool=public_ipv4_pool,
                network_border_group=network_border_group, is_used=is_used)
            session.add(new_eip)
        session.commit()


if __name__ == '__main__':
    pass