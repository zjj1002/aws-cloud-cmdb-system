#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
import csv
import decimal
from datetime import datetime, timedelta
from websdk.consts import const
from sqlalchemy import or_
from libs.base_handler import BaseHandler
from models.elasticache_ri_db import RiElastiCache, model_to_dict, AWSElastiCacheRiUsageReport
from websdk.db_context import DBContext
from tornado.web import RequestHandler


class RiElastiCacheHandler(BaseHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        pageNum = int(self.get_argument('page', default='1', strip=True))
        pageSize = int(self.get_argument('limit', default='10', strip=True))
        with DBContext('r') as session:
            if key:
                ri_elasticache_data = session.query(RiElastiCache).filter(
                    or_(RiElastiCache.ReservedCacheNodeId.like('%{}%'.format(key)),
                        RiElastiCache.ReservedCacheNodesOfferingId.like('%{}%'.format(key)),
                        RiElastiCache.CacheNodeType.like('%{}%'.format(key)),
                        RiElastiCache.Duration.like('%{}%'.format(key)),
                        RiElastiCache.FixedPrice.like('%{}%'.format(key)),
                        RiElastiCache.UsagePrice.like('%{}%'.format(key)),
                        RiElastiCache.CacheNodeCount.like('%{}%'.format(key)),
                        RiElastiCache.ProductDescription.like('%{}%'.format(key)),
                        RiElastiCache.OfferingType.like('%{}%'.format(key)),
                        RiElastiCache.State.like('%{}%'.format(key)),
                        RiElastiCache.RecurringCharges.like('%{}%'.format(key)),
                        )
                ).all()
            else:
                ri_elasticache_data = session.query(RiElastiCache).all()
            data_dict = list()
            for msg in ri_elasticache_data:
                msg = model_to_dict(msg)
                msg.pop("create_time")
                msg.pop("update_time")
                data_dict.append(msg)
            ri_elasticache_list_re = data_dict[(pageNum - 1) * pageSize:pageNum * pageSize]
        self.write(dict(code=0, msg='获取成功', count=len(data_dict), data=ri_elasticache_list_re))


class RiElastiCacheTodayHanlder(BaseHandler):
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
                .query(AWSElastiCacheRiUsageReport)\
                .filter(AWSElastiCacheRiUsageReport.date >= d_start)\
                .filter(AWSElastiCacheRiUsageReport.date <= d_end)
            if key is not None:
                data = data.filter(AWSElastiCacheRiUsageReport.dbengine.like("%" + key + "%"))
            data = data.all()

        usage_list = [model_to_dict(e) for e in data]
        for usage in usage_list:
            usage["total_running"] = int(decimal.Decimal(usage["total_running"]).quantize(decimal.Decimal('0.00000')))
            usage["total_ri"] = int(decimal.Decimal(usage["total_ri"]).quantize(decimal.Decimal('0.00000')))
            usage["coverage_rate"] = str(decimal.Decimal(usage["coverage_rate"]).quantize(decimal.Decimal('0.00000')))
            usage["date"] = str(usage["date"])
        total = len(usage_list)
        pageTotal = (total + pageSize if total % pageSize >= 0 else 0) // pageSize
        pageNum = min([pageNum, pageTotal])
        _pn = pageNum - 1
        ec2_data = usage_list[_pn * pageSize: pageNum * pageSize + 1]
        if export_csv == "1":
            filename = "ri_elasticache_report.csv"
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


class RiElastiCacheHistoryHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        end_day = datetime.now()
        start_day = end_day - timedelta(days=365)

        end_day = end_day.strftime("%Y-%m-%d")
        start_day = start_day.strftime("%Y-%m-%d")

        start_day = self.get_argument('key', default=start_day, strip=True)
        end_day = self.get_argument('key', default=end_day, strip=True)
        dbclass = self.get_argument('dbclass', default="t3", strip=True)
        dbsize = self.get_argument('dbsize', default="small", strip=True)
        dbengine = self.get_argument('dbengine', default="redis", strip=True)

        with DBContext('r', const.DEFAULT_DB_KEY) as session:
            data = session \
                .query(AWSElastiCacheRiUsageReport) \
                .filter(AWSElastiCacheRiUsageReport.date >= start_day) \
                .filter(AWSElastiCacheRiUsageReport.date < end_day) \
                .filter(AWSElastiCacheRiUsageReport.dbclass == dbclass) \
                .filter(AWSElastiCacheRiUsageReport.dbsize == dbsize) \
                .filter(AWSElastiCacheRiUsageReport.dbengine == dbengine) \
                .all()
        histories = [model_to_dict(e) for e in data]
        for history in histories:
            history["total_running"] = str(decimal.Decimal(history["total_running"]).quantize(decimal.Decimal('0.00000')))
            history["total_ri"] = str(decimal.Decimal(history["total_ri"]).quantize(decimal.Decimal('0.00000')))
            history["coverage_rate"] = str(decimal.Decimal(history["coverage_rate"]).quantize(decimal.Decimal('0.00000')))
            history["date"] =  str(history["date"])
        return self.write(dict(code=0, msg='获取成功', count=len(histories), data=histories))


elasticache_urls = [
    (r"/v1/cmdb/ri_elasticache/", RiElastiCacheHandler),
    (r"/v1/cmdb/ri_elasticache/today/", RiElastiCacheTodayHanlder),
    (r"/v1/cmdb/ri_elasticache/history/", RiElastiCacheHistoryHanlder),
]

if __name__ == "__main__":
    pass
