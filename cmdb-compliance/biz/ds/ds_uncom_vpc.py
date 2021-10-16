import re

from libs.db_context import DBContext
from models.eip import model_to_dict
from models.uncom_vpc import UncomVpc
from models.vpc import Vpc
from models.vpc_endpoint import VpcEndpoint


# 找出未启用s3 endpoint或者ecr endpoint的vpc id
def get_uncom_vpc_id():
    with DBContext('r') as session:
        vpc_endpoint_info = session.query(VpcEndpoint).all()
        vpc_endpoint = []
        for data in vpc_endpoint_info:
            data_dict = model_to_dict(data)
            vpc_endpoint.append(data_dict)
        vpc_id_list = []
        for i in vpc_endpoint:
            if i["service_name"][-2:] == "s3" or re.search(".ecr", i["service_name"]):
                continue
            else:
                vpc_id_list.append(i["vpc_id"])
        return vpc_id_list


# 获取不合规的vpc列表
def get_uncom_vpc_list():
    with DBContext('r') as session:
        vpc_info_list = []
        for uncom_vpc_id in get_uncom_vpc_id():
            vpc_info = session.query(Vpc).filter(
                Vpc.vpc_id == uncom_vpc_id
            ).first()
            vpc_info_list.append(vpc_info)
    vpc_list = []
    for data in vpc_info_list:
        if data:
            data_dict = model_to_dict(data)
            vpc_list.append(data_dict)
    return vpc_list


def uncom_vpc_sync_cmdb():
    """把uncom vpc数据同步到数据库"""
    with DBContext('w') as session:
        session.query(UncomVpc).delete(synchronize_session=False)  # 清空数据库的所有记录
        for uncom_vpc in get_uncom_vpc_list():
            vpc_id = uncom_vpc.get("vpc_id", "")
            state = uncom_vpc.get("state", "")
            cidr_block = uncom_vpc.get("cidr_block", "")
            dhcp_options_id = uncom_vpc.get("dhcp_options_id", "")
            new_vpc = UncomVpc(
                vpc_id=vpc_id, state=state, cidr_block=cidr_block,dhcp_options_id=dhcp_options_id)
            session.add(new_vpc)
        session.commit()


if __name__ == '__main__':
    pass