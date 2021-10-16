from settings import settings
from libs.aws.session import get_aws_session


def get_ec2_list():
    """获取ec2信息数据"""
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("ec2")
    instance_list = []
    all_instances = clients.describe_instances()
    for reservation in all_instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_list.append(instance)
    return instance_list


if __name__ == '__main__':
    pass