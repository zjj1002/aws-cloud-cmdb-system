# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from tornado.web import RequestHandler
from awssts.aws_sts import AWSSTS
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.aws_sts import AwsSts, model_to_dict
from websdk.db_context import DBContext


class AWSSTShanlder(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        local_image_list = []
        with DBContext('w') as session:
            if key:
                images_info = session.query(AwsSts).filter(
                    or_(AwsSts.bucket.like('%{}%'.format(key)),
                        AwsSts.Action.like('%{}%'.format(key)),
                        AwsSts.RoleArn.like('%{}%'.format(key)),
                        AwsSts.RoleSessionName.like('%{}%'.format(key)),
                        AwsSts.region_name.like('%{}%'.format(key)),
                        AwsSts.externalid.like('%{}%'.format(key)),
                        AwsSts.RoleArn.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                images_info = session.query(AwsSts).all()
        for data in images_info:
            data_dict = model_to_dict(data)
            local_image_list.append(data_dict)
            # 返回数据
        return local_image_list

    def post(self, *args, **kwargs):
        region_name = self.get_body_argument("region_name", default=None, strip=True)
        aws_access_key_id = self.get_body_argument("aws_access_key_id", default=None, strip=True)
        aws_secret_access_key = self.get_body_argument("aws_secret_access_key", default=None, strip=True)
        action = self.get_body_argument("action", default=None, strip=True)
        resource = self.get_body_argument("resource", default=None, strip=True)
        rolearn = self.get_body_argument("rolearn", default=None, strip=True)
        rolesessionname = self.get_body_argument("rolesessionname", default=None, strip=True)
        externalid = self.get_body_argument("externalid", default="fasdfsdfsdfsdf", strip=True)
        durationseconds = self.get_body_argument("durationseconds", default=None, strip=True)
        sts = AWSSTS(
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            action=action,
            resource=resource,
            rolearn=rolearn,
            rolesessionname=rolesessionname,
            externalid=externalid,
            durationseconds=int(durationseconds)
        )
        sts.main()
        return self.write(dict(code=0,
                               msg='添加成功', ))

    def delete(self, *args, **kwargs):
        AccessKeyId = self.get_body_argument('AccessKeyId', default=None, strip=True)
        with DBContext('r') as session:
            session.query(AwsSts).filter(AwsSts.AccessKeyId == AccessKeyId).delete()
            session.commit()
        return self.write(dict(code=0,
                               msg='删除成功', ))


aws_sts_urls = [
    (r"/v1/cmdb/sts/", AWSSTShanlder),
]
