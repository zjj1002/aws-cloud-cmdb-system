#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-08 16:43
# @Author : jianxlin
# @Site : 
# @File : ec2.py
# @Software: PyCharm
import datetime
from libs.aws.aws import AWS
from settings import settings
from libs.aws.session import get_aws_session


class EC2(AWS):
    ServiceName = "ec2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_ec2_list(self):
        """
            获取主机列表。
        :return:
        """
        ret = []
        result = self.client.describe_instances()
        for r in result["Reservations"]:
            for i in r["Instances"]:
                name = None
                if i["State"]["Name"] != "running":
                    continue
                if "Tags" in i.keys():
                    for t in i["Tags"]:
                        if t["Key"] == "Name":
                            name = t["Value"]
                            break
                e = {
                    "InstanceId": i["InstanceId"],
                    "Name": name,
                    "InstanceType": i["InstanceType"]
                }
                ret.append(e)
        return ret

    def get_volumes(self):
        """
            获取ebs列表。
        :return:
        """
        ret = {}
        volumes = self.client.describe_volumes()

        for v in volumes["Volumes"]:
            vol_id = v["VolumeId"]
            ret[vol_id] = {}
            ret[vol_id]["InstanceId"] = "i-ffffffffffffffffff"
            for a in v["Attachments"]:
                ret[vol_id]["InstanceId"] = a["InstanceId"]
            ret[vol_id]["Size"] = v["Size"]
            ret[vol_id]["CreateTime"] = v["CreateTime"]
            ret[vol_id]["State"] = v["State"]
            name = None
            if "Tags" in v.keys():
                for t in v["Tags"]:
                    if t["Key"] == "Name":
                        name = t["Value"]
                    break

            ret[vol_id]["Name"] = name
        return ret

    def get_ec2_volume_size(self):
        """
            获取主机ebs信息。
        :return:
        """
        ret = {}
        volumes = self.client.describe_volumes()

        for v in volumes["Volumes"]:
            instance_id = None
            device = None
            for a in v["Attachments"]:
                instance_id = a["InstanceId"]
                device = a["Device"].split("/")[-1]
            if instance_id not in ret.keys():
                ret[instance_id] = {}
            ret[instance_id][device] = v["Size"]
        return ret

    def get_snapshots(self):
        """
            获取快照信息。
        :return:
        """
        ret = {}
        snapshots = self.client.describe_snapshots()
        volumes = self.get_volumes()
        for s in snapshots["Snapshots"]:
            snap_id = s["SnapshotId"]
            vol_id = s["VolumeId"]

            ret[snap_id] = volumes.get(vol_id, {"InstanceId": "i-fffffffffffffffffe"})["InstanceId"]
        return ret

    def get_ami_snapshots(self, owner_id=None):
        """
            获取snapshots
        :return:
        """
        ret = {}
        snapshots = self.client.describe_snapshots(OwnerIds=[owner_id, ])
        for s in snapshots["Snapshots"]:
            if not s["Description"].startswith("Created by CreateImage"):
                continue
            snapshot_id = s["SnapshotId"]
            name = None
            start_time = s["StartTime"]
            if "Tags" in s.keys():
                for t in s["Tags"]:
                    if t["Key"] == "Name":
                        name = t["Value"]
            ret[snapshot_id] = {
                "Name": name,
                "StartTime": start_time
            }
        return ret

    def get_volumes_list(self):
        return [(k, v["InstanceId"]) for k, v in self.get_volumes().items()]

    def get_snapshots_list(self):
        return [(k, v) for k, v in self.get_snapshots().items()]

    def get_ami(self, owner_id=None):
        """
            查询AMI列表
        :return:
        """
        ret = {}
        result = self.client.describe_images(Owners=[owner_id])
        for a in result["Images"]:
            image_id = a["ImageId"]
            create_date = a["CreationDate"]
            instance_id = None
            snapshots = []
            for ebs in a["BlockDeviceMappings"]:
                snapshots.append(ebs["Ebs"]["SnapshotId"])
            if "Tags" in a.keys():
                for t in a["Tags"]:
                    if t["Key"] == "InstanceId":
                        instance_id = t["Value"]

            ret[image_id] = {
                "Snapshots": snapshots,
                "AmiId": image_id,
                "InstanceId": instance_id,
                "CreateDate": create_date
            }
        return ret

    def describe_ri(self):
        """

        :return:
        """

        ret = []
        result = self.client.describe_reserved_instances()
        for ri in result["ReservedInstances"]:
            if ri["End"].replace(tzinfo=None) >= datetime.datetime.now().replace(tzinfo=None):
                ret.append(ri)
        return ret

    def get_instance_type_dict(self):
        """

        :return:
        """

        ret = {}
        instance_list =list()
        for file in self.get_all_instance_type(self.client):
            instance_list.append(file)
        for i in instance_list:
            dict = {}
            dict.update({"cpu_num": i["VCpuInfo"]["DefaultVCpus"]})
            dict.update({"mem": i["MemoryInfo"]["SizeInMiB"]})
            ret.update({i["InstanceType"]: dict})
        return ret

    def get_all_instance_type(self,client_ec2, **base_kwargs):
        continuation_token = None
        while True:
            list_kwargs = dict(MaxResults=100, **base_kwargs)
            if continuation_token:
                list_kwargs['NextToken'] = continuation_token
            response = client_ec2.describe_instance_types(**list_kwargs)
            yield from response.get('InstanceTypes', [])
            if not response.get('NextToken'):  # At the end of the list?
                break
            continuation_token = response.get('NextToken')


def p():
    ec2 = EC2()

    ee = ec2.get_ec2_list()

    for ri in ec2.describe_ri():
        Y = False
        p = ri["FixedPrice"] / ri["InstanceCount"]
        end = str(ri["End"] - datetime.timedelta(days=365)).split(" ")[0].replace("-", "/").strip()
        for i in range(0, ri["InstanceCount"]):
            for _ in ee:
                if _["InstanceType"] != ri["InstanceType"]:
                    continue
                print(ri["ReservedInstancesId"], "\t", "ec2", "\t", p, "\t", ri["InstanceType"], "\t",
                      _["Name"], "\t",
                      _["InstanceId"], "\t", end)
                ee.remove(_)
                Y = True
                break
        if not Y:
            print(ri["ReservedInstancesId"], "\t", "ec2", "\t", p, "\t", ri["InstanceType"], "\t", end)
    for e in ee:
        print(None, "\t", "ec2", "\t", None, "\t", e["InstanceType"], "\t", None, "\t", e["InstanceId"], "\t", None)


def get_instance_type_dict():
    """
         获取主机类型的cpu和mem信息。
     :return:
     """
    ret = {}
    s = get_aws_session(**settings.get("aws_key"))
    client = s.client('ec2')
    result = client.describe_instance_types()
    for i in result["InstanceTypes"]:
        dict = {}
        dict.update({"cpu_num": i["VCpuInfo"]["DefaultVCpus"]})
        dict.update({"mem": i["MemoryInfo"]["SizeInMiB"]})
        ret.update({i["InstanceType"]: dict})
    return ret

if __name__ == '__main__':
    p()
