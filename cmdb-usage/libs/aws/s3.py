#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:21
# @Author : jianxlin
# @Site : 
# @File : s3.py
# @Software: PyCharm

from libs.aws.aws import AWS
from libs.config import config


class S3(AWS):
    ServiceName = "s3"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def download_cbr(self, *args, **kwargs):
        """
            下载账单文件。
        :param args:
        :param kwargs:
        :return:
        """
        self.resource.meta.client.download_file(config.aws_s3_bucket_name,
                                                config.cloud_bill_record,
                                                config.cloud_bill_record_path)


if __name__ == '__main__':
    s3 = S3()
    s3.download_cbr()
