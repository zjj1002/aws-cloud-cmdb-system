from sqlalchemy import or_
from tornado.web import RequestHandler

from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from libs.pagination import pagination_util
from models.tag_list import TagList, model_to_dict, ServicesTagMiddle, ServicesList


class TagServicesHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询出标签服务关联的数据接口"""
        tag_list = []
        with DBContext('r') as session:
            tag_services_info = session.query(ServicesTagMiddle).all()
            for data in tag_services_info:
                data_dict = model_to_dict(data)
                tag_info = session.query(TagList).filter(TagList.id == data_dict["tag_id"]).first()
                tag_name = model_to_dict(tag_info)["key"]
                services_info = session.query(ServicesList).filter(ServicesList.id == data_dict["services_id"]).first()
                services_name = model_to_dict(services_info)["services_name"]
                tag_list.append({tag_name: services_name})
        return tag_list


tag_services_host_urls = [
    (r"/v1/cmdb/tag_services/", TagServicesHandler),
]


if __name__ == '__main__':
    pass












