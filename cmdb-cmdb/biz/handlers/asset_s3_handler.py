from libs.common import data_sort
from websdk.web_logs import ins_log
from sqlalchemy import or_, exc
from websdk.db_context import DBContext
from models.s3 import S3, model_to_dict
from opssdk.operate import MyCryptV2
from libs.base_handler import BaseHandler
from tornado.web import RequestHandler, HTTPError
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from libs.aws.s3 import main as s3_refresh
import json
import datetime

class S3BucketHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)


    @run_on_executor
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = int(self.get_argument('limit', default=15, strip=True))
        limit_start = (int(page_size) - 1) * int(limit)
        result_list = []

        with DBContext('r') as session:
            if key:
            # 模糊查所有
                bucket_info = session.query(S3).filter(or_(S3.bucket_name.like('%{}%'.format(key)))).order_by(S3.id).all()
            else:
                bucket_info = session.query(S3).order_by(S3.id).all()

        #    bucket_info = bucket_info.limit(limit).offset(limit_start)
            count = len(bucket_info)
            bucket_info = [model_to_dict(e) for e in bucket_info]
            bucket_info = data_sort(bucket_info, "bucket_name")
            bucket_info = bucket_info[limit_start:limit_start+limit]

            for data_dict in bucket_info:
                data_dict['create_time'] = data_dict['create_time'].strftime("%Y-%m-%d %H:%M:%S") if \
                    isinstance(data_dict['create_time'],datetime.datetime) else data_dict['create_time']
                data_dict['update_time'] = data_dict['update_time'].strftime("%Y-%m-%d %H:%M:%S")  if \
                    isinstance(data_dict['update_time'],datetime.datetime) else data_dict['update_time']
                data_dict["size"] = round(float(data_dict.get("size",0)),2)
                result_list.append(data_dict)

        return self.write(dict(code=0, msg='获取成功', data=result_list, count=count))


    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        status = data.get('status')
        s3_name = data.get('name')
        remark = data.get('remark')
        

        if not remark:
            return self.write(dict(code=-1, msg='mark内容不能为空'))

        ins_log.read_log("info", s3_name)
        with DBContext('w', None) as session:
            session.query(S3).filter(S3.bucket_name == s3_name).update({
                S3.bucket_remark: remark, S3.bucket_mark:int(status)})
            session.commit()

        self.write(dict(code=0, msg='修改成功'))

class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        s3_refresh()
        return self.write({"test":"sucess"})

s3_host_urls = [
    (r"/v1/cmdb/s3/", S3BucketHandler),
    (r"/v1/cmdb/s3/test/", ApiTest),
]

