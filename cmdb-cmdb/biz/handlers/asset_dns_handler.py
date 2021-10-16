from biz.ds.ds_elb import main
from libs.common import data_sort
from websdk.web_logs import ins_log
from sqlalchemy import or_, exc
from websdk.db_context import DBContext
from models.dns import Dns, model_to_dict
from models.elb import ElbDB
from models.elb import model_to_dict as model_to_dict_2
from opssdk.operate import MyCryptV2
from libs.base_handler import BaseHandler
from tornado.web import RequestHandler, HTTPError
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import json

class DnsHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        main_dns = self.get_argument('main_dns', default="jncapp.cn", strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = int(self.get_argument('limit', default=15, strip=True))
        limit_start = (int(page_size) - 1) * int(limit)
        result_list = []

        with DBContext('r') as session:
            if key:
            # 模糊查所有
                dns_info = session.query(Dns).filter(Dns.dns_name.like('%{}%'.format(key)),Dns.dns_name.like('%{}'.format(main_dns))).order_by(Dns.id).all()
            else:
                dns_info = session.query(Dns).filter(Dns.dns_name.like('%{}'.format(main_dns))).order_by(Dns.id).all()

            count = len(dns_info)
            dns_info = [model_to_dict(e) for e in dns_info]
            dns_info = data_sort(dns_info, "dns_name")
            dns_info = dns_info[limit_start:limit_start+limit]

            for data_dict in dns_info:
                instance_info = session.query(ElbDB).filter(ElbDB.dnsname== data_dict['dns_value']).first()
                data_dict["instances"] =None
                if instance_info:
                    instance_info = model_to_dict_2(instance_info)
                    data_dict["instances"] = instance_info["instance"]
                result_list.append(data_dict)
            #查询instance
        return self.write(dict(code=0, msg='获取成功', data=result_list, count=count))


    # def put(self, *args, **kwargs):
    #     data = json.loads(self.request.body.decode("utf-8"))
    #     status = data.get('status')
    #     s3_name = data.get('name')
    #     remark = data.get('remark')
        

    #     if not remark:
    #         return self.write(dict(code=-1, msg='mark内容不能为空'))

    #     ins_log.read_log("info", s3_name)
    #     with DBContext('w', None) as session:
    #         session.query(S3).filter(S3.bucket_name == s3_name).update({
    #             S3.bucket_remark: remark, S3.bucket_mark:int(status)})
    #         session.commit()

    #     self.write(dict(code=0, msg='修改成功'))


class MainDnsHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def get(self, *args, **kwargs):
        result_list = []
        with DBContext('r') as session:
            dns_info = session.query(Dns).order_by(Dns.id).all()
            for data in dns_info:
                data_dict = model_to_dict(data)
                result_list.append(data_dict)
        result_list = list(set([".".join(i["dns_name"].split(".")[-2:]) for i in result_list]))
        return self.write(dict(code=0, msg='获取成功', data=result_list, count=len(result_list)))

class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        main()
        return self.write("test")


dns_host_urls = [
    (r"/v1/cmdb/dns/", DnsHandler),
    (r"/v1/cmdb/main_dns/", MainDnsHandler),
    (r"/v1/cmdb/main_dns/test/", ApiTest),
]

