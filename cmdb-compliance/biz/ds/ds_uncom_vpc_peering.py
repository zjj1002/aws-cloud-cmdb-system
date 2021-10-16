from libs.db_context import DBContext
from models.uncom_vpc_peering import UncomVpcPeering
from models.vpc_peering import VpcPeering, model_to_dict
from models.owner_list import OwnerList
from models.owner_list import model_to_dict as owner_model_to_list


# 获取不合规的vpc peering账户id
def get_uncom_id():
    with DBContext('r') as session:
        # 获取vpc peering的账户id
        vpc_peering_info = session.query(VpcPeering).all()
        account_id = set()
        for data in vpc_peering_info:
            data_dict = model_to_dict(data)
            account_id.add(data_dict["requester_owner_id"])
            account_id.add(data_dict["accepter_owner_id"])
        # 获取owner账户的id
        owner_info = session.query(OwnerList).all()
        owner_id = []
        for data in owner_info:
            data_dict = owner_model_to_list(data)
            owner_id.append(data_dict["owner_id"])
    # 找出不合规的vpc peering账户id
    uncom_id = []
    for a_id in account_id:
        if a_id not in owner_id:
            uncom_id.append(a_id)
    return uncom_id


def get_uncom_vpc_peering():
    """获取到不合规的vpc peering数据列表"""
    uncom_id_list = get_uncom_id()
    with DBContext('r') as session:
        uncom_vpc_peering_info_list = set()
        for uncom_id in uncom_id_list:
            uncom_vpc_peering_info_request = session.query(VpcPeering).filter(VpcPeering.requester_owner_id == uncom_id).all()
            for uncom_vpc_peering_request in uncom_vpc_peering_info_request:
                uncom_vpc_peering_info_list.add(uncom_vpc_peering_request)
            uncom_vpc_peering_info_accepter = session.query(VpcPeering).filter(VpcPeering.accepter_owner_id == uncom_id).all()
            for uncom_vpc_peering_accepter in uncom_vpc_peering_info_accepter:
                uncom_vpc_peering_info_list.add(uncom_vpc_peering_accepter)
    uncom_vpc_peering = []
    for data in uncom_vpc_peering_info_list:
        data_dict = model_to_dict(data)
        uncom_vpc_peering.append(data_dict)
    return uncom_vpc_peering


def uncom_vpc_peering_sync_cmdb():
    """把uncom_vpc_peering数据同步到数据库"""
    uncom_vpc_peering_list = get_uncom_vpc_peering()
    with DBContext('w') as session:
        session.query(UncomVpcPeering).delete(synchronize_session=False)  # 清空数据库的所有记录
        for uncom_vpc_peering in uncom_vpc_peering_list:
            vpc_peering_connection_id = uncom_vpc_peering["vpc_peering_connection_id"]
            requester_cidr_block = uncom_vpc_peering["requester_cidr_block"]
            requester_owner_id = uncom_vpc_peering["requester_owner_id"]
            requester_vpc_id = uncom_vpc_peering["requester_vpc_id"]
            requester_region = uncom_vpc_peering["requester_region"]
            accepter_cidr_block = uncom_vpc_peering["accepter_cidr_block"]
            accepter_owner_id = uncom_vpc_peering["accepter_owner_id"]
            accepter_vpc_id = uncom_vpc_peering["accepter_vpc_id"]
            accepter_region = uncom_vpc_peering["accepter_region"]
            new_uncom_vpc_peering = UncomVpcPeering(
                vpc_peering_connection_id=vpc_peering_connection_id, requester_cidr_block=requester_cidr_block,
                requester_owner_id=requester_owner_id, requester_vpc_id=requester_vpc_id,
                requester_region=requester_region, accepter_cidr_block=accepter_cidr_block,
                accepter_owner_id=accepter_owner_id, accepter_vpc_id=accepter_vpc_id, accepter_region=accepter_region)
            session.add(new_uncom_vpc_peering)
        session.commit()


if __name__ == '__main__':
    pass