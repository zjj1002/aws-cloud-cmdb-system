from libs.aws.session import get_aws_session
from settings import settings


def get_ami_list():
    """获取ami的信息"""
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("ec2")
    resp_dict = clients.describe_images(Owners=['self'])
    all_ami = resp_dict.get("Images")
    ami_list = []
    for ami in all_ami:
        ami_list.append(ami)
    return ami_list


if __name__ == '__main__':
    print(get_ami_list())