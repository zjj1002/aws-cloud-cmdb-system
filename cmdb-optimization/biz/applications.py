#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
date   : 2017-10-11
role   : Application
"""

from biz.handlers.asset_eip_handler import eip_host_urls
from websdk.application import Application as myApplication
from biz.handlers.rds_handler import aws_rds_urls
from biz.handlers.nat_handler import aws_nat_urls
from biz.handlers.elb_handler import aws_elb_urls
from biz.handlers.ebs_handler import aws_ebs_urls


class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(eip_host_urls)
        urls.extend(aws_rds_urls)
        urls.extend(aws_nat_urls)
        urls.extend(aws_elb_urls)
        urls.extend(aws_ebs_urls)
        super(Application, self).__init__(urls, **settings)

if __name__ == '__main__':
    pass
