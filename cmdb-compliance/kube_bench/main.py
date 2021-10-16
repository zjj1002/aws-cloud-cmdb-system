# -*- coding: utf-8 -*-
# @Time    : 2020/9/9
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
import subprocess
import re
import os
import sys
from datetime import datetime
from libs.web_logs import ins_log
from models.kube_bench import KUBECONFIG, model_to_dict, BENCHDB
from libs.db_context import DBContext
import shortuuid


def config_parser(config_str):
    server = re.compile(r'https://(\S*)\s*')
    current_context = re.compile(r'current-context:\s*(\w*)\s*')
    config_info = {
        "server": 'unknown',
        "current_context": 'unknown',
    }
    try:
        config_info['server'] = server.findall(config_str)[0]
        config_info['current_context'] = current_context.findall(config_str)[0]
    except Exception as e:
        ins_log.read_log('info', "kube config parser failed: %s" % e)
    return config_info


def databases_config_init():
    try:
        with DBContext('w') as session:
            try:
                session.query(KUBECONFIG).delete()
                session.commit()
            except:
                session.rollback()

            #把report从文件从宿主机拷贝到 合规性模块
            result = os.popen("nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker ps'").read()
            a = re.search("\s+(\w+)\s+309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-compliance", result)
            if a:
                CONTAINER_ID = a.group(1)
                result = os.system(
                    "nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker container cp /root/.kube {}:/tmp/'".format(CONTAINER_ID))
                if result != 0:
                    ins_log.read_log('info', '拷贝config到容器失败')
                    return False
            else:
                ins_log.read_log('info', '没有匹配到合规性的容器id')
                return False

            _kube_path = "/tmp/.kube"
            if os.path.exists(_kube_path):
                for config_filename in os.listdir(_kube_path):
                    if "config" in config_filename:
                        with open(_kube_path + "/" + config_filename, "r", encoding="UTF-8") as config_read:
                            config_str = config_read.read()
                            config_data = config_parser(config_str)
                            new_db = KUBECONFIG(
                                id='config_' + shortuuid.uuid(),
                                kube_config_name=config_filename,
                                current_context=config_data['current_context'],
                                server=config_data['server'],
                                date=str(datetime.now()))
                        session.add(new_db)
                        session.commit()
    except Exception as e:
        ins_log.read_log('info', "config parser failed: %s" % e)
        sys.exit(0)


def scan_kube():
    # 从数据库拿出所有的kubeconfig
    with DBContext('w') as session:
        config_data = session.query(KUBECONFIG).all()
        config_list = []
        for data in config_data:
            config_data = model_to_dict(data)
            config_list.append(config_data["kube_config_name"])
        # 扫描
        data_list = []
        for config in config_list:
            #扫描master
            result = subprocess.getstatusoutput("nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro -t  -v $(which kubectl):/usr/local/mount-from-host/bin/kubectl -v ~/.kube:/.kube -e KUBECONFIG=/.kube/{} aquasec/kube-bench:latest master'".format(config))

            # 存储master扫描结果
            if "Remediations" not in result[1]:
                ins_log.read_log('info', '{}的master扫描失败'.format(config))
                return False
            else:
                re = result[1].split("\n\n", 1)
                line_list = result[1].splitlines()
                line_b = re[1].split("\n\n")
                for line in line_list:
                    if "[WARN]" in line or "[FAIL]" in line:
                        date_dict = {}
                        re = line.split(" ", 2)
                        date_dict["config_name"] = config
                        date_dict["mastr_or_node"] = "master"
                        date_dict["stats"] = re[0]
                        date_dict["version"] = re[1]
                        date_dict["description"] = re[2]
                        for i in line_b:
                            if re[1] in i:
                                date_dict["remediations"] = i
                                break
                        data_list.append(date_dict)

            #扫描node
            result = subprocess.getstatusoutput(
                "nsenter --mount=/host/proc/1/ns/mnt sh -c 'docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro -t  -v $(which kubectl):/usr/local/mount-from-host/bin/kubectl -v ~/.kube:/.kube -e KUBECONFIG=/.kube/{} aquasec/kube-bench:latest node'".format(
                    config))

             # 存储node扫描结果
            if "Remediations" not in result[1]:
                ins_log.read_log('info', '{}的node扫描失败'.format(config))
                return False
            else:
                re = result[1].split("\n\n", 1)
                line_list = result[1].splitlines()
                line_b = re[1].split("\n\n")
                for line in line_list:
                    if "[WARN]" in line or "[FAIL]" in line:
                        date_dict = {}
                        re = line.split(" ", 2)
                        date_dict["config_name"] = config
                        date_dict["mastr_or_node"] = "node"
                        date_dict["stats"] = re[0]
                        date_dict["version"] = re[1]
                        date_dict["description"] = re[2]
                        for i in line_b:
                            if re[1] in i:
                                date_dict["remediations"] = i
                                break
                        data_list.append(date_dict)
    return data_list


def sys_db():
    data_list = scan_kube()
    if not data_list:
        ins_log.read_log('info', 'k8s扫描失败')
        return
    with DBContext('w') as session:
        try:
            session.query(BENCHDB).delete()
            session.commit()
        except:
            session.rollback()
        for kube_result in data_list:
            new_db = BENCHDB(
                id="result_" + shortuuid.uuid(),
                config_name=kube_result["config_name"],
                mastr_or_node=kube_result["mastr_or_node"],
                stats=kube_result.get("stats", "无"),
                version=kube_result["version"],
                description=kube_result["description"],
                remediation=kube_result["remediations"],
                date=str(datetime.now()))
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', '存入k8s扫描结果共{}条'.format(len(data_list)))

def kube_daily_scan():
    databases_config_init()
    sys_db()


if __name__ == '__main__':
    sys_db()
