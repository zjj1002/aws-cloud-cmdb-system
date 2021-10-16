from libs.aws.asg import get_asg_list
from libs.db_context import DBContext
from models.asg import Asg


def asg_sync_cmdb():
    """最小和所需都为0的ASG数据同步"""

    asg_list = get_asg_list()
    with DBContext('w') as session:
        session.query(Asg).delete(synchronize_session=False)  # 清空数据库的所有记录
        for asg in asg_list:
            asg_name = asg.get("AutoScalingGroupName", "")
            asg_arn = asg.get("AutoScalingGroupARN", "")
            launch_template = str(asg.get("LaunchTemplate", ""))
            min_size = asg.get("MinSize", "")
            max_size = asg.get("MaxSize", "")
            desirced_capacity = asg.get("DesiredCapacity", "")
            availability_zones = asg.get("AvailabilityZones", "")[0]
            health_check_type = asg.get("HealthCheckType", "")
            asg_created_time = str(asg.get("CreatedTime", ""))
            new_asg = Asg(
                asg_name=asg_name, asg_arn=asg_arn, launch_template=launch_template,
                min_size=min_size, max_size=max_size, desirced_capacity=desirced_capacity,
                availability_zones=availability_zones, health_check_type=health_check_type,
                asg_created_time=asg_created_time)
            session.add(new_asg)
        session.commit()


if __name__ == '__main__':
    pass