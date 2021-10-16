#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 13:16

# @File    : resource_usage_handler.py
# @Role    : 系统用户
import decimal
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from biz.timed_program import update_usage_report
from websdk.consts import const
from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.db import UsageReport, AwsTaskQueue
from models.db import ResourceUsage
from models.db import model_to_dict
from tornado.web import RequestHandler

#显示某一个月的ec2资源使用情况
class ResourceUsageHanlder(BaseHandler):
    #处理get请求
    def get(self, *args, **kwargs):
        usage_data = []
        #获取当前月份1号日期信息
        this_month = datetime.now().replace(day=1, minute=0, hour=1, second=0, microsecond=0)
        #获取get请求的ec2_id参数
        ec2_id = self.get_argument('ec2_id', default=None, strip=True)
        # 获取get请求的mouth参数
        month = self.get_argument('month', default=None, strip=True)
        #判断get请求是否是查询具体某一个月的信息，如果没有就设置为当前月
        if not month:
            month = this_month
        else:
            month = datetime.strptime(month, '%Y-%m')
        #获取month的下个月当天
        next_month = month + relativedelta(months=+1)
        month = month.strftime("%Y-%m-01")
        #去除时间 到天
        next_month = next_month.strftime("%Y-%m-01")
        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            # 判断get请求是否是查询具体某一个ec2的信息，如果没有就查UsageReport表单的第一个
            if not ec2_id:
                ec2 = session.query(UsageReport).filter(UsageReport.month == month).first()
            else:
                ec2 = session.query(UsageReport).filter(UsageReport.month == month,
                                                        UsageReport.ec2_id == ec2_id).first()
            if ec2:
                #根据上面得到的ec2 去ResourceUsage表查询具体的使用情况 并过滤月份
                usage_data = session.query(ResourceUsage) \
                    .filter(ResourceUsage.ec2_id == ec2.ec2_id,
                            ResourceUsage.date >= month,
                            ResourceUsage.date < next_month,
                            ).all()
        ec2_data =  model_to_dict(ec2) if ec2 else None
        ec2_data["cost_gap"] = str(decimal.Decimal(ec2_data['cost_gap']).quantize(decimal.Decimal('0.00000')))
        usage_detail = {
            'ec2_info': ec2_data,
            'usage_list': [model_to_dict(u) for u in usage_data]
        }
        #返回数据
        return self.write(dict(code=0, msg='获取成功', count=len(usage_detail), data=usage_detail))

#显示某一个月的所有ec2资源使用报告单情况(可以筛选时间和页数)
class UsageReportHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        month_default = datetime.now().strftime('%Y-%m-01')#当前月份的的1号 格式：2020-06-01
        month = self.get_argument('month', default=month_default, strip=True)
        pageNum = int(self.get_argument('pageNum', default='1', strip=True))
        pageSize = int(self.get_argument('pageSize', default='10', strip=True))
        key = self.get_argument('key', default=None, strip=True)
        export_csv = self.get_argument('export_csv', default="0", strip=True)
        #判断pageSize合法性
        if not 5 <= pageSize <= 100:
            return self.write(dict(code=400, msg='pageSize只能介于5和100之间。'))
        # 判断pageNum合法性
        if not 0 < pageNum:
            return self.write(dict(code=400, msg='pageSize只能介于5和100之间。'))

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            #过滤要显示的月份
            ec2_data = session.query(UsageReport).filter(UsageReport.month == month)
            #模糊查询key值处理
            if key is not None:
                ec2_data = ec2_data.filter(UsageReport.host_name.like("%" + key + "%"))
            ec2_data = ec2_data.all()
        #处理页码和每页显示条数
        ec2_list = [model_to_dict(e) for e in ec2_data]
        total = len(ec2_list)
        pageTotal = (total + pageSize if total % pageSize > 0 else 0) // pageSize
        ec2_data = ec2_list[(pageNum - 1) * pageSize:pageNum * pageSize]
        for ec2 in ec2_data:
            ec2["cost_gap"] = str(decimal.Decimal(ec2['cost_gap']).quantize(decimal.Decimal('0.00000')))
        if export_csv == "1":
            import csv
            filename = "UsageReport.csv"
            data_dict = ec2_data
            headers = [list(i.keys()) for i in data_dict][0]
            rows = [list(i.values()) for i in data_dict]
            with open(filename, "w", encoding="utf8", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + filename)
            buf_size = 4096
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(buf_size)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        else:
            return self.write(dict(code=0,
                                   msg='获取成功',
                                   count=total,
                                   pageTotal=pageTotal,
                                   data=ec2_data))

