from sqlalchemy import or_
from tornado.web import RequestHandler

from libs.aws.session import get_aws_session
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext
from models.tag_list import TagList, model_to_dict, ServicesTagMiddle, ServicesList, EC2Instance
from settings import settings


class TagManageHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询出标签管理数据接口"""
        search_key = self.get_argument('search_key', default=None, strip=True)
        tag_list = []
        with DBContext('r') as session:
            if search_key:
                # 模糊查所有
                tag_info = session.query(TagList).filter(
                    or_(TagList.key.like('%{}%'.format(search_key)),
                        TagList.value.like('%{}%'.format(search_key)),
                        TagList.describe.like('%{}%'.format(search_key)),
                        TagList.service_name.like('%{}%'.format(search_key)))
                ).order_by(
                    TagList.id
                ).all()
            else:
                tag_info = session.query(TagList).order_by(
                    TagList.id
                ).all()

        for data in tag_info:
            data_dict = model_to_dict(data)
            tag_list.append(data_dict)
        return tag_list

    def post(self, *args, **kwargs):
        """管理员添加标签信息数据接口"""
        tag_key = self.get_argument('tag_key', default=None, strip=True)
        tag_value = self.get_argument('tag_value', default=None, strip=True)
        tag_describe = self.get_argument('tag_describe', default=None, strip=True)
        with DBContext('w') as session:
            tag_info = session.query(TagList).filter(TagList.key == tag_key).first()
            if not tag_info:
                new_tag = TagList(key=tag_key, value=tag_value, describe=tag_describe)
                session.add(new_tag)
                session.commit()

    def put(self, *args, **kwargs):
        """管理员修改标签信息数据接口"""
        tag_key = self.get_argument('tag_key', default=None, strip=True)
        tag_value = self.get_argument('tag_value', default=None, strip=True)
        tag_describe = self.get_argument('tag_describe', default=None, strip=True)
        with DBContext('w') as session:
            tag_info = session.query(TagList).filter(
                TagList.key == tag_key
            ).first()
            tag_info.value = tag_value
            tag_info.describe = tag_describe
            session.commit()

    def delete(self, *args, **kwargs):
        """删除某个标签数据接口"""
        tag_key = self.get_argument('tag_key', default=None, strip=True)
        with DBContext('w') as session:
            session.query(TagList).filter(TagList.key == tag_key).delete()
            session.commit()


class ConTagServices(BaseHandler):

    def get(self, *args, **kwargs):
        """可关联的服务名称"""
        with DBContext('w') as session:
            services_name_list = []
            all_services_info = session.query(ServicesList).all()
            for services in all_services_info:
                services_name = model_to_dict(services)["services_name"]
                services_name_list.append(services_name)
        return self.write(dict(code=0, msg='获取成功', total=len(services_name_list), data=services_name_list))

    def post(self, *args, **kwargs):
        """关联标签和服务"""
        tag_key = self.get_argument('tag_key', default=None, strip=True)
        services_name = self.get_argument('services_name', default=None, strip=True)  # 传入一个service_name的列表
        with DBContext('w') as session:
            tag_info = session.query(TagList).filter(TagList.key == tag_key).first()
            tag_id = model_to_dict(tag_info)['id']
            tag_info.service_name = services_name

            for name in services_name.split(','):
                services_info = session.query(ServicesList).filter(ServicesList.services_name == name).first()
                if not services_info:
                    new_service = ServicesList(services_name=name)
                    session.add(new_service)
                    session.commit()

            services_id_list = []
            for name in services_name.split(','):
                services_info = session.query(ServicesList).filter(ServicesList.services_name == name).first()
                dict_data = model_to_dict(services_info)
                services_id = dict_data['id']
                services_id_list.append(services_id)

            for services_id in services_id_list:
                data_info = session.query(ServicesTagMiddle).filter_by(
                    tag_id=tag_id, services_id=services_id
                ).first()
                if not data_info:
                    new_middle = ServicesTagMiddle(tag_id=tag_id, services_id=services_id)
                    session.add(new_middle)
                session.commit()


class SetTimeTag(BaseHandler):

    def put(self, *args, **kwargs):
        """设置开关机时间标签"""
        instance_id = self.get_argument('instance_id', default=None, strip=True)  # 传一个列表
        uptime = self.get_argument('uptime', default=None, strip=True)
        downtime = self.get_argument('downtime', default=None, strip=True)  # 字符串类型的时间 '8:30'
        week = self.get_argument('week', default=None, strip=True)  # 传一个列表类型的数据
        temp = [uptime, downtime]
        instance_id_list = instance_id.split(',')
        s = get_aws_session(**settings.get("aws_key"))
        client = s.client("ec2")
        for i, data in enumerate(temp):
            data_list = data.split(':')
            s = int(data_list[1])
            h = int(data_list[0])
            w = '*'
            if week:
                str_week = [str(i) for i in week]
                w = ','.join(str_week)
            value = f'{s} {h} * * {w}'
            if i == 0:
                try:
                    client.create_tags(
                        Resources=instance_id_list,
                        Tags=[
                            {
                                'Key': 'uptime',
                                'Value': value,
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
                                'Value': value,
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
                ec2_info = session.query(EC2Instance).filter(
                    EC2Instance.instance_id == tag["ResourceId"]).first()
                if tag["Key"] == "uptime":
                    ec2_info.uptime = tag["Value"]
                    session.commit()
                elif tag["Key"] == "downtime":
                    ec2_info.downtime = tag["Value"]
                    session.commit()


tag_manage_host_urls = [
    (r"/v1/cmdb/tag_manage/", TagManageHandler),
    (r"/v1/cmdb/con_tag_services/", ConTagServices),
    (r"/v1/cmdb/set_time_tag/", SetTimeTag),
]


if __name__ == '__main__':
    pass