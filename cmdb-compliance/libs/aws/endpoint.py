from settings import settings
from libs.aws.session import get_aws_session


def get_endpoint_list():
    """获取endpoint信息"""
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("ec2")
    resp_dict = clients.describe_vpc_endpoints()
    endpoint_list = resp_dict.get("VpcEndpoints")
    return endpoint_list


if __name__ == '__main__':
    pass

