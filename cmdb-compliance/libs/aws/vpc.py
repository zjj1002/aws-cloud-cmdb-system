from settings import settings
from libs.aws.session import get_aws_session


def get_vpc_list():
    """获取所有的vpc信息"""
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("ec2")
    resp_dict = clients.describe_vpcs()
    vpc_list = resp_dict.get("Vpcs")
    return vpc_list


if __name__ == '__main__':
    pass
