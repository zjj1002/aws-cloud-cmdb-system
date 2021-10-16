from sqlalchemy import or_
from websdk.db_context import DBContext

from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.eip import model_to_dict
from models.uncom_vpc import UncomVpc


class UncomVpcHandler(BaseHandler):
    # 未启用S3 ENDPOINT或者ECR ENDPOINT的VPC列表
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                uncom_vpc_info = session.query(UncomVpc).filter(
                    or_(UncomVpc.vpc_id.like('%{}%'.format(key)),
                        UncomVpc.state.like('%{}%'.format(key)),
                        UncomVpc.cidr_block.like('%{}%'.format(key)),
                        UncomVpc.dhcp_options_id.like('%{}%'.format(key)))
                ).order_by(
                    UncomVpc.id
                ).all()
            else:
                uncom_vpc_info = session.query(UncomVpc).order_by(
                    UncomVpc.id
                ).all()
        uncom_vpc_list = []
        for data in uncom_vpc_info:
            if data:
                data_dict = model_to_dict(data)
                uncom_vpc_list.append(data_dict)
        return uncom_vpc_list


uncom_vpc_host_urls = [
    (r"/v1/cmdb/uncom_vpc/", UncomVpcHandler),
]


if __name__ == '__main__':
    pass