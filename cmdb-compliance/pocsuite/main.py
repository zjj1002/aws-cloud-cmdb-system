# -*- coding: utf-8 -*-
# @Time    : 2020/7/14
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

import time
import shortuuid
from datetime import datetime
from tempfile import gettempdir
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.pocsutie_db import PocsuiteTask, PocsuitePlugin, model_to_dict, Result, Target
from pocsuite.pocsuite_api import pocsuite_scanner
from pocsuite.tools.parser import databases_init


def add_task():
    """
    把所有目标和poc加入task中
    :return:
    """
    with DBContext('w') as session:
        plugin_data = session.query(PocsuitePlugin).all()
        plugin_list = [model_to_dict(e) for e in plugin_data]
        plugin_list = [e["id"] for e in plugin_list]
        target_data = session.query(Target).all()
        target_list = [model_to_dict(e) for e in target_data]
        target_list = [e["id"] for e in target_list]
        id = "task_" + shortuuid.uuid()
        new_db = PocsuiteTask(id=id,
                              target=','.join(target_list),
                              poc=','.join(plugin_list),
                              status="未扫描",
                              name="daily_task_"+ str(datetime.now())[:10],
                              date=str(datetime.now()),
                              vul_count="0"
                              )
        session.add(new_db)
        session.commit()
        return id


def poc_config_init(target_list, poc_str, threat=10, quiet=True):
    _poc_config = {
        'url_file': '',
        'poc': '',
        'threads': threat,
        'quiet': quiet
    }
    tmp_path = gettempdir()
    try:
        target_file_path = tmp_path + "/target_{}".format(int(time.time()))
        print(target_file_path)
        with open(target_file_path, 'w') as _target_f_save:
            _target_f_save.write("\n".join(target_list))
        _poc_config['url_file'] = target_file_path
    except Exception as e:
        ins_log.read_log('info', "Failed to save temporary target file: {} {}".format(target_list[0], e))
    try:
        poc_file_path = tmp_path + "/poc_{}.py".format(int(time.time()))
        with open(poc_file_path, 'w') as _poc_f_save:
            _poc_f_save.write(poc_str.encode('ascii', 'ignore').decode('ascii'))
        _poc_config['poc'] = poc_file_path
    except Exception as e:
        ins_log.read_log('info', "Failed to save temporary poc file: {}".format(e))
    return _poc_config


def t_poc_scanner_all(task_id):
    """
    传入task_id  执行扫描任务
    """
    try:
        with DBContext('w') as session:
            #获取task任务
            task_data = session.query(PocsuiteTask).filter(PocsuiteTask.id == task_id).first()
            #判断taks任务是否存在
            if task_data:
                task_data = model_to_dict(task_data)
                target_id_list = task_data["target"].split(",")
                poc_id_list = task_data["poc"].split(",")
                target_list = []
                #获取任务中的目标列表
                for id in target_id_list:
                    data = session.query(Target).filter(Target.id == id).first()
                    data = model_to_dict(data)
                    target_list.append(data["url"])
                #获取任务中的的poc列表
                plugin_list = []
                for id in poc_id_list:
                    data = session.query(PocsuitePlugin).filter(PocsuitePlugin.id == id).all()
                    data = [model_to_dict(e) for e in data]
                    plugin_list.append({data[0]["id"]: data[0]["poc_str"]})
                count = 0
                #如果获取的目标和poc都不为空就开始扫描任务
                if target_list and plugin_list:
                    #遍历poc列表
                    for plugin in plugin_list:
                        for key, value in plugin.items():# 提取poc的代码
                            #初始化config文件
                            _poc_config = poc_config_init(target_list, value, 1)
                            #执行扫描
                            _scan_items = pocsuite_scanner(_poc_config)
                            #储存扫描结果
                            for _item in _scan_items:
                                try:
                                    result = _item['result'] if _item['result'] else _item['error_msg'][1]
                                    new_db = Result(
                                        id="result_" + shortuuid.uuid(),
                                        tid=task_data["id"],
                                        poc=key,
                                        task_name=task_data.get("name", "无"),
                                        poc_name=_item["poc_name"],
                                        status=_item["status"],
                                        target=_item["target"],
                                        mode=_item["mode"],
                                        app_name=_item["app_name"],
                                        app_version=_item["app_version"],
                                        url=_item["url"],
                                        name=_item["name"],
                                        created=_item["created"],
                                        vul_id=_item["vul_id"],
                                        result=str(result))
                                    session.add(new_db)
                                    try:
                                        session.commit()
                                    except Exception as e:
                                        session.rollback()
                                        ins_log.read_log('info', "存储失败 {}".format(e))
                                    if _item['status'] == "success":
                                        count += 1
                                except Exception as e:
                                    ins_log.read_log('info', "save poc result failed: {}".format(e))
                #改变任务的状态
                session.query(PocsuiteTask) \
                    .filter(PocsuiteTask.id == task_id) \
                    .update(
                    {
                        PocsuiteTask.end_date: str(datetime.now()),
                        PocsuiteTask.status: "已扫描"
                    })
                session.commit()

            else:
                ins_log.read_log('info', "dont find task {}".format(task_id))

    except Exception as e:
        ins_log.read_log('info', "Failed to save temporary poc file: {}".format(e))


def dayly_san_taks():
    #初始话poc数据库
    databases_init()
    # 创建每日任务 并返回 任务id
    task_id = add_task()
    # 执行任务
    t_poc_scanner_all(task_id)

def run_scan_task():
    with DBContext('w') as session:
        # 获取task任务的id列表
        task_list = []
        task_data = session.query(PocsuiteTask).filter(PocsuiteTask.status =="未扫描").all()
        for data in task_data:
            data_dict = model_to_dict(data)
            task_list.append(data_dict.get("id"))
        #执行扫描任务
        for task_id in task_list:
            try:
                t_poc_scanner_all(task_id)
            except Exception as e:
                ins_log.read_log('info', "run task_id{} failed {}".format(task_id,e))
    ins_log.read_log('info', "已执行网站扫描任务")

if __name__ == '__main__':
    run_scan_task()
