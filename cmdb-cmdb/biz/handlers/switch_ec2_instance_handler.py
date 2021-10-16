from datetime import datetime
from croniter import croniter
from sqlalchemy import or_
from libs.web_logs import ins_log
from settings import settings
from libs.aws.session import get_aws_session
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext
from models.tag_list import model_to_dict, EC2Instance


class Ec2InstanceHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询出定时开关机的ec2信息数据接口"""
        key = self.get_argument('key', default=None, strip=True)
        ec2_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                ec2_info = session.query(EC2Instance).filter(
                    or_(EC2Instance.service_name.like('%{}%'.format(key)),
                        EC2Instance.instance_id.like('%{}%'.format(key)),
                        EC2Instance.tag_name.like('%{}%'.format(key)),
                        EC2Instance.private_ip.like('%{}%'.format(key)),
                        EC2Instance.uptime.like('%{}%'.format(key)),
                        EC2Instance.downtime.like('%{}%'.format(key)),
                        EC2Instance.instance_type.like('%{}%'.format(key)))
                ).order_by(
                    EC2Instance.id
                ).all()
            else:
                ec2_info = session.query(EC2Instance).order_by(
                    EC2Instance.id
                ).all()

        for data in ec2_info:
            data_dict = model_to_dict(data)
            ec2_list.append(data_dict)
        return ec2_list

    def put(self, *args, **kwargs):
        """修改开关机时间，并更改aws服务上的标签"""
        instance_id = self.get_argument('instance_id', default=None, strip=True)  # 传一个列表
        cron_times = self.get_argument('cron_times', default=None, strip=True)
        switch_up_down = self.get_argument('switch_up_down', default=None, strip=True)
        instance_id_list = instance_id.split(',')
        s = get_aws_session(**settings.get("aws_key"))
        client = s.client("ec2")
        try:
            croniter(cron_times, datetime.now())
        except Exception as e:
            ins_log.read_log('info', e)
            return self.write(dict(code=0, msg='输入的时间格式错误'))
        if switch_up_down == "开机":
            try:
                client.create_tags(
                    Resources=instance_id_list,
                    Tags=[
                        {
                            'Key': 'uptime',
                            'Value': cron_times,
                        },
                    ],
                )
            except Exception as e:
                if "UnauthorizedOperation" in str(e):
                    return self.write(dict(code=0, msg='没有权限'))
                else:
                    return self.write(dict(code=0, msg='其他错误'))
        else:
            try:
                client.create_tags(
                    Resources=instance_id_list,
                    Tags=[
                        {
                            'Key': 'downtime',
                            'Value': cron_times,
                        },
                    ],
                )
            except Exception as e:
                if "UnauthorizedOperation" in str(e):
                    return self.write(dict(code=0, msg='没有权限'))
                else:
                    return self.write(dict(code=0, msg='其他错误'))
        # 更改完之后，去aws服务上获取更改过后的数据同步到数据库
        response = client.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': instance_id_list
                },
            ],
        )
        with DBContext('w') as session:
            for tag in response["Tags"]:
                ec2_info = session.query(EC2Instance).filter(EC2Instance.instance_id == tag["ResourceId"]).first()
                if tag["Key"] == "uptime":
                    ec2_info.uptime = tag["Value"]
                    session.commit()
                elif tag["Key"] == "downtime":
                    ec2_info.downtime = tag["Value"]
                    session.commit()


ec2_instance_host_urls = [
    (r"/v1/cmdb/ec2_instance/", Ec2InstanceHandler),
]


if __name__ == '__main__':
    pass