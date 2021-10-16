from sqlalchemy import or_
from tornado.web import RequestHandler

from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext
from models.tag_list import model_to_dict, ResultList, ChangeResultList


class TagResultHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询出标签检测结果数据接口"""
        search_key = self.get_argument('search_key', default=None, strip=True)
        tag_list = []
        with DBContext('r') as session:
            if search_key:
                # 模糊查所有
                tag_info = session.query(ResultList).filter(
                    or_(ResultList.services_name.like('%{}%'.format(search_key)),
                        ResultList.services_resource_id.like('%{}%'.format(search_key)),
                        ResultList.key.like('%{}%'.format(search_key)),
                        ResultList.value.like('%{}%'.format(search_key)),
                        ResultList.is_valid.like('%{}%'.format(search_key)))
                ).order_by(
                    ResultList.id
                ).all()
            else:
                tag_info = session.query(ResultList).order_by(
                    ResultList.id
                ).all()

        for data in tag_info:
            data_dict = model_to_dict(data)
            tag_list.append(data_dict)
        return tag_list

    def put(self, *args, **kwargs):
        """管理员修改标签value数据接口"""
        tag_key = self.get_argument('tag_key', default=None, strip=True)
        services_name = self.get_argument('services_name', default=None, strip=True)
        resource_id = self.get_argument('resource_id', default=None, strip=True)
        tag_value = self.get_argument('tag_value', default=None, strip=True)
        with DBContext('w') as session:
            tag_info = session.query(ResultList).filter_by(
                services_name=services_name, services_resource_id=resource_id, key=tag_key
            ).first()
            tag_info.value = tag_value
            session.commit()
            # 把修改的数据记录到修改数据库
            new_order_tag = ChangeResultList(
                key=tag_key, services_name=services_name,
                services_resource_id=resource_id, value=tag_value)
            session.add(new_order_tag)
            session.commit()


tag_result_host_urls = [
    (r"/v1/cmdb/tag_result/", TagResultHandler),
]


if __name__ == '__main__':
    pass