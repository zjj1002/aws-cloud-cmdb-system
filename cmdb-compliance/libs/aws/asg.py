from libs.aws.session import get_aws_session
from settings import settings


def get_asg_list():
    """获取最小和所需都为0的ASG数据"""
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("autoscaling")
    resp_dict = clients.describe_auto_scaling_groups()
    all_asg = resp_dict.get("AutoScalingGroups")
    asg_list = []
    for asg in all_asg:
        if asg["MinSize"] == 0 and asg["DesiredCapacity"] == 0:
            asg_list.append(asg)
    return asg_list


if __name__ == '__main__':
    pass