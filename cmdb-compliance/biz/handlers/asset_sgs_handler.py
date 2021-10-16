from sqlalchemy import or_
from biz.ds.ds_sgs import sgs_sync_cmdb
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.sgs import model_to_dict, FreeSgs


class SgsHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        sgs_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                sgs_info = session.query(FreeSgs).filter(
                    or_(FreeSgs.security_group_id.like('%{}%'.format(key)),
                        FreeSgs.security_group_name.like('%{}%'.format(key)),
                        FreeSgs.owner_id.like('%{}%'.format(key)),
                        FreeSgs.description.like('%{}%'.format(key)),
                        FreeSgs.ip_permissions_egress.like('%{}%'.format(key)),
                        FreeSgs.ip_permissions.like('%{}%'.format(key)),
                        FreeSgs.to_port.like('%{}%'.format(key)),
                        FreeSgs.vpc_id.like('%{}%'.format(key)))).filter(
                    FreeSgs.is_used == 0
                ).order_by(
                    FreeSgs.id
                ).all()
            else:
                sgs_info = session.query(FreeSgs).filter(
                    FreeSgs.is_used == 0
                ).order_by(FreeSgs.id).all()

        for data in sgs_info:
            data_dict = model_to_dict(data)
            sgs_list.append(data_dict)
        return sgs_list

    # 获取数据，更新数据库的请求
    def post(self, *args, **kwargs):
        sgs_sync_cmdb()


sgs_host_urls = [
    (r"/v1/cmdb/sgs/", SgsHandler),
]

if __name__ == '__main__':
    pass
