#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
date   : 2017-10-11
role   : Application
"""
from biz.handlers.ri_rds_handler import rds_urls
from biz.handlers.ri_elasticache_handler import elasticache_urls
from websdk.application import Application as myApplication
from biz.handlers.resource_usage_handler import ec2_usage_urls
from biz.handlers.ri_usage_handler import aws_ri_usage_urls
from biz.handlers.bill_handler import bill_urls
from biz.handlers.bill_budget_handler import bill_budget_urls
from biz.handlers.asset_idc_handler import asset_idc_urls


class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(ec2_usage_urls)
        urls.extend(aws_ri_usage_urls)
        urls.extend(bill_urls)
        urls.extend(rds_urls)
        urls.extend(bill_budget_urls)
        urls.extend(asset_idc_urls)
        urls.extend(elasticache_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
