from libs.db_context import DBContext
from models.tag_list import EC2Instance
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


def ec2_instance_sync_cmdb():
    """数据同步"""
    ec2_instance_list = get_ec2_list()
    with DBContext('w') as session:
        session.query(EC2Instance).delete(synchronize_session=False)  # 清空数据库的所有记录
        for instance in ec2_instance_list:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            tag_name = "UnKnown"
            uptime = "UnKnown"
            downtime = "UnKnown"
            try:
                private_ip = instance["PrivateIpAddress"]
            except Exception as e:
                private_ip = "UnKnown"
                print(e)
            try:
                tags_info = instance["Tags"]
            except Exception as e:
                tags_info = None
                print(e)
            if tags_info:
                for tag in tags_info:
                    if tag["Key"] == "Name":
                        tag_name = tag["Value"]
                    elif tag["Key"] == "uptime":
                        uptime = tag["Value"]
                    elif tag["Key"] == "downtime":
                        downtime = tag["Value"]

            new_ec2 = EC2Instance(
                instance_id=instance_id, service_name="ec2", instance_type=instance_type,
                private_ip=private_ip, tag_name=tag_name, uptime=uptime, downtime=downtime
            )
            session.add(new_ec2)
        session.commit()


if __name__ == '__main__':
    ec2_instance_sync_cmdb()