#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:22
# @Author : jianxlin
# @Site : 
# @File : base.py
# @Software: PyCharm

import pandas as pd
from libs.config import config


class Report(object):
    def __init__(self):
        self._report_file = config.report_path
        self._reports = None
        self._excel = pd.ExcelWriter(self._report_file)

    def append_sheet(self, sheet=None, name=None):
        """
            添加sheet到表格。
        :param sheet:
        :param name:
        :return:
        """
        sheet.to_excel(self._excel, sheet_name=name)

    def save(self):
        """
            生成excel文件
        :return:
        """
        self._excel.save()


if __name__ == '__main__':
    from libs.report.ec2_report import Ec2ReportData

    erd = Ec2ReportData()
    r = Report()
    r.append_sheet(erd.report_data, name="Ec2")
    r.save()
