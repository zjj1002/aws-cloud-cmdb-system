# -*- coding: utf-8 -*-
# @Time    : 2020/8/3
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
import json
import os
import shlex
import subprocess
import time
from datetime import datetime
from urllib.request import urlopen
import shortuuid
import gitlab
from libs.web_logs import ins_log
from libs.db_context import DBContext
from models.git_secrets import GitProject, model_to_dict, GitScanResult
from settings import settings

git_url = settings.get("git").get("git_url")
git_token = settings.get("git").get("git_token")
path = settings.get("git").get("path")


class Gitlab:
    def __init__(self):
        self.url = git_url
        self.token = git_token

    #登录认证
    def login_gitlab(self):
        gl = gitlab.Gitlab(git_url, git_token, api_version='4')
        gl.auth()
        return gl

    #获取项目列表
    def get_project_list_by_jdk(self):
        gl = self.login_gitlab()
        projects = gl.projects.list()
        return projects

    # 获取项目列表
    def get_project_list_by_api(self):
        allProjects = urlopen("{}api/v4/projects?membership=true&private_token={}".format(git_url,git_token))
        allProjectsDict = json.loads(allProjects.read().decode())
        return allProjectsDict

    #克隆项目到本地
    def clone_projects_by_jdk(self):
        projects_list = self.get_project_list_by_jdk()
        for thisProject in projects_list:
            try:
                thisProjectURL = thisProject.attributes["http_url_to_repo"]
                name_with_namespace = thisProject.attributes["path_with_namespace"]
                command = shlex.split('git clone %s %s' % (thisProjectURL, '/root/gitClone/' + name_with_namespace))
                resultCode = subprocess.Popen(command)
            except Exception as e:
                print("Error on %s: %s" % (thisProjectURL, e.strerror))
            time.sleep(5)

    #克隆项目到本地
    def clone_projects_by_api(self):
        projects_list = self.get_project_list_by_api()
        with DBContext('w') as session:
            try:
                session.query(GitProject).delete()
                session.commit()
            except:
                session.rollback()

        if os.path.exists(path):
            os.system("rm -rf " + path)
        else:
            print('no such file:%s' % path)

        for thisProject in projects_list:
            try:
                thisProjectURL = thisProject['http_url_to_repo']
                name_with_namespace = thisProject['path_with_namespace']
                command = shlex.split('git clone http://oauth2:%s@%s %s' % (git_token,thisProjectURL.replace("http://",""), path + name_with_namespace))
                resultCode = subprocess.Popen(command)
            except Exception as e:
                print("Error on %s: %s" % (thisProjectURL, e.strerror))

            time.sleep(3)

            new_db = GitProject(id=shortuuid.uuid(),
                                name=thisProject['name'],
                                branch=thisProject['default_branch'],
                                project_team=thisProject['name_with_namespace'].replace(" ","").split("/")[0],
                                path = thisProject['name_with_namespace'].replace(" ",""),
                                source=thisProject['web_url'],
                                add_date=str(datetime.now()),
                                last_scan_time="未扫描")
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', '项目克隆到本地')


def scan_project():
    with DBContext('w') as session:
        try:
            session.query(GitScanResult).delete()
            session.commit()
        except:
            session.rollback()
        data = session.query(GitProject).all()
        projects_data = [model_to_dict(e) for e in data]
        for project in projects_data:
            cmd = "git secrets --scan -r "+ path +  project["path"]
            result = subprocess.getstatusoutput(cmd)
            if "Matched one or more prohibited patterns" not in result[1]:
                result = "safe"
                risk_index = "low"
            else:
                result = result[1].splitlines()[0:-10]
                result = "----".join(result) if result else None
                risk_index = "high" if result else "low"
            new_db = GitScanResult(id=shortuuid.uuid(),
                                name=project['name'],
                                result=result,
                                risk_index=risk_index,
                                branch=project['branch'],
                                project_team=project["project_team"],
                                Last_scan_time=str(datetime.now()),
                                source=project["source"],)
            session.add(new_db)
        session.commit()
        ins_log.read_log('info', '把扫描结果添加到数据库')


def daily_scan_task():
    st_init = Gitlab()
    st_init.clone_projects_by_api()
    scan_project()


if __name__ == '__main__':
    st_init = Gitlab()
    st_init.clone_projects_by_api()
    scan_project()





