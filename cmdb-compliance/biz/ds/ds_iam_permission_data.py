import json

from biz.ds.get_action import run
import argparse
import datetime
import yaml
from libs.aws.session import get_aws_session
from libs.db_context import DBContext
from models.permission_optimize import PermissionOptimize
from settings import settings


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def run_user(account, start, end):

    session = get_aws_session(**settings.get("aws_key"))
    client = session.client("iam")
    account_iam = client.get_account_authorization_details(
        Filter=['User', "LocalManagedPolicy", "AWSManagedPolicy"]
    )
    with open("account-data/demo_iam.json", mode='w', encoding='utf-8') as f:
        json.dump(account_iam, f, cls=ComplexEncoder)

    try:
        with open('/var/www/cmdb-compliance/config.yaml', 'r') as f:
            config = yaml.load(f.read())
    except yaml.YAMLError as e:
        raise argparse.ArgumentError(
            None,
            "ERROR: Could not load yaml from config file {}\n{}".format('config.yaml', e)
        )
    with DBContext('w') as session:
        session.query(PermissionOptimize).delete(synchronize_session=False)  # 清空数据库的所有记录
        for user_iam in account_iam["UserDetailList"]:
            user_name = user_iam["UserName"]
            user_id = user_iam["UserId"]
            user_arn = user_iam["Arn"]
            print(user_name)
            user_action_list = run(account, user_name, config, start, end)
            print(user_action_list)
            for action in user_action_list:
                services_action = action.split(":")
                services_name = services_action[0]
                un_used_action = services_action[1]
                if not (un_used_action.startswith("describe") or un_used_action.startswith("list")):
                    new_data = PermissionOptimize(user_name=user_name, user_id=user_id, user_arn=user_arn,
                                        services_name=services_name, un_used_permission=un_used_action)
                    session.add(new_data)
                    session.commit()


def iam_permission_sync_cmdb():
    """定时任务：定时获取数据存入数据库"""
    now = datetime.datetime.now()
    s = (now - datetime.timedelta(days=90)).date().isoformat()  # 检测90内的数据情况
    e = now.date().isoformat()
    root_account = 'zjj'
    run_user(root_account, s, e)


if __name__ == '__main__':
    iam_permission_sync_cmdb()



