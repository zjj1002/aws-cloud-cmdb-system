# -*- coding: utf-8 -*-
# @Time    : 2020/7/20
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
import json
import os
import re
import shortuuid
from time import sleep
from datetime import datetime
from libs.web_logs import ins_log
from libs.db_context import DBContext
from models.clair_db import model_to_dict, LocalImage, ScanResult


# 获取本地docker  images 并存入数据库
def get_local_image():
    image_data = {}
    try:
        command = "nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker images'"
        # command = "docker images"
        result = os.popen(command)
        str_result = result.read()
        image_list = str_result.split('\n')
        image_data = [re.split(r'\s{2,}', i) for i in image_list[1:-1]]

    except Exception as e:
        print("异常:{}".format(e))
    return image_data


# 把本地image存入数据库
def images_sync_cmdb():
    image_data = get_local_image()
    image_data = [image for image in image_data if image[0] != "<none>" and image[1] != "<none>"]
    with DBContext('w') as session:
        try:
            session.query(LocalImage).delete()
            session.commit()
        except:
            session.rollback()
        # 写入新数据
        for image in image_data:
            ins_log.read_log('info', 'local_images信息：{}'.format(image))
            new_db = LocalImage(id=shortuuid.uuid(),
                                REPOSITORY=image[0],
                                TAG=image[1],
                                IMAGE_ID=image[2],
                                CREATED=image[3],
                                SIZE=image[4],
                                is_scan=False,
                                last_scan_time="未扫描")
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'local_images写入数据库共{}条'.format(len(image_data)))


# 扫描images 并把vul存入数据库
def scan_images(image):
    _poc_path = "/tmp"
    report_name = "report.json"
    # image ="309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-compliance"

    result = os.popen("nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker ps -a'").read()
    if "objectiflibre/clair-scanner" in result:
        os.system("nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker container rm scanner'")

    cmd = "nsenter --mount=/host/proc/1/ns/mnt sh -c \"docker run --net=scanning --name=scanner --link=clair:clair " \
          "-v '/var/run/docker.sock:/var/run/docker.sock'  objectiflibre/clair-scanner --clair='http://clair:6060' " \
          "--ip='scanner' -r {} {}\"".format(report_name, image)
    # 扫描
    result = os.popen(cmd).read()
    if result.count("Unapproved") == 0:
        ins_log.read_log('info', '没有漏洞')


    # 把report从文件中拷贝到宿主机
    result = os.system(
        "nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker container cp scanner:{}  /root/{}'".format(report_name,
                                                                                                      report_name))
    if result != 0:
        ins_log.read_log('info', '拷贝文件失败')
        return False

    # 把report从文件从宿主机拷贝到 合规性模块
    result = os.popen("nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker ps'").read()
    a = re.search("\s+(\w+)\s+309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-compliance", result)
    if a:
        CONTAINER_ID = a.group(1)
        result = os.system(
            "nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker container cp /root/{} {}:/tmp/{}'".format(report_name,
                                                                                                         CONTAINER_ID,
                                                                                                         report_name))
        if result != 0:
            ins_log.read_log('info', '拷贝report到容器失败')
            return False
    else:
        ins_log.read_log('info', '没有匹配到合规性的容器id')
        return False

    # 删除容器
    result = os.system("nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker container rm scanner'")
    if result != 0:
        ins_log.read_log('info', '删除scnner失败')
        return False

    ins_log.read_log('info', '执行完成')

    with DBContext('w') as session:
        with open(_poc_path + "/" + report_name, "r", encoding="UTF-8") as clair_read:
            report_str = clair_read.read()
            data = json.loads(report_str)  # str转为dict
            for vul in data["vulnerabilities"]:
                new_db = ScanResult(id='vul' + shortuuid.uuid(),
                                    image=image,
                                    featurename=vul.get("featurename"),
                                    featureversion=vul.get("featureversion"),
                                    vulnerability=vul.get("vulnerability"),
                                    namespace=vul.get("namespace"),
                                    description=vul.get("description"),
                                    link=vul.get("link"),
                                    severity=vul.get("severity"),
                                    fixedby=vul.get("fixedby"),
                                    scan_time=str(datetime.now()))
                session.add(new_db)
        session.commit()
        ins_log.read_log('info', 'vul写入成功')
        return True


# 每日定时任务
def scan_images_by_day():
    # 更新image
    images_sync_cmdb()
    with DBContext('w') as session:
        try:
            session.query(ScanResult).delete()
            session.commit()
        except:
            session.rollback()
        data = session.query(LocalImage).all()
        image_data = [model_to_dict(e) for e in data]
        for image in image_data:
            # image = image["REPOSITORY"] + ":" + image["TAG"] if image["TAG"] else image["REPOSITORY"]
            try:
                result = scan_images(image["REPOSITORY"] + ":" + image["TAG"])
                if not result:
                    ins_log.read_log('info', '扫描镜像{}失败'.format(image["REPOSITORY"] + ":" + image["TAG"]))
            except Exception as e:
                ins_log.read_log("info", "{}扫描失败 失败原因{}".format(image, e))

            session.query(LocalImage) \
                .filter(LocalImage.REPOSITORY == image["REPOSITORY"] , LocalImage.TAG == image["TAG"]) \
                .update(
                {
                    LocalImage.is_scan: result,
                    LocalImage.last_scan_time: str(datetime.now())
                })
            session.commit()
        ins_log.read_log('info', '扫描镜像共{}条'.format(len(image_data)))


if __name__ == '__main__':
    images_sync_cmdb()
