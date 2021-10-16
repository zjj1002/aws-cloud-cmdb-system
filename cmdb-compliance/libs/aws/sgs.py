from settings import settings
from libs.aws.session import get_aws_session


def get_security_groups_back():
    s = get_aws_session(**settings.get("aws_key"))

    rds_client = s.client("rds")
    rds_sg_set = set()
    rds_data = rds_client.describe_db_instances()  # 获取所有的rds实例
    for db_instances in rds_data['DBInstances']:
        for vpc_sg in db_instances['VpcSecurityGroups']:
            vpc_sg_id = vpc_sg['VpcSecurityGroupId']
            rds_sg_set.add(vpc_sg_id)

    elb_client = s.client("elb")
    elb_sg_set = set()
    elb = elb_client.describe_load_balancers()  # 获取所有的elb实例
    for LoadBalancerDescriptions in elb["LoadBalancerDescriptions"]:
        sg_id = LoadBalancerDescriptions['SecurityGroups'][0]
        elb_sg_set.add(sg_id)

    ec2_client = s.client("ec2")
    sgs = ec2_client.describe_security_groups()
    all_sgs = sgs.get("SecurityGroups")  # 获取所有安全组
    instance_sg_set = set()
    all_instances = ec2_client.describe_instances()  # 获取所有实例
    for reservation in all_instances["Reservations"]:
        for instance in reservation["Instances"]:
            for sg in instance["SecurityGroups"]:
                instance_sg_set.add(sg["GroupId"])

    for sgs in all_sgs:
        sgs['is_used'] = 1
        if sgs.get("GroupId") not in instance_sg_set:
            if sgs.get("GroupId") not in elb_sg_set:
                if sgs.get("GroupId") not in rds_sg_set:
                    sgs['is_used'] = 0
    return all_sgs


def get_security_groups():
    s = get_aws_session(**settings.get("aws_key"))

    ec2_client = s.client("ec2")
    sgs = ec2_client.describe_security_groups()
    all_sgs = sgs.get("SecurityGroups")  # 获取所有安全组

    for sgs in all_sgs:
        sgs['is_used'] = 1
        response = ec2_client.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'group-id',
                    'Values': [
                        sgs.get("GroupId"),
                    ]
                },
            ],
        )
        if len(response['NetworkInterfaces']) == 0:
            sgs['is_used'] = 0
    return all_sgs


if __name__ == '__main__':
    get_security_groups()
