
from libs.aws.tags import get_configs
from websdk.web_logs import ins_log
import boto3
from sqlalchemy import or_,exc
from websdk.db_context import DBContext
from models.db import Unattach_Ebs
from models.db import DBTag, DB, model_to_dict
from opssdk.operate import MyCryptV2
from libs.base_handler import BaseHandler
from tornado.web import RequestHandler, HTTPError
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import json
import itertools
import datetime

class EbsHandler(BaseHandler):
#class EbsHandler(RequestHandler): ##测试之用
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = int(self.get_argument('limit', default=15, strip=True))
        limit_start = (int(page_size) - 1) * int(limit)
        result_list = []

        with DBContext('r') as session:
            if key:
                # 模糊查所有
                host_info = session.query(Unattach_Ebs).filter(or_(Unattach_Ebs.Attachments.like('%{}%'.format(key)),
                                                         Unattach_Ebs.CreateTime.like('%{}%'.format(key)),
                                                         Unattach_Ebs.Encrypted.like('%{}%'.format(key)),
                                                         Unattach_Ebs.AvailabilityZone.like('%{}%'.format(key)),
                                                         Unattach_Ebs.Size.like('%{}%'.format(key)),
                                                         Unattach_Ebs.SnapshotId.like('%{}%'.format(key)),
                                                         Unattach_Ebs.State.like('%{}%'.format(key)),
                                                         Unattach_Ebs.VolumeId.like('%{}%'.format(key)),
                                                         Unattach_Ebs.VolumeType.like('%{}%'.format(key)),
                                                         Unattach_Ebs.Iops.like('%{}%'.format(key)))).order_by(Unattach_Ebs.id).all()
                count = host_info.count()
            else:
                host_info = session.query(Unattach_Ebs).order_by(Unattach_Ebs.id)
                count = host_info.count()

            host_info = host_info[limit_start:limit_start+limit]

            for data in host_info:
                data_dict = model_to_dict(data)
                result_list.append(data_dict)
        return self.write(dict(code=0, msg='获取成功', count=count,data=result_list))



    def post(self):
        ebs_list = []
        mc = MyCryptV2()
        aws_configs_list = get_configs()
        if not aws_configs_list:
            ins_log.write_log('error', '没有获取到AWS资产配置信息，跳过')
            return False
        for config in aws_configs_list:
            access_id = config.get('access_id')
            access_key = mc.my_decrypt(config.get('access_key'))  # 解密后使用
            region = config.get('region')
            default_admin_user = config.get('default_admin_user')
            client = boto3.client('ec2',region_name=region, aws_access_key_id=access_id,
                                   aws_secret_access_key=access_key)
            paginator = client.get_paginator('describe_volumes')
            page_iterator = paginator.paginate()
            filtered_iterator = page_iterator.search("Volumes[]") 
            for i in filtered_iterator:
                if i['Attachments'] == []:
                    i['Attachments'] = '磁盘没有被使用'
                    i['CreateTime'] = i['CreateTime'].strftime("%Y-%m-%d")
                    i['Encrypted'] =  'false' if i['Encrypted'] == 0 else 'Trues'
                    print(i)
                    ebs_list.append(i)
        with DBContext('w', None, True) as session:
            session.execute( '''TRUNCATE TABLE Unattach_Ebs''' )
            session.bulk_insert_mappings(Unattach_Ebs,ebs_list)  
            session.commit()         
        self.write(dict(code=0, msg='获取并写入成功'))


ebs_urls = [
    (r"/v1/cmdb/ebs/",EbsHandler),
]
            
