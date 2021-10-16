#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-03-13 11:08
# @Author : jianxlin
# @Site : 
# @File : host.py
# @Software: PyCharm

from datetime import datetime, timedelta
from pyzabbix import ZabbixAPI
from settings import settings


class UserZbx(object):
    def __init__(self,time=None):
        zbx_conf = settings.get("zabbix")
        _z = ZabbixAPI(zbx_conf.get("host"))
        _z.session.auth = (zbx_conf.get("user"), zbx_conf.get("pwd"))
        # _z.session.verify = False
        _z.timeout = 5
        _z.login(zbx_conf.get("user"), zbx_conf.get("pwd"))

        self.zbxapi = _z
        self.time = time

    def get_ec2_usage_info(self):
        hosts = {}
        user_macros = self.zbxapi.usermacro.get(hostids=[_["hostid"] for _ in self.zbxapi.host.get()])
        for um in user_macros:
            if um.get("macro", None) == "{$AWS_UNIQ_ID}" and um.get("value", "").startswith("i-"):
                ec2_id = um["value"]
                if ec2_id not in hosts.keys():
                    hosts[um["hostid"]] = {"ec2_id": um["value"]}
        zbx_hosts = self.zbxapi.host.get(hostids=list(hosts.keys()))
        for zh in zbx_hosts:
            hosts[zh["hostid"]]["Name"] = zh["host"]
            hosts[zh["hostid"]].update(self.get_usage(zh["hostid"]))
        return hosts

    def get_usage(self, hostid=None):
        return {
            "cpu": self.get_cpu_usage(hostid=hostid),
            "mem": self.get_mem_usage(hostid=hostid),
            "disk": self.get_disk_usage(hostid=hostid),
        }

    def get_cpu_usage(self, hostid=None):
        key_ = "system.cpu.util"
        return self.get_item_last_day_usage(self.get_host_item_id(hostid=hostid, key=key_))

    def get_mem_usage(self, hostid=None):
        key_ = "vm.memory.size[pavailable]"

        return self.get_item_last_day_usage(self.get_host_item_id(hostid=hostid, key=key_))

    def get_disk_usage(self, hostid=None):
        key_ = "vfs.fs.size[/,pused]"
        return self.get_item_last_day_usage(self.get_host_item_id(hostid=hostid, key=key_))

    def get_item_last_day_usage(self, itemid=None):
        if itemid is None:
            return None
        if self.time:
            time_from = self.time.replace(hour=0, minute=0, second=0)
        else:
            time_from = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0)
        time_till = time_from + timedelta(days=1)
        time_from = int(time_from.timestamp())
        time_till = int(time_till.timestamp())
        histories = self.zbxapi.history.get(itemids=[itemid],
                                            time_from=time_from,
                                            time_till=time_till,
                                            history=0)
        values = [float(h["value"]) for h in histories]

        return None if len(values) == 0 else sum(values) / len(values)

    def get_host_item_id(self, hostid=None, key=None):
        item = self.zbxapi.item.get(hostids=hostid, search={"key_": key})
        for _ in item:
            if _["key_"] == key:
                return _["itemid"]
        return None



if __name__ == '__main__':
    uz = UserZbx()
    # logging.info(uz.get_host_item_id(hostid='10566', key=''))
    # logging.info(uz.get_host_item_id(hostid='10566', key='vm.memory.size[pavailable]'))
    # logging.info(uz.get_item_last_day_usage(itemids='42343'))
