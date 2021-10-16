#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-03-19 11:20
# @Author : jianxlin
# @Site :
# @File : __init__.py.py
# @Software: PyCharm
from datetime import datetime

from settings import settings
from libs.aws.session import get_aws_session


# 继承并重写python的dict对象
class UserDict(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, item):
        assert item in self.keys()
        return self[item]

    def __setattr__(self, key, value):
        raise Exception


# 定义保留实例的数据结构
class ReservedInstance(UserDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update(kwargs)


class Ec2Instance(UserDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # 把platform方法包装成属性
    @property
    def Platform(self):
        p = self.get("Platform", None)
        return "Linux/UNIX" if p is None else "Windows BYOL"


class Image(UserDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AwsEc2Client(object):
    def __init__(self):
        self._session = get_aws_session(**settings.get("aws_key"))
        self._client = self._session.client('ec2')

    def get_ec2_list(self):
        # 返回ec2实例信息的列表生成器
        return [
            Ec2Instance(**i)
            for r in self._client.describe_instances()["Reservations"]
            for i in r["Instances"]
        ]

    def get_reserved_instances(self):
        # 返回ec2保留实例信息的列表生成器
        return [
            ReservedInstance(**ri)
            for ri in self._client.describe_reserved_instances()["ReservedInstances"] if
            ri["End"].replace(tzinfo=None) > datetime.now()
        ]

    def get_images(self):
        # 返回所有映像信息的列表生成器
        return [
            Image(**img)
            for img in self._client.describe_images()["Images"]
        ]


if __name__ == '__main__':
    aec = AwsEc2Client()
    ris = aec.get_ec2_list()
