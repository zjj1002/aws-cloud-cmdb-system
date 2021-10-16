# -*- coding: utf-8 -*-
# @Time    : 2020/6/11
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :
from datetime import datetime
from libs.web_logs import ins_log
import boto3
import shortuuid
from libs.web_logs import ins_log
from libs.db_context import DBContext
from models.aws_sts import AwsSts, model_to_dict


class AWSSTS():
    def __init__(self, action, resource, rolearn, rolesessionname, externalid, durationseconds, region_name,
                 aws_access_key_id, aws_secret_access_key):
        self.action = action
        self.resource = resource
        self.rolearn = rolearn
        self.rolesessionname = rolesessionname
        self.externalid = externalid
        self.durationseconds = durationseconds
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def get_sts_client(self):
        client = None
        err = None
        try:
            client = boto3.client('sts', region_name=self.region_name, aws_access_key_id=self.aws_access_key_id,
                                  aws_secret_access_key=self.aws_secret_access_key)
        except Exception as e:
            err = e
        return client, err

    def assume_role(self):
        client, err = self.get_sts_client()
        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False
        response = client.assume_role(
            DurationSeconds=self.durationseconds,
            ExternalId=self.externalid,
            Policy=f'''{{"Version": "2012-10-17","Statement": [{{"Effect": "Allow","Action": {self.action},"Resource": "{self.resource}/*"}}]}}''',
            RoleArn=self.rolearn,
            RoleSessionName=self.rolesessionname,
        )
        return response

    def async_db(self):
        re = self.assume_role()
        credentials = re['Credentials']
        region_name = "cn-north-1",
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken']
        with DBContext('w') as session:
            new_db = AwsSts(id=shortuuid.uuid(),
                            AccessKeyId=aws_access_key_id,
                            SecretAccessKey=aws_secret_access_key,
                            SessionToken=aws_session_token,
                            bucket=self.resource,
                            Action=self.action,
                            RoleArn=self.rolearn,
                            RoleSessionName=self.rolesessionname,
                            externalid=self.externalid,
                            durationseconds=self.durationseconds,
                            region_name=region_name,
                            add_date=str(datetime.now()),
                            )
            session.add(new_db)
            session.commit()
        ins_log.read_log('info', '{}存库成功'.format(self.rolesessionname))

    def main(self):
        self.async_db()


if __name__ == '__main__':
    test = AWSSTS(region_name="",
                  aws_access_key_id="",
                  aws_secret_access_key="",
                  action='["s3:GetObject","s3:ListObject","s3:PutObject"]',
                  resource='arn:aws-cn:s3:::aws-logs-871006737058-cn-north-1',
                  rolearn='arn:aws-cn:iam::871006737058:role/test_lch',
                  rolesessionname='tesat',
                  externalid='1321a',
                  durationseconds=3600
                  )
    test.main()
