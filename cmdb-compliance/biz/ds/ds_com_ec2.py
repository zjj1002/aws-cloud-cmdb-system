from libs.aws.com_ec2 import get_ec2_list
from libs.db_context import DBContext
from models.ec2 import ComEc2


def com_ec2_sync_cmdb():
    """数据同步"""
    com_ec2_list = get_ec2_list()
    with DBContext('w') as session:
        session.query(ComEc2).delete(synchronize_session=False)  # 清空数据库的所有记录
        for com_ec2 in com_ec2_list:
            instance_id = com_ec2.get("InstanceId", "")
            ami_id = com_ec2.get("ImageId", "")
            instance_type = com_ec2.get("InstanceType", "")
            key_name = com_ec2.get("KeyName", "")
            launch_time = com_ec2.get("LaunchTime", "")
            placement = str(com_ec2.get("Placement", ""))
            private_dns_name = com_ec2.get("PrivateDnsName", "")
            private_ip_address = com_ec2.get("PrivateIpAddress", "")
            public_dns_name = com_ec2.get("PublicDnsName", "")
            public_ip_address = com_ec2.get("PublicIpAddress", "")
            new_com_ec2 = ComEc2(
                instance_id=instance_id, ami_id=ami_id, instance_type=instance_type, key_name=key_name,
                launch_time=launch_time, placement=placement, private_dns_name=private_dns_name,
                private_ip_address=private_ip_address, public_dns_name=public_dns_name, public_ip_address=public_ip_address
            )
            session.add(new_com_ec2)
        session.commit()


if __name__ == '__main__':
    com_ec2_sync_cmdb()