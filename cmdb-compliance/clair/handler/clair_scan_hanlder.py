# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from tornado.web import RequestHandler

from clair.main import scan_images_by_day
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.clair_db import model_to_dict, LocalImage, ScanResult
from websdk.db_context import DBContext


class GetLocalImage(RequestHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        local_image_list = []
        with DBContext('w') as session:
            if key:
                images_info = session.query(LocalImage).filter(
                    or_(LocalImage.REPOSITORY.like('%{}%'.format(key)),
                        LocalImage.IMAGE_ID.like('%{}%'.format(key)),
                        LocalImage.CREATED.like('%{}%'.format(key)),
                        LocalImage.is_scan.like('%{}%'.format(key)),
                        LocalImage.SIZE.like('%{}%'.format(key)),
                        LocalImage.last_scan_time.like('%{}%'.format(key)),
                        LocalImage.TAG.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                images_info = session.query(LocalImage).all()
        for data in images_info:
            data_dict = model_to_dict(data)
            local_image_list.append(data_dict)
            # 返回数据
        return local_image_list


class GetScanResult(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        image = self.get_argument('image', default=None, strip=True)
        with DBContext('w') as session:
            images_info = session.query(LocalImage).filter(LocalImage.is_scan==True).first()
            if images_info:
                images_info = model_to_dict(images_info)
            else:
                return []
        if image == None:
            image = images_info['REPOSITORY'] + ":"+images_info['TAG']
        scan_result_list = []
        with DBContext('w') as session:
            result_data = session.query(ScanResult) \
                .filter(ScanResult.image == image).all()
        for data in result_data:
            data_dict = model_to_dict(data)
            scan_result_list.append(data_dict)
            #返回数据
        return scan_result_list


#测试用 后续会删除---lch
class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        scan_images_by_day()
        return "测试中"


aws_clair_urls = [
    (r"/v1/cmdb/clair/local_image/", GetLocalImage),
    (r"/v1/cmdb/clair/scan_cliar/", GetScanResult),
    (r"/v1/cmdb/apitest/", ApiTest),

]
