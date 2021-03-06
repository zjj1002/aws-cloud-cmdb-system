
from libs.aws.tags import ForDangersHandler,get_configs
from websdk.web_logs import ins_log
from sqlalchemy import or_,exc
from websdk.db_context import DBContext
from models.db import Security_Host
from models.db import DBTag, DB, model_to_dict
from opssdk.operate import MyCryptV2
from libs.base_handler import BaseHandler
from tornado.web import RequestHandler, HTTPError
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import json

class DangersOpenPortHandler(BaseHandler):
#class DangersOpenPortHandler(RequestHandler): ##测试之用
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def AwsQueryRiskPort(self,Aws_host_API_result):
        all_instance_risk_pair = {}  ## 数据库里有，但是AWS无的情况下 轮询用
        all_values = []   ## 如果第一次 从来没有写入过数据库的时候用
        host_list = Aws_host_API_result
        for instance_str in host_list.keys():
                        instance = eval(instance_str)
                        for port in instance['security_group']:
                            sg_group_description = host_list[instance_str].client.describe_security_groups(GroupIds = [port['GroupId']])##去重时候的字典的value
                            for groups in sg_group_description['SecurityGroups']:
                                for ip in groups['IpPermissions']:
                                    if ip['IpRanges'] == [{'CidrIp': '0.0.0.0/0'}]:
                                        instance['risk_port'].append(ip['FromPort'])
                        instance['risk_port'] = str(','.join('%s' % port for port in instance['risk_port'])) 
                        if instance['risk_port'] == '':
                            continue
                        instance['security_group'] = str(instance['security_group'])
                        all_values.append(instance)
                        all_instance_risk_pair[instance['server_instance_id']] = instance['risk_port']
        return all_instance_risk_pair,all_values


    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = int(self.get_argument('limit', default=15, strip=True))
        export_csv = self.get_argument('export_csv', default="0", strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        result_list = []

        with DBContext('r') as session:
            if key:
                # 模糊查所有
                host_info = session.query(Security_Host).filter(or_(Security_Host.server_name.like('%{}%'.format(key)),
                                                         Security_Host.server_instance_id.like('%{}%'.format(key)),
                                                         Security_Host.server_private_ip.like('%{}%'.format(key)),
                                                         Security_Host.server_public_ip.like('%{}%'.format(key)),
                                                         Security_Host.server_Project.like('%{}%'.format(key)),
                                                         Security_Host.server_mark.like('%{}%'.format(key)),
                                                         Security_Host.security_state.like('%{}%'.format(key)),
                                                         Security_Host.risk_port.like('%{}%'.format(key)),
                                                         Security_Host.security_group.like('%{}%'.format(key)))).order_by(Security_Host.id)
                count = host_info.count()
            else:
                host_info = session.query(Security_Host).order_by(Security_Host.id)
                count = host_info.count()

            host_info = host_info[limit_start:limit_start+limit]

            for data in host_info:
                data_dict = model_to_dict(data)
                if data_dict["risk_port"] == "-1":
                    data_dict["is_allow_icmpicmpv6"] = "1"
                    data_dict["risk_port"] = ""
                else:
                    data_dict["is_allow_icmpicmpv6"] = "0"
                result_list.append(data_dict)
        if export_csv == "1":
            import csv
            filename = "DangersOpenPort.csv"
            data_dict = result_list
            headers = [list(i.keys()) for i in data_dict][0]
            rows = [list(i.values()) for i in data_dict]
            with open(filename, "w", encoding="utf8", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + filename)
            buf_size = 4096
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(buf_size)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        else:
            return self.write(dict(code=0, msg='获取成功', count=count,data=result_list))


    @gen.coroutine
    def post(self):
        host_list = {}
        mc = MyCryptV2()
        aws_configs_list = get_configs()
        if not aws_configs_list:
            ins_log.write_log('error', '没有获取到AWS资产配置信息，跳过')
            self.write(dict(code=0, msg='没有获取到AWS资产配置信息，跳过'))
        for config in aws_configs_list:
            access_id = config.get('access_id')
            access_key = mc.my_decrypt(config.get('access_key'))  # 解密后使用
            region = config.get('region')
            default_admin_user = config.get('default_admin_user')

            obj = ForDangersHandler(access_id, access_key, region, default_admin_user)
            server_info = obj.get_server_info()
            for msg in server_info:
                if not host_list.get(str(msg)):
                    host_list[str(msg)] = obj## 字典去重 可能会有两个相同权限的ak/sk
        if not host_list:
            ins_log.read_log('info', 'Not fount server info...')
            print('Not Fount Server Info')
            self.write(dict(code=0, msg='没有从AWS接口里读到信息，跳过'))
        else:
            with DBContext('r') as session:
                try:
                    session.query(Security_Host).delete()
                    session.commit()
                except:
                    session.rollback()
                db_record = session.query(Security_Host.server_instance_id,Security_Host.risk_port)
                all_instance_risk_pair,all_values = yield self.AwsQueryRiskPort(host_list)
                if db_record.count() != 0:
                    for ins in db_record:
                        if ins.server_instance_id in all_instance_risk_pair.keys(): ##数据库查到的是否在从aws取到的ID列表里
                            if ins.risk_port != all_instance_risk_pair[ins.server_instance_id]:##如果查询后发现从aws取到的风险端口和数据库存的不一致，则updates
                                session.query(Security_Host).filter(Security_Host.server_instance_id == ins.server_instance_id).update({Security_Host.risk_port: all_instance_risk_pair[ins.server_instance_id]})
                                session.commit()
                                del all_instance_risk_pair[ins.server_instance_id]
                            else:  ##如果一致 则什么都不做
                                del all_instance_risk_pair[ins.server_instance_id]  ## 只要在数据库有记录的都删了 只剩下数据里没的机器 给另外一个维度的轮询用
                        else: ###如果数据库里查到的 不在aws里，证明这个机器已经在aws端被删除，需要在数据库里删除
                            ins_log.write_log('warning', 'no exist server will  Deleted...%s' % ins.server_instance_id)
                            session.query(Security_Host).filter(Security_Host.server_instance_id == ins.server_instance_id).delete(synchronize_session=False)
                            session.commit()
                else:##数据库里无记录
                    session.bulk_insert_mappings(Security_Host,all_values)   
                    session.commit()
                    all_instance_risk_pair.clear()

                if  all_instance_risk_pair:##如果没被删空
                    miss_instance = [i for i in all_values if i['server_instance_id'] in all_instance_risk_pair] 
                    print(len(miss_instance))               
                    session.bulk_insert_mappings(Security_Host,miss_instance)  
                    session.commit()       ##AWS云里有 但是数据库里没的部分           
        self.write(dict(code=0, msg='获取并写入成功'))

    def put(self,*args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        remark = data.get('mark')
        instance_id = data.get('id')
        state = data.get('state')

        ins_log.read_log("info", remark+"||||"+state+"||||"+instance_id)

        if not remark or not state:
            return self.write(dict(code=-1, msg='mark内容和状态内容都不能为空'))
        with DBContext('w', None) as session:
            session.query(Security_Host).filter(Security_Host.server_instance_id == instance_id).update({Security_Host.server_mark: remark, Security_Host.security_state: state})
            session.commit()

        self.write(dict(code=0, msg='修改成功')) 


security_host_urls = [
    (r"/v1/cmdb/dangers/",DangersOpenPortHandler),
]
            
