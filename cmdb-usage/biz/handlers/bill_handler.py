# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
import copy
import decimal
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from functools import reduce
from websdk.consts import const
from settings import settings
from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.db import AwsServiceBillReport, AwsProjectBillReport
from models.db import model_to_dict
from tornado.web import RequestHandler


# 根据服务类型查询资源的月度总账单
class ServerMonthlyBillHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        pageNum = int(self.get_argument('pageNum', default='1', strip=True))
        pageSize = int(self.get_argument('pageSize', default='10', strip=True))
        service_name = self.get_argument('service_name', default=None, strip=True)
        this_month = datetime.now().replace(day=1, minute=0, hour=0, second=0, microsecond=0)
        month = self.get_argument('month', default=None, strip=True)
        export_csv = self.get_argument('export_csv', default="0", strip=True)
        if not month:
            month = this_month
        else:
            month = datetime.strptime(month, '%Y-%m')
        next_month = month + relativedelta(months=+1)
        month = month.strftime("%Y-%m-01 00:00:00")
        next_month = next_month.strftime("%Y-%m-01,00:00:00")
        if not 5 <= pageSize <= 100:
            return self.write(dict(code=-2, msg='pageSize只能介于5和100之间。'))
        if not 0 < pageNum:
            return self.write(dict(code=-2, msg='pageSize只能介于5和100之间。'))

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            bill_data = session.query(AwsServiceBillReport) \
                .filter(AwsServiceBillReport.service_name == service_name,
                        AwsServiceBillReport.bill_date >= month,
                        AwsServiceBillReport.bill_date < next_month,
                        ).all()

        bill_list = [model_to_dict(e) for e in bill_data]
        bill_dict={}
        for bill in bill_list:
            if bill["resource_id"] in bill_dict.keys():
                bill_dict[bill["resource_id"]]["total_cost"] += bill["total_cost"]
            else:
                bill_dict.update({bill["resource_id"]:bill})
                bill_dict[bill["resource_id"]]["total_cost"] += bill["total_cost"]
        bill_list = [v for k,v in bill_dict.items()]
        for bill in bill_list:
            bill["total_cost"] = str(decimal.Decimal(bill['total_cost']).quantize(decimal.Decimal('0.00000')))
            bill["bill_date"]=bill["bill_date"][:7]
        bill_data = bill_list[(pageNum - 1) * pageSize:pageNum * pageSize]
        # 返回数据
        if export_csv == "1":
            import csv
            filename = "ServerMonthlyBill.csv"
            data_dict = bill_list
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
                                   count=len(bill_list),
                                   data=bill_data))

def sum_dict(a,b):
    for key in ["ec2_cost","ebs_cost","snapshot_cost","s3_cost","rds_cost","elasticache_cost","support_cost","t_a_x","aws_total_cost","rounding","credit","no_reserved_ri_cost"]:
        a[key] = sum([float_dict(d.get(key, 0.0)) for d in (a, b)])
    return a

def float_dict(m):
    if m:
        return float(m)
    else:
        return 0

# 根据月份查询所有BU总账单
class BUMonthlyBillHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        pageNum = int(self.get_argument('pageNum', default='1', strip=True))
        pageSize = int(self.get_argument('pageSize', default='10', strip=True))
        bill_date = self.get_argument('bill_date', default=None, strip=True)
        export_csv = self.get_argument('export_csv', default="0", strip=True)
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
            bill_data = session.query(AwsProjectBillReport) \
                .filter(AwsProjectBillReport.bill_date == bill_date,
                        AwsProjectBillReport.aws_total_cost >0
                        ).all()
        bill_list = [model_to_dict(e) for e in bill_data]
        trance_list = settings.get("project")
        for bill in bill_list:
            bill["bill_date"] = bill["bill_date"][:7]
            bill["chinese"]= trance_list.get(bill['userproject'],None)
            for k, v in bill.items():
                if isinstance(v, decimal.Decimal):
                    bill[k] = str(decimal.Decimal(v).quantize(decimal.Decimal('0.00000')))
        add_bill = copy.deepcopy(bill_list)
        if add_bill:
            total  = reduce(sum_dict, add_bill)
            total["userproject"] = "total"
            total["chinese"] = "汇总"
            bill_list.append(total)
        bill_data = bill_list[(pageNum - 1) * pageSize:pageNum * pageSize]
        # 返回数据
        if export_csv == "1":
            import csv
            filename = "buMonthlyBill.csv"
            data_dict = bill_list
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
                                   count=len(bill_list),
                                   data=bill_data))


# 根据资源ID查询月份内资源每日总账单
class ResourceDaylyBillHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        resource_id = self.get_argument('resource_id', default=None, strip=True)
        service_name = self.get_argument('service_name', default=None, strip=True)
        this_month = datetime.now().replace(day=1, minute=0, hour=0, second=0, microsecond=0)
        month = self.get_argument('month', default=None, strip=True)
        if not month:
            month = this_month
        else:
            month = datetime.strptime(month, '%Y-%m')
        next_month = month + relativedelta(months=+1)
        month = month.strftime("%Y-%m-01 00:00:00")
        next_month = next_month.strftime("%Y-%m-01,00:00:00")
        if not resource_id or not service_name:
            return self.write(dict(code=-2, msg='关键参数不能为空'))
        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            bill_data = session.query(AwsServiceBillReport) \
                .filter(AwsServiceBillReport.resource_id == resource_id,
                        AwsServiceBillReport.service_name == service_name,
                        AwsServiceBillReport.bill_date >= month,
                        AwsServiceBillReport.bill_date < next_month,
                        ).all()

        bill_list = [model_to_dict(e) for e in bill_data]
        if bill_list:
            bill_list = sorted(bill_list, key=lambda bill_list: int(bill_list["bill_date"][8:10]))
        for bill in bill_list:
            bill["total_cost"] = str(decimal.Decimal(bill['total_cost']).quantize(decimal.Decimal('0.00000')))
        # 返回数据
        return self.write(dict(code=0,
                               msg='获取成功',
                               count=len(bill_list),
                               data=bill_list))