#显示所有资源报告单的月份 并排序
class UsageReportMonthsHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        month_list = []
        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            month_data = session.query(UsageReport).all()
        for m in month_data:
            month = m.month.strftime('%Y-%m-01 00:00:00')
            if month not in month_list:
                month_list.append(month)
        month_list.sort()
        return self.write(dict(code=0, msg='获取成功', count=len(month_list), data=month_list))

class UsageReportOneDayHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self,*args, **kwargs):
        date_period = self.get_body_argument('date_period', strip=True)
        if not date_period:
            return self.write(dict(code=-1, msg='传入时间段为空'))
        date = date_period.split('--')
        date_list = []
        begin_date = datetime.strptime(date[0], "%Y-%m-%d")
        end_date = datetime.strptime(date[1], '%Y-%m-%d')
        if end_date < begin_date:
            return self.write(dict(code=-1, msg='时间段不合法'))
        while begin_date <= end_date:
            date_str = begin_date
            date_list.append(date_str)
            begin_date += timedelta(days=1)
        task_list=[]
        for day_time in date_list:
            task_name = "add_usage"
            task_list.append({"task_name":task_name,
                              "date":day_time,
                              "status":0
                              })

        with DBContext('wr', const.DEFAULT_DB_KEY) as session:
            for task in task_list:
                new_db = AwsTaskQueue(
                                    task_name=task.get('task_name'),
                                      date=task.get('date'),
                                      status=task.get('status'))
                session.add(new_db)
                session.commit()
        return self.write(dict(code=0, msg='任务添加成功，后台执行添加usage数据库', ))


class UsageAddBillByDay(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        date_period = self.get_body_argument('date_period', strip=True)
        if not date_period:
            return self.write(dict(code=-1, msg='传入时间段为空'))
        date = date_period.split('--')
        date_list = []
        begin_date = datetime.strptime(date[0], "%Y-%m-%d")
        end_date = datetime.strptime(date[1], '%Y-%m-%d')
        if end_date < begin_date:
            return self.write(dict(code=-1, msg='时间段不合法'))
        while begin_date <= end_date:
            date_str = begin_date
            date_list.append(date_str)
            begin_date += timedelta(days=1)
        task_list = []
        for day_time in date_list:
            task_name = "billing"
            task_list.append({"task_name": task_name,
                              "date": day_time,
                              "status": 0
                              })

        with DBContext('wr', const.DEFAULT_DB_KEY) as session:
            for task in task_list:
                new_db = AwsTaskQueue(
                    task_name=task.get('task_name'),
                    date=task.get('date'),
                    status=task.get('status'))
                session.add(new_db)
                session.commit()
        return self.write(dict(code=0, msg='任务添加成功，后台执行添加账单数据库', ))


#显示主机可以节约费用最多的10台EC2主机列表。
class UsageReportTop10Hanlder(BaseHandler):
    def get(self, *args, **kwargs):
        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            ec2_data = session.query(UsageReport).order_by(UsageReport.cost_gap.desc()).limit(10)
        ec2_list = [model_to_dict(e) for e in ec2_data]
        total = len(ec2_list)
        for ec2 in ec2_list:
            ec2["cost_gap"] = str(decimal.Decimal(ec2['cost_gap']).quantize(decimal.Decimal('0.00000')))
        return self.write(dict(code=0,
                               msg='获取成功',
                               count=total,
                               data=ec2_list))

#测试用 后续会删除---lch
class ApiTest(BaseHandler):
    def get(self, *args, **kwargs):
        update_usage_report()
        return self.write({"msg":"test"})



ec2_usage_urls = [
    (r"/v1/usage/resource/", ResourceUsageHanlder),
    (r"/v1/usage/report/", UsageReportHanlder),
    (r"/v1/usage/report/months/", UsageReportMonthsHanlder),
    (r"/v1/usage/report/day/", UsageReportOneDayHanlder),
    (r"/v1/usage/addbill/byday/", UsageAddBillByDay),
    (r"/v1/usage/report/top10/", UsageReportTop10Hanlder),
    (r"/v1/usage/report/test/", ApiTest),
]
