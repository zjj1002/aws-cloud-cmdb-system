from models.com_ami import ComAmi
from models.ec2 import model_to_dict
from libs.db_context import DBContext
from models.ec2 import ComEc2
from models.uncom_ec2 import UnComEc2


# 从com_ami中获取ami信息
def get_com_ami():
    with DBContext('r') as session:
        ami_info = session.query(ComAmi).all()
        ami_list = []
        ami_id_list = set()
        for data in ami_info:
            data_dict = model_to_dict(data)
            ami_list.append(data_dict)
        for ami in ami_list:
            ami_id_list.add(ami["ami_id"])
        return ami_id_list


# 对比获取不合规的ec2信息数据
def get_uncom_ec2():
    com_ami = get_com_ami()
    with DBContext('r') as session:
        ec2_info = session.query(ComEc2).all()
        uncom_ec2_list = []
        for data in ec2_info:
            ec2 = model_to_dict(data)
            if ec2["ami_id"] not in com_ami:
                un_ec2_info = session.query(ComEc2).filter(ComEc2.instance_id == ec2["instance_id"]).first()
                data_dict = model_to_dict(un_ec2_info)
                uncom_ec2_list.append(data_dict)
        return uncom_ec2_list


def uncom_ec2_sync_cmdb():
    """没有使用合规的ami的ec2数据同步"""
    with DBContext('w') as session:
        uncom_ec2_list = get_uncom_ec2()
        session.query(UnComEc2).delete(synchronize_session=False)  # 清空数据库的所有记录
        for uncom_ec2 in uncom_ec2_list:
            instance_id = uncom_ec2["instance_id"]
            ami_id = uncom_ec2["ami_id"]
            instance_type = uncom_ec2["instance_type"]
            key_name = uncom_ec2["key_name"]
            launch_time = uncom_ec2["launch_time"]
            placement = uncom_ec2["placement"]
            private_dns_name = uncom_ec2["private_dns_name"]
            private_ip_address = uncom_ec2["private_ip_address"]
            public_dns_name = uncom_ec2["public_dns_name"]
            public_ip_address = uncom_ec2["public_ip_address"]
            new_uncom_ec2 = UnComEc2(
                instance_id=instance_id, ami_id=ami_id, instance_type=instance_type, key_name=key_name,
                launch_time=launch_time, placement=placement, private_dns_name=private_dns_name,
                private_ip_address=private_ip_address, public_dns_name=public_dns_name, public_ip_address=public_ip_address
            )
            session.add(new_uncom_ec2)
        session.commit()


if __name__ == '__main__':
    uncom_ec2_sync_cmdb()


















