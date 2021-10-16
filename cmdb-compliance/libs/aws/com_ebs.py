# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
from datetime import datetime
from libs.web_logs import ins_log


class ComplianceEbsApi():
    def __init__(self,session):
        self.ebs_list = []
        # 获取ec2的client
        self.client = session.client('ec2')

    def get_ebs_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.client.get_paginator('describe_volumes')
        except Exception as e:
            err = e
        return response_data, err

    def get_ebs_list(self):
        """
        获取返回值
        :return:
        """
        paginator, err = self.get_ebs_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False

        page_iterator = paginator.paginate()
        filtered_iterator = page_iterator.search("Volumes[]")
        for i in filtered_iterator:
            print(i)
            i.update({"Snapshot_overtime": "True"})
            if i["SnapshotId"] != "":
                try:
                    response = self.client.describe_snapshots(SnapshotIds=[i["SnapshotId"]])
                    if datetime.now().timestamp() - response["Snapshots"][0][
                        "StartTime"].timestamp() > 60 * 60 * 24 * 30:
                        i.update({"Snapshot_overtime": "false"})
                except:
                    pass
            if i['Attachments'] == [] or i['Encrypted'] == False or i["Snapshot_overtime"] =="false":
                i['Attachments'] = '磁盘没有被使用' if i['Attachments'] == [] else "磁盘有人使用"
                i['CreateTime'] = i['CreateTime'].strftime("%Y-%m-%d")
                i['Encrypted'] = 'false' if i['Encrypted'] == False else 'Trues'
                self.ebs_list.append(i)
        return self.ebs_list

    def main(self):
        result = self.get_ebs_list()
        return result


    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.client.get_paginator('describe_volumes')

        return response_data