# 根据BU查询其各个服务的每日总账单
class BUServerDaylyBillHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        userproject = self.get_argument('userproject', default=None, strip=True)
        this_month = datetime.now().replace(day=1, minute=0, hour=0, second=0, microsecond=0)
        month = self.get_argument('month', default=None, strip=True)
        if not month:
            month = this_month
        else:
            month = datetime.strptime(month, '%Y-%m')
        next_month = month + relativedelta(months=+1)
        month = month.strftime("%Y-%m-01 00:00:00")
        next_month = next_month.strftime("%Y-%m-01 00:00:00")
        if not userproject:
            return self.write(dict(code=-2, msg='关键参数不能为空'))

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            bill_data = session.query(AwsServiceBillReport) \
                .filter(AwsServiceBillReport.userproject == userproject,
                        AwsServiceBillReport.bill_date >= month,
                        AwsServiceBillReport.bill_date < next_month,
                        ).all()
        bill_list = [model_to_dict(e) for e in bill_data]
        for bill in bill_list:
            bill["total_cost"] = str(decimal.Decimal(bill['total_cost']).quantize(decimal.Decimal('0.00000')))
        date_list = []
        begin_date = datetime.strptime(month, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(next_month, '%Y-%m-%d %H:%M:%S')
        while begin_date < end_date:
            date_str = begin_date
            date_list.append(str(date_str)[:10])
            begin_date += timedelta(days=1)
        server_list = ["EC2", "ElastiCache", "RDS", "EBS"]
        bill_data = {}
        for i in server_list:
            bill_data.update({i: {}})
            for j in date_list:
                bill_data[i].update({str(j): None})

        for i in bill_list:
            i["bill_date"] = i["bill_date"][:10]
            if i["service_name"] in server_list:
                if i["bill_date"] in bill_data[i["service_name"]].keys():
                    if bill_data[i["service_name"]][i["bill_date"]] == None:
                        bill_data[i["service_name"]][i["bill_date"]] = 0
                    bill_data[i["service_name"]][i["bill_date"]] += float(i["total_cost"])
                else:
                    bill_data[i["service_name"]][i["bill_date"]] = float(i["total_cost"])

        return self.write(dict(code=0,
                               msg='获取成功',
                               count=len(bill_data),
                               data=bill_data))


# 有已知项目在年度内每个月的费用信息。
class BUProjectYearBillHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        this_year = datetime.now().replace(month=1, day=1, minute=0, hour=0, second=0, microsecond=0)
        year = self.get_argument('year', default=None, strip=True)
        if not year:
            year = this_year
        else:
            year = datetime.strptime(year, '%Y')
        next_year = datetime(year.year + 1, 1, 1)
        year = year.strftime("%Y-%m-01 00:00:00")
        next_year = next_year.strftime("%Y-01-01 00:00:00")
        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            bill_data = session.query(AwsProjectBillReport) \
                .filter(
                AwsProjectBillReport.bill_date >= year,
                AwsProjectBillReport.bill_date < next_year,
            ).all()
        bill_list = [model_to_dict(e) for e in bill_data]
        for bill in bill_list:
            for k, v in bill.items():
                if isinstance(v, decimal.Decimal):
                    bill[k] = str(decimal.Decimal(v).quantize(decimal.Decimal('0.00000')))
        #获取月份列表
        month_list = []
        begin_date = datetime.strptime(year, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(next_year, '%Y-%m-%d %H:%M:%S')
        while begin_date < datetime(end_date.year, 1, 1) - timedelta(days=1):
            date_str = begin_date
            month_list.append(date_str)
            if begin_date.month + 1 <= 12:
                begin_date = datetime(begin_date.year, begin_date.month + 1, 1)
            else:
                break
        #组织返回的数据结构
        bill_dict = {}
        for i in bill_list:
            if i["userproject"] in bill_dict.keys():
                bill_dict[i["userproject"]].update({i["bill_date"]:i["aws_total_cost"]})
            else:
                bill_dict.update({i["userproject"]:{}})
                for month in month_list:
                    bill_dict[i["userproject"]].update({str(month):None})
                bill_dict[i["userproject"]].update({i["bill_date"]:i["aws_total_cost"]})

        return self.write(dict(code=0,
                               msg='获取成功',
                               count=len(bill_dict),
                               data=bill_dict))

bill_urls = [
    (r"/v1/usage/bill/server/monthly/", ServerMonthlyBillHanlder),
    (r"/v1/usage/bill/bu/monthly/", BUMonthlyBillHanlder),
    (r"/v1/usage/bill/resource/dayly/", ResourceDaylyBillHanlder),
    (r"/v1/usage/bill/buserver/dayly/", BUServerDaylyBillHanlder),
    (r"/v1/usage/bill/project/Year/", BUProjectYearBillHanlder),
]
