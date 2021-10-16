#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-03-19 11:20
# @Author : jianxlin
# @Site :
# @File : __init__.py.py
# @Software: PyCharm


import logging
from libs.aws.session import get_aws_session
from settings import settings

#根据ec2_Id获取ec2实例信息
def get_ec2_resource(ec2_id=None):
    assert ec2_id is not None
    s = get_aws_session(**settings.get("aws_key"))
    ec2 = s.resource('ec2')
    instance = ec2.Instance(ec2_id)
    return instance

#根据image_Id获取映像信息
def get_image_resource(image_id=None):
    assert image_id is not None
    s = get_aws_session(**settings.get("aws_key"))
    ec2 = s.resource('ec2')
    image = ec2.Image(image_id)
    return image


if __name__ == '__main__':
    er = get_image_resource("")
    logging.info(er.platform)
    logging.info(er.id)
