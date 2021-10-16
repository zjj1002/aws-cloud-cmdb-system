#!/usr/bin/env python
#coding=utf-8
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.dns import Dns
from models.server import AssetConfigs, model_to_dict
from opssdk.operate import MyCryptV2
import fire


# #获取域名列表
# request = DescribeDomainsRequest()
# request.set_accept_format('json')
# response = client.do_action_with_exception(request)
# print(str(response, encoding='utf-8'))

class DnsApi():
    def __init__(self, access_id = '', access_key = '', region = ''):
        self.region = region
        self.access_id = access_id
        self.access_key = access_key

    def get_sub_dns_record(self, domain, page_number=1, page_size=100):
        try:
            client = AcsClient(self.access_id, self.access_key, self.region)
            request = DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(domain)
            request.set_PageNumber(page_number)
            request.set_PageSize(page_size)
            response = client.do_action_with_exception(request)
            return json.loads(str(response, encoding="utf8"))
        except Exception as err:
            print(err)
            return {}
    
    def format_dns_record(self, dns_info):

        if not isinstance(dns_info, dict):
            raise TypeError
        
        dns_list = dns_info.get("DomainRecords",'').get("Record",'')
        asset_data = []
        
        if dns_list:
            for dns in dns_list:
                dns_data = dict()
                dns_data['dns_name']=dns.get('RR') + '.' + dns.get('DomainName')
                dns_data['dns_status'] = dns.get('Status')
                dns_data['dns_type'] = dns.get('Type')
                dns_data['dns_value'] = dns.get('Value')
                dns_data['dns_ttl'] = dns.get('TTL')
                dns_data['dns_remark'] = dns.get('Remark')
                asset_data.append(dns_data)

        return asset_data
  
    def get_all_dns_record(self,all_domains):
        total_results = []
        if all_domains:
            for domain in all_domains:
                sub_domain_results = self.get_sub_dns_record(domain)
                total_results = total_results + (self.format_dns_record(sub_domain_results))
        return total_results

    def sync_cmdb(self,all_domains):

        dns_record_list = self.get_all_dns_record(all_domains)

        if not dns_record_list: 
            return False

        with DBContext('w') as session:
            session.query(Dns).delete()
            for dns in dns_record_list:
                ins_log.read_log('info', 'dns信息：{}'.format(dns))
                new_dns = Dns(dns_name = dns.get('dns_name'),dns_status = dns.get('dns_status'),dns_type = dns.get('dns_type'),dns_value = dns.get('dns_value'),dns_ttl = dns.get('dns_ttl'),dns_remark = dns.get('dns_remark'))
                session.add(new_dns)
            session.commit()

def get_configs():
    """
    get id / key / region info
    :return:
    """

    aliyun_configs_list = []
    with DBContext('r') as session:
        aliyun_configs_info = session.query(AssetConfigs).filter(AssetConfigs.account == '阿里云',
                                                              AssetConfigs.state == 'true').all()
        for data in aliyun_configs_info:
            data_dict = model_to_dict(data)
            data_dict['create_time'] = str(data_dict['create_time'])
            data_dict['update_time'] = str(data_dict['update_time'])
            aliyun_configs_list.append(data_dict)
    return aliyun_configs_list

def main():
    mc = MyCryptV2()
    aliyun_configs_list = get_configs()
    if not aliyun_configs_list:
        ins_log.read_log('error', '没有获取到阿里云资产配置信息，跳过')
        return False
    for config in aliyun_configs_list:
        access_id = config.get('access_id')
        access_key = mc.my_decrypt(config.get('access_key'))  # 解密后使用
        region = config.get('region')

        obj = DnsApi(access_id = access_id,access_key = access_key,region= region)
        obj.sync_cmdb(all_domains = ['jncapp.com','jncapp.cn'])

if __name__ == '__main__':
    fire.Fire(main)

