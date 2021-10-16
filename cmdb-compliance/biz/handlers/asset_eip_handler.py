from sqlalchemy import or_
from biz.ds.ds_eip import eip_sync_cmdb
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.eip import FreeEip, model_to_dict


class EipHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        eip_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                epi_info = session.query(FreeEip).filter(
                    or_(FreeEip.public_ip.like('%{}%'.format(key)),
                        FreeEip.allocation_id.like('%{}%'.format(key)),
                        FreeEip.public_ipv4_pool.like('%{}%'.format(key)),
                        FreeEip.network_border_group.like('%{}%'.format(key)))
                ).filter(
                    FreeEip.is_used == 0
                ).all()
            else:
                epi_info = session.query(FreeEip).filter(
                    FreeEip.is_used == 0
                ).all()

        for data in epi_info:
            data_dict = model_to_dict(data)
            eip_list.append(data_dict)
        return eip_list

    # 获取数据，更新数据库的请求
    def post(self, *args, **kwargs):
        eip_sync_cmdb()


eip_host_urls = [
    (r"/v1/cmdb/eip/", EipHandler),
]


if __name__ == '__main__':
    pass