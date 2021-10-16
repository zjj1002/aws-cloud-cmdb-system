from libs.aws.vpc_peering_con import get_vpc_peer_con_list
from libs.db_context import DBContext
from models.vpc_peering import VpcPeering


def vpc_peering_sync_cmdb():
    """vpc_peering数据同步到数据库"""
    vpc_peering_list = get_vpc_peer_con_list()
    with DBContext('w') as session:
        session.query(VpcPeering).delete(synchronize_session=False)  # 清空数据库的所有记录
        for vpc_peering in vpc_peering_list:
            vpc_peering_connection_id = vpc_peering.get("VpcPeeringConnectionId", "")
            requester_cidr_block = vpc_peering["RequesterVpcInfo"].get("CidrBlock", "")
            requester_owner_id = vpc_peering["RequesterVpcInfo"].get("OwnerId", "")
            requester_vpc_id = vpc_peering["RequesterVpcInfo"].get("VpcId", "")
            requester_region = vpc_peering["RequesterVpcInfo"].get("Region", "")
            accepter_cidr_block = vpc_peering["AccepterVpcInfo"].get("CidrBlock", "")
            accepter_owner_id = vpc_peering["AccepterVpcInfo"].get("OwnerId", "")
            accepter_vpc_id = vpc_peering["AccepterVpcInfo"].get("VpcId", "")
            accepter_region = vpc_peering["AccepterVpcInfo"].get("Region", "")
            new_vpc_peering = VpcPeering(
                vpc_peering_connection_id=vpc_peering_connection_id, requester_cidr_block=requester_cidr_block,
                requester_owner_id=requester_owner_id, requester_vpc_id=requester_vpc_id,
                requester_region=requester_region, accepter_cidr_block=accepter_cidr_block,
                accepter_owner_id=accepter_owner_id, accepter_vpc_id=accepter_vpc_id, accepter_region=accepter_region)
            session.add(new_vpc_peering)
        session.commit()


if __name__ == '__main__':
    pass