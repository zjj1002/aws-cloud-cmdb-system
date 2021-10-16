#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-06 13:21
# @Author : jianxlin
# @Site : 
# @File : cloudwatch.py
# @Software: PyCharm
import json
from datetime import datetime
from datetime import timedelta

from libs.aws.aws import AWS


class CloudWatch(AWS):
    """
        Cloudwatch服务
    """
    ServiceName = 'cloudwatch'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __get_ec2_metric_statistics(self, Namespcace=None, MetricName=None, InstanceId=None, Dimensions=None, date=None,
                                    Period=None, **kwargs):
        """
            查询ec2主机cpu监控信息
        :return:
        """
        points = []
        start_time = date
        start_time = start_time.replace(day=1, hour=0, minute=0, second=0)
        next_month_num = (start_time.month + 1) % 12
        next_year_num = start_time.year + (start_time.month + 1) // 12

        end_time = start_time.replace(month=next_month_num, year=next_year_num)
        # end_time = start_time.replace(month=start_time.month + 1)
        dimensions = [
            {
                'Name': 'InstanceId',
                'Value': InstanceId
            }
        ]
        if Dimensions:
            dimensions = Dimensions
        for i in range(0, 8):
            start_time = start_time + timedelta(days=5)
            if start_time >= end_time:
                break
            _end_time = start_time + timedelta(days=5)
            if _end_time > end_time:
                _end_time = end_time
            ret = self.client.get_metric_statistics(
                Namespace=Namespcace,
                MetricName=MetricName,
                Dimensions=dimensions,
                EndTime=_end_time,
                StartTime=start_time,
                Period=Period,
                Statistics=[
                    'Maximum'
                ],
                Unit='Percent'
            )
            points += ret["Datapoints"]
        if not points:
            return -1
        return sum([d["Maximum"] for d in points]) / len(points)

    def __get_metrics(self, Namespace=None, MetricName=None, ):
        """
            查询指标。
        :param Namespace:
        :param MetricName:
        :return:
        """
        return self.client.list_metrics(Namespace=Namespace,
                                        MetricName=MetricName)

    def get_ec2_ebs_metrics(self):
        """
            查询磁盘使用率指标信息列表。
        :return:
        """
        ret = {}
        result = self.__get_metrics(Namespace="CWAgent", MetricName='disk_used_percent')
        for m in result["Metrics"]:
            ms = []
            _ = {}
            for d in m["Dimensions"]:
                ms.append(d)
                d = json.loads(json.dumps(d))
                _[d["Name"]] = d["Value"]
            if sorted(_.keys()) != sorted(["path", "InstanceId", "device", "fstype"]):
                continue
            if _["fstype"] != "xfs":
                continue
            instance_id = _["InstanceId"]
            if instance_id not in ret.keys():
                ret[instance_id] = {}
            ret[instance_id][_["device"]] = ms

        return ret

    def get_ec2_cpu_usage_avg(self, *args, **kwargs):
        """
            查询ec2监控信息。
        :return:
        """
        return self.__get_ec2_metric_statistics(Namespcace="AWS/EC2", MetricName="CPUUtilization", *args, **kwargs)

    def get_ec2_mem_usage_avg(self, *args, **kwargs):
        """
            查询ec2监控信息。
        :return:
        """
        return self.__get_ec2_metric_statistics(Namespcace="CWAgent", MetricName="mem_used_percent", *args,
                                                **kwargs)

    def get_ec2_disk_usage_avg(self, *args, **kwargs):
        """
            查询ec2监控信息。
        :return:
        """
        ret = {}
        instance_metrics = self.get_ec2_ebs_metrics()
        for instance_id, devices in instance_metrics.items():
            ret[instance_id] = {}
            for name, dimensions in devices.items():
                avg_max = self.__get_ec2_metric_statistics(Namespcace="CWAgent", MetricName="disk_used_percent",
                                                           Dimensions=dimensions, *args, **kwargs)
                ret[instance_id][name] = avg_max
        return ret


if __name__ == '__main__':
    cw = CloudWatch()
    #                                date=datetime.now(),
    #                                Period=60 * 5))
    #                                date=datetime.now(),
    #                                Period=60 * 5))

    #                                 date=datetime.now(),
    #                                 Period=60 * 5))

    ms = cw.get_ec2_disk_usage_avg(date=datetime.now(), Period=60 * 5)
