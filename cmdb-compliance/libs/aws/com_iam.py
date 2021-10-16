# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : com_iam.py
# @Role    : 筛选出不合规的iam


import datetime

from libs.aws.session import get_aws_session
from libs.web_logs import ins_log
from settings import settings


class ComplianceIamApi():
    def __init__(self, session):
        self.iam_list = []
        self.usrname_list = []
        # 获取ec2的client
        self.iam_client = session.client("iam")

    def get_iam_access_key_response(self, usrname):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.iam_client.list_access_keys(UserName=usrname)
        except Exception as e:
            err = e
        return response_data, err

    def get_user_name_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.iam_client.list_users()
        except Exception as e:
            err = e
        return response_data, err

    def get_aksk_90_used_status(self, response):
        status = []
        if response["AccessKeyMetadata"]:
            for user_info in response["AccessKeyMetadata"]:
                ak_id = user_info["AccessKeyId"]
                ak_data = self.iam_client.get_access_key_last_used(AccessKeyId=ak_id)
                ak_used_last = ak_data["AccessKeyLastUsed"]
                if len(ak_used_last) == 3:
                    last_used_time = ak_used_last["LastUsedDate"]
                    if datetime.datetime.utcnow().timestamp() - last_used_time.timestamp() > 60 * 60 * 24 * 90:
                        status.append(False)
                    else:
                        status.append(True)
        return status

    def get_90_no_signin_and_two_keys_users_list(self):
        """
        获取返回值
        :return:
        """

        response_data, err = self.get_user_name_response()
        if err:
            ins_log.read_log("error", "获取用户名失败{}".format(err))

        for each in response_data["Users"]:
            username_dict = {}
            username_dict["password_last_used"] = each.get("PasswordLastUsed",0)
            if not username_dict["password_last_used"] or datetime.datetime.utcnow().timestamp()- username_dict["password_last_used"].timestamp() > 60*60*24*90:
                username_dict["is_90_signin"] = False
                username_dict["user_name"] = each.get("UserName")
                username_dict["user_id"] = each.get("UserId")
                username_dict["arn"] = each.get("Arn")
                response, err = self.get_iam_access_key_response(usrname=each.get("UserName"))
                # 添加ak/sk 90天未使用的记录
                status = self.get_aksk_90_used_status(response)
                # all全为真返回true, 有一个假返回false
                if status and all(status):
                    username_dict["aksk_90_used"] = True
                else:
                    username_dict["aksk_90_used"] = False

                if err:
                    ins_log.read_log("error", "获取用户密码列表失败{}".format(err))
                if len(response["AccessKeyMetadata"]) == 2:
                    username_dict["is_2_keys"] = False
                else:
                    username_dict["is_2_keys"] = True
                self.iam_list.append(username_dict)

            else:
                response, err = self.get_iam_access_key_response(usrname=each.get("UserName"))
                if err:
                    ins_log.read_log("error", "获取用户密码列表失败{}".format(err))
                if len(response["AccessKeyMetadata"]) == 2:
                    username_dict["is_2_keys"] = False
                    username_dict["is_90_signin"] = True
                    username_dict["user_name"] = each.get("UserName")
                    username_dict["user_id"] = each.get("UserId")
                    username_dict["arn"] = each.get("Arn")
                    # 添加ak/sk 90天未使用的记录
                    status = self.get_aksk_90_used_status(response)
                    # all全为真返回true, 有一个假返回false
                    if status and all(status):
                        username_dict["aksk_90_used"] = True
                    else:
                        username_dict["aksk_90_used"] = False

                    self.iam_list.append(username_dict)
                else:
                    username_dict["is_2_keys"] = True
                    # 添加ak/sk 90天未使用的记录
                    status = self.get_aksk_90_used_status(response)
                    # all全为真返回true, 有一个假返回false
                    if status and all(status):
                        username_dict["aksk_90_used"] = True
                    else:
                        username_dict["aksk_90_used"] = False

        return self.iam_list

    def main(self):
        result = self.get_90_no_signin_and_two_keys_users_list()
        return result

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.iam_client.list_users()

        return response_data
