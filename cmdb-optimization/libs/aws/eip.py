
from libs.aws.session import get_aws_session


def get_eip_list(config):
    """获取所以的eip"""
    s = get_aws_session(config)
    clients = s.client("ec2")
    resp_dict = clients.describe_addresses()
    eip_list = resp_dict.get("Addresses")
    return eip_list


if __name__ == '__main__':
    pass
