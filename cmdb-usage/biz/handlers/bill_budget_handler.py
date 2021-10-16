# -*- coding: utf-8 -*-
# @Time    : 2020/10/10
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

import decimal
from datetime import datetime, timedelta

from libs.aws.bill import update_project_budget, get_project_budget
from websdk.consts import const
from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.db import AwsProjectBudgetControl
from models.db import model_to_dict
from tornado.web import RequestHandler


class BillBudgetHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        pageNum = int(self.get_argument('pageNum', default='1', strip=True))
        pageSize = int(self.get_argument('pageSize', default='10', strip=True))
        bill_date = self.get_argument('bill_date', default=None, strip=True)
        if not bill_date:
            return self.write(dict(code=-2, msg='关键参数不能为空'))
        # 判断pageSize合法性
        if not 5 <= pageSize <= 100:
            return self.write(dict(code=-2, msg='pageSize只能介于5和100之间。'))
        # 判断pageNum合法性
        if not 0 < pageNum:
            return self.write(dict(code=-2, msg='pageSize只能介于5和100之间。'))
        bill_date = datetime.strptime(bill_date, '%Y-%m')
        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            bill_data = session.query(AwsProjectBudgetControl) \
                .filter(AwsProjectBudgetControl.bill_date == bill_date,
                        ).all()

        bill_list = [model_to_dict(e) for e in bill_data]
        for bill in bill_list:
            bill["bill_date"] = bill["bill_date"][:7]
            for k, v in bill.items():
                if isinstance(v, decimal.Decimal):
                    bill[k] = str(decimal.Decimal(v).quantize(decimal.Decimal('0.00000')))
        bill_data = bill_list[(pageNum - 1) * pageSize:pageNum * pageSize]
        return self.write(dict(code=0,
                               msg='获取成功',
                               count=len(bill_list),
                               data=bill_data))

    def post(self, *args, **kwargs):
        userproject = self.get_argument('userproject', default=None, strip=True)
        bill_date = self.get_argument('bill_date', default=None, strip=True)
        aws_budget_cost = self.get_argument('aws_budget_cost', default=None, strip=True)
        aws_alert_percentage = self.get_argument('aws_alert_percentage', default=None, strip=True)
        bill_date = bill_date + "-01 00:00:00"
        with DBContext('w') as session:
            session.query(AwsProjectBudgetControl) \
                .filter(AwsProjectBudgetControl.bill_date == bill_date,
                        AwsProjectBudgetControl.userproject == userproject,
                        ).update({
                AwsProjectBudgetControl.aws_budget_cost: decimal.Decimal(aws_budget_cost),
                AwsProjectBudgetControl.aws_alert_percentage: decimal.Decimal(aws_alert_percentage),

            })
            session.commit()
        update_project_budget()
        return self.write(dict(msg='修改成功'))


class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        get_project_budget()
        update_project_budget()
        return "测试中"

bill_budget_urls = [
    (r"/v1/usage/bill/budget/", BillBudgetHanlder),
    (r"/v1/usage/bill/budget/test/", ApiTest),
]
