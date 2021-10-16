from sqlalchemy import or_
from tornado.web import RequestHandler

from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext

from models.com_ami import ComAmi, model_to_dict


class ComAmiHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询合规ami数据接口"""
        key = self.get_argument('key', default=None, strip=True)
        com_ami_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                com_ami_info = session.query(ComAmi).filter(
                    or_(ComAmi.ami_id.like('%{}%'.format(key)),
                        ComAmi.name.like('%{}%'.format(key)),
                        ComAmi.describe.like('%{}%'.format(key)),
                        ComAmi.creation_date.like('%{}%'.format(key)),
                        ComAmi.create_time.like('%{}%'.format(key)),
                        ComAmi.ami_name.like('%{}%'.format(key)))
                ).order_by(
                    ComAmi.id
                ).all()
            else:
                com_ami_info = session.query(ComAmi).order_by(
                    ComAmi.id
                ).all()

        for data in com_ami_info:
            data_dict = model_to_dict(data)
            com_ami_list.append(data_dict)
        return com_ami_list

    def post(self, *args, **kwargs):
        """修改合规的ami信息数据接口"""
        ami_id = self.get_argument('ami_id', default=None, strip=True)
        ami_name = self.get_argument('ami_name', default=None, strip=True)
        name = self.get_argument('name', default=None, strip=True)
        describe = self.get_argument('describe', default=None, strip=True)
        with DBContext('w') as session:
            ami_info = session.query(ComAmi).filter(ComAmi.ami_id == ami_id).first()
            ami_info.ami_name = ami_name
            ami_info.name = name
            ami_info.describe = describe
            session.commit()

    def delete(self, *args, **kwargs):
        """删除某条合规的ami数据接口"""
        ami_id = self.get_argument('ami_id', default=None, strip=True)
        with DBContext('r') as session:
            session.query(ComAmi).filter(ComAmi.ami_id == ami_id).delete()
            session.commit()


com_ami_host_urls = [
    (r"/v1/cmdb/com_ami/", ComAmiHandler),
]


if __name__ == '__main__':
    pass