#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
date   : 2017-10-11
role   : Application
"""
from websdk.application import Application as myApplication

from biz.handlers.all_assets_handler import all_assets_host_urls
from biz.handlers.asset_server_handler import asset_server_urls
from biz.handlers.asset_db_handler import asset_db_urls
from biz.handlers.admin_user_handler import admin_user_urls
from biz.handlers.asset_tag_handler import tag_urls
from biz.handlers.asset_tag_result_handler import tag_result_host_urls
from biz.handlers.switch_ec2_instance_handler import ec2_instance_host_urls
from biz.handlers.system_user_handler import system_user_urls
from biz.handlers.asset_configs_handler import asset_configs_urls
from biz.handlers.hand_update_asset_handler import asset_hand_server_urls
from biz.handlers.aws_events_handler import aws_events_urls
from biz.handlers.asset_idc_handler import asset_idc_urls
from biz.handlers.asset_operational_audit_handler import asset_audit_urls
from biz.handlers.dangers_opened_port_host_handler import security_host_urls
from biz.handlers.asset_s3_handler import s3_host_urls
from biz.handlers.aws_ebs_handler import ebs_urls
from biz.handlers.asset_dns_handler import dns_host_urls
from biz.handlers.tag_manage_handler import tag_manage_host_urls
from biz.handlers.tag_services_handler import tag_services_host_urls
from biz.handlers.user_manage_handler import user_manage_host_urls
from biz.handlers.asset_elasticache_handler import asset_elasticache_urls
from biz.handlers.asset_elasticsearch_handler  import asset_elasticsearch_urls

class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(security_host_urls)
        urls.extend(asset_server_urls)
        urls.extend(asset_db_urls)
        urls.extend(admin_user_urls)
        urls.extend(tag_urls)
        urls.extend(system_user_urls)
        urls.extend(asset_configs_urls)
        urls.extend(asset_hand_server_urls)
        urls.extend(aws_events_urls)
        urls.extend(asset_idc_urls)
        urls.extend(asset_audit_urls)
        urls.extend(s3_host_urls)
        urls.extend(ebs_urls)
        urls.extend(dns_host_urls)
        urls.extend(all_assets_host_urls)
        urls.extend(tag_manage_host_urls)
        urls.extend(tag_result_host_urls)
        urls.extend(tag_services_host_urls)
        urls.extend(ec2_instance_host_urls)
        urls.extend(user_manage_host_urls)
        urls.extend(asset_elasticache_urls)
        urls.extend(asset_elasticsearch_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
