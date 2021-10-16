from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from libs.pagination import pagination_util
from models.uncom_vpc_peering import UncomVpcPeering, model_to_dict
from sqlalchemy import or_


class UncomVpcPeeringHandler(BaseHandler):
    """不合规的vpc_peering"""
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                uncom_vpc_peering_info = session.query(UncomVpcPeering).filter(
                    or_(UncomVpcPeering.vpc_peering_connection_id.like('%{}%'.format(key)),
                        UncomVpcPeering.requester_cidr_block.like('%{}%'.format(key)),
                        UncomVpcPeering.requester_owner_id.like('%{}%'.format(key)),
                        UncomVpcPeering.requester_vpc_id.like('%{}%'.format(key)),
                        UncomVpcPeering.requester_region.like('%{}%'.format(key)),
                        UncomVpcPeering.accepter_cidr_block.like('%{}%'.format(key)),
                        UncomVpcPeering.accepter_owner_id.like('%{}%'.format(key)),
                        UncomVpcPeering.accepter_vpc_id.like('%{}%'.format(key)),
                        UncomVpcPeering.accepter_region.like('%{}%'.format(key)))
                ).order_by(
                    UncomVpcPeering.id
                ).all()
            else:
                uncom_vpc_peering_info = session.query(UncomVpcPeering).order_by(
                    UncomVpcPeering.id
                ).all()
        uncom_vpc_peering_list = []
        for data in uncom_vpc_peering_info:
            if data:
                data_dict = model_to_dict(data)
                uncom_vpc_peering_list.append(data_dict)
        return uncom_vpc_peering_list


uncom_vpc_peering_host_urls = [
    (r"/v1/cmdb/uncom_vpc_peering/", UncomVpcPeeringHandler),
]


if __name__ == '__main__':
    pass