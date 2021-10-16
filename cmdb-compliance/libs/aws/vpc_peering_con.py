from settings import settings
from libs.aws.session import get_aws_session


def get_vpc_peer_con_list():
    """获取vpc对等连接的数据信息"""
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("ec2")
    resp_dict = clients.describe_vpc_peering_connections()
    vpc_peer_con_list = resp_dict.get("VpcPeeringConnections")
    return vpc_peer_con_list


if __name__ == '__main__':
    pass
