#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 17:37
# @Author : jianxlin
# @Site : 
# @File : aws.py
# @Software: PyCharm

from boto3 import session
from libs.config import config


class AWS(object):
    ServiceName = "ec2"

    def __init__(self, *args, **kwargs):
        try:
            self._session = session.Session(**config.get_aws_conf())
        except Exception as e:
            self._session = session.Session()
        self.client = self._session.client(service_name=self.ServiceName)
        self.resource = self._session.resource(service_name=self.ServiceName)
