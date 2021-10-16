import csv
import decimal
from datetime import datetime, timedelta
from websdk.consts import const
from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.db import AWSRiUsageReport, AwsTaskQueue, AWSRiDateDB
from models.db import model_to_dict
from tornado.web import RequestHandler


class RiUsageTodayHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        pageNum = int(self.get_argument('pageNum', default='1', strip=True))
        pageSize = int(self.get_argument('pageSize', default='10', strip=True))
        key = self.get_argument('key', default=None, strip=True)
        export_csv = self.get_argument('export_csv', default="0", strip=True)
        d = datetime.now().strftime('%Y-%m-%d')
        d_start = d + ' 00:00:00'
        d_end = d + ' 23:59:59'
        if not 5 <= pageSize <= 100:
            return self.write(dict(code=400, msg='pageSize只能介于5和100之间。'))

        if not 0 < pageNum:
            return self.write(dict(code=400, msg='pageSize只能介于5和100之间。'))

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            data = session\
                .query(AWSRiUsageReport)\
                .filter(AWSRiUsageReport.date >= d_start)\
                .filter(AWSRiUsageReport.date <= d_end)
            if key is not None:
                data = data.filter(AWSRiUsageReport.platform.like("%" + key + "%"))
            data = data.all()
            data_num = session.query(AWSRiDateDB).all()

        usage_list = [model_to_dict(e) for e in data]
        usage_date_numlist = [model_to_dict(e) for e in data_num]
        for i in usage_date_numlist:
            i["total_ri"] = str(decimal.Decimal(i["total_ri"]).quantize(decimal.Decimal('0.00000')))
        total_ri_num = 0
        rotal_running = 0
        for usage in usage_list:
            usage["total_running"] = int(decimal.Decimal(usage["total_running"]).quantize(decimal.Decimal('0.00000')))
            usage["total_ri"] = int(decimal.Decimal(usage["total_ri"]).quantize(decimal.Decimal('0.00000')))
            usage["coverage_rate"] = str(decimal.Decimal(usage["coverage_rate"]).quantize(decimal.Decimal('0.00000')))
            usage["end"] = {}
            total_ri_num +=  usage["total_ri"]
            rotal_running +=  usage["total_running"]
        for ri in usage_date_numlist:
            for usage in usage_list:
                if ri["family"] == usage["family"] and ri["size"] == usage["size"] and ri["platform"] == usage["platform"]:
                    if ri["end"] in usage["end"].keys():
                        usage["end"][ri["end"]] += ri["total_ri"]
                    else:
                        usage["end"].update({ri["end"]:ri["total_ri"]})
        total = len(usage_list)
        pageTotal = (total + pageSize if total % pageSize >= 0 else 0) // pageSize
        pageNum = min([pageNum, pageTotal])
        _pn = pageNum - 1
        ec2_data = usage_list[_pn * pageSize: pageNum * pageSize + 1]
        if export_csv == "1":
            filename = "ri_report.csv"
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


class RiUsageHistoryHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        end_day = datetime.now()
        start_day = end_day - timedelta(days=365)

        end_day = end_day.strftime("%Y-%m-%d")
        start_day = start_day.strftime("%Y-%m-%d")

        start_day = self.get_argument('key', default=start_day, strip=True)
        end_day = self.get_argument('key', default=end_day, strip=True)
        family = self.get_argument('family', default="c5", strip=True)
        size = self.get_argument('size', default="large", strip=True)
        platform = self.get_argument('platform', default="Linux", strip=True)

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            data = session \
                .query(AWSRiUsageReport) \
                .filter(AWSRiUsageReport.date >= start_day) \
                .filter(AWSRiUsageReport.date < end_day) \
                .filter(AWSRiUsageReport.family == family) \
                .filter(AWSRiUsageReport.size == size) \
                .filter(AWSRiUsageReport.platform == platform) \
                .all()
        histories = [model_to_dict(e) for e in data]
        for history in histories:
            history["total_running"] = str(decimal.Decimal(history["total_running"]).quantize(decimal.Decimal('0.00000')))
            history["total_ri"] = str(decimal.Decimal(history["total_ri"]).quantize(decimal.Decimal('0.00000')))
            history["coverage_rate"] = str(decimal.Decimal(history["coverage_rate"]).quantize(decimal.Decimal('0.00000')))
        return self.write(dict(code=0, msg='获取成功', count=len(histories), data=histories))


class UsageAddRiByDayHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self,*args, **kwargs):
        with DBContext('wr', const.DEFAULT_DB_KEY) as session:
            new_db = AwsTaskQueue(
                                task_name="add_ri_usage",
                                date=datetime.now(),
                                status=0)
            session.add(new_db)
            session.commit()
        return self.write(dict(code=0, msg='任务添加成功，后台执行添加ri_usage数据库', ))


class RiUsage30DayHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        end_day = datetime.now()
        start_day = end_day - timedelta(days=30)
        end_day = end_day.strftime("%Y-%m-%d")
        start_day = start_day.strftime("%Y-%m-%d")

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            data = session \
                .query(AWSRiUsageReport) \
                .filter(AWSRiUsageReport.date >= start_day) \
                .filter(AWSRiUsageReport.date < end_day).all()
        histories = [model_to_dict(e) for e in data]
        for history in histories:
            history["total_running"] = str(decimal.Decimal(history["total_running"]).quantize(decimal.Decimal('0.00000')))
            history["total_ri"] = str(decimal.Decimal(history["total_ri"]).quantize(decimal.Decimal('0.00000')))
            history["coverage_rate"] = str(decimal.Decimal(history["coverage_rate"]).quantize(decimal.Decimal('0.00000')))
        date_list = []
        begin_date = datetime.strptime(start_day, "%Y-%m-%d")
        end_date = datetime.strptime(end_day, '%Y-%m-%d')
        while begin_date < end_date:
            date_str = begin_date
            date_list.append(date_str)
            begin_date += timedelta(days=1)
        data_dict ={}
        for i in histories:
            name = i["family"]+"."+i["size"]+"."+i["platform"]
            if name in data_dict.keys():
                data_dict[name].update({i["date"]:i["coverage_rate"]})
            else:
                data_dict.update({name: {}})
                for date in date_list:
                    data_dict[name].update({str(date):None})
                data_dict[name].update({i["date"]: i["coverage_rate"]})
        return self.write(dict(code=0, msg='获取成功', count=len(histories), data=data_dict))


aws_ri_usage_urls = [
    (r"/v1/ri-usage/today/", RiUsageTodayHanlder),
    (r"/v1/ri-usage/history/", RiUsageHistoryHanlder),
    (r"/v1/ri-usage/add/byday/", UsageAddRiByDayHanlder),
    (r"/v1/ri-usage/30day/", RiUsage30DayHanlder),
]

