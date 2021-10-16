from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from models.owner_list import OwnerList
from models.uncom_vpc_peering import UncomVpcPeering


class AddOwnerIdHandler(BaseHandler):

    def post(self, *args, **kwargs):
        """添加合规的owner id"""
        key = self.get_argument('key', default=None, strip=True)
        with DBContext('w') as session:
            if not session.query(OwnerList).filter(OwnerList.owner_id == key).first():
                new_owner_id = OwnerList(owner_id=key)
                session.add(new_owner_id)
                session.commit()
                # 根据owner id删除相对应的vpc_peering
                session.query(UncomVpcPeering).filter(
                    UncomVpcPeering.requester_owner_id == key
                ).delete()
                session.query(UncomVpcPeering).filter(
                    UncomVpcPeering.accepter_owner_id == key
                ).delete()
                session.commit()


add_owner_id_host_urls = [
    (r"/v1/cmdb/add_owner_id/", AddOwnerIdHandler),
]


if __name__ == '__main__':
    pass