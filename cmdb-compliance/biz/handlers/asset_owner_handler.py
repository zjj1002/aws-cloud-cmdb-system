from sqlalchemy import or_
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext
from models.owner_list import OwnerList, model_to_dict


class OwnerHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询合规owner id数据接口"""
        key = self.get_argument('key', default=None, strip=True)
        owner_id_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                owner_info = session.query(OwnerList).filter(
                    or_(OwnerList.owner_id.like('%{}%'.format(key)),
                        OwnerList.name.like('%{}%'.format(key)))
                ).order_by(
                    OwnerList.id
                ).all()
            else:
                owner_info = session.query(OwnerList).order_by(
                    OwnerList.id
                ).all()

        for data in owner_info:
            data_dict = model_to_dict(data)
            owner_id_list.append(data_dict)
        return owner_id_list

    def post(self, *args, **kwargs):
        """修改合规的owner id信息数据接口"""
        owner_id = self.get_argument('owner_id', default=None, strip=True)
        name = self.get_argument('name', default=None, strip=True)
        with DBContext('w') as session:
            owner_info = session.query(OwnerList).filter(OwnerList.owner_id == owner_id).first()
            owner_info.name = name
            session.commit()

    def delete(self, *args, **kwargs):
        """删除某条合规的owner id数据接口"""
        owner_id = self.get_argument('owner_id', default=None, strip=True)
        with DBContext('r') as session:
            session.query(OwnerList).filter(OwnerList.owner_id == owner_id).delete()
            session.commit()


owner_id_host_urls = [
    (r"/v1/cmdb/owner_id/", OwnerHandler),
]


if __name__ == '__main__':
    pass