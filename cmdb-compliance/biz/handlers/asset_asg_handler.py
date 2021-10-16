from sqlalchemy import or_
from biz.ds.ds_asg import asg_sync_cmdb
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.asg import Asg, model_to_dict
from websdk.db_context import DBContext


class AsgHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        asg_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                asg_info = session.query(Asg).filter(
                    or_(Asg.asg_name.like('%{}%'.format(key)),
                        Asg.asg_arn.like('%{}%'.format(key)),
                        Asg.launch_template.like('%{}%'.format(key)),
                        Asg.availability_zones.like('%{}%'.format(key)),
                        Asg.health_check_type.like('%{}%'.format(key)),
                        Asg.asg_created_time.like('%{}%'.format(key)))
                ).order_by(
                    Asg.id
                ).all()
            else:
                asg_info = session.query(Asg).order_by(
                    Asg.id
                ).all()

        for data in asg_info:
            data_dict = model_to_dict(data)
            asg_list.append(data_dict)
        return asg_list

    # 获取数据，更新数据库的请求
    def post(self, *args, **kwargs):
        asg_sync_cmdb()


asg_host_urls = [
    (r"/v1/cmdb/asg/", AsgHandler),
]


if __name__ == '__main__':
    pass