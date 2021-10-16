# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from tornado.web import RequestHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.ebs import DB, model_to_dict
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from biz.ds.ds_ebs import main as aws_ebs_refresh


class GetEbsHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        button = int(self.get_argument('button', default='0', strip=True))
        if button == 1:
            aws_ebs_refresh()
        ebs_list = []
        with DBContext('w') as session:
            if key:
                ebs_info = session.query(DB).filter(
                    or_(DB.Attachments.like('%{}%'.format(key)),
                        DB.AvailabilityZone.like('%{}%'.format(key)),
                        DB.Encrypted.like('%{}%'.format(key)),
                        DB.Size.like('%{}%'.format(key)),
                        DB.SnapshotId.like('%{}%'.format(key)),
                        DB.State.like('%{}%'.format(key)),
                        DB.VolumeId.like('%{}%'.format(key)),
                        DB.Iops.like('%{}%'.format(key)),
                        DB.VolumeType.like('%{}%'.format(key)),

                        )
                ).filter(or_(DB.Attachments == "磁盘没有被使用",
                             DB.Encrypted == "false",
                             DB.Snapshot_overtime == "false", )
                         ).all()

            else:
                ebs_info = session.query(DB).filter(
                    or_(DB.Attachments == "磁盘没有被使用",
                        DB.Encrypted ==  "false",
                        DB.Snapshot_overtime ==  "false", )
                ).all()

        for data in ebs_info:
            data_dict = model_to_dict(data)
            data_dict.pop("update_time")
            ebs_list.append(data_dict)
        return ebs_list


aws_ebs_urls = [
    (r"/v1/cmdb/ebs/", GetEbsHandler),
]
