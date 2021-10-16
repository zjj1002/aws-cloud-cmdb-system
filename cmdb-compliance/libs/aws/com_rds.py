import boto3
import datetime
from libs.web_logs import ins_log


class ComplianceRDSApi():
    def __init__(self, session):
        self.tag = "project" #筛选打了tag标签 但没开启加密存储的rds
        self.rds_list = []
        # 获取rds的client
        self.rds_client = session.client('rds')
        # 获取cloudwatch的client
        self.cloudwatch_client = session.client('cloudwatch')

    def get_describe_db_instances_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        db_instances_list = []
        try:
            response_data = self.rds_client.describe_db_instances()
            for each in response_data["DBInstances"]:
                db_instances_list.append(each["DBInstanceIdentifier"])

        except Exception as e:
            err = e
        return response_data, err, db_instances_list

    def get_tags_response(self, arn):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.rds_client.list_tags_for_resource(
                ResourceName=arn)
        except Exception as e:
            err = e
        return response_data, err

    def get_conn_cloudwatch_response(self, id):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        StartTime = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        EndTime = datetime.datetime.utcnow()
        try:
            response_data = self.cloudwatch_client.get_metric_statistics(Namespace='AWS/RDS',
                                                                         MetricName='DatabaseConnections',
                                                                         Dimensions=[dict(Name='DBInstanceIdentifier',
                                                                                          Value=id)],
                                                                         Period=60 * 60 * 24 * 7,  # 取七天内的数据
                                                                         StartTime=StartTime,
                                                                         EndTime=EndTime,
                                                                         Statistics=['Maximum'],
                                                                         Unit='Count')
        except Exception as e:
            err = e
        return response_data, err

    def get_not_compliance_rds_data(self):
        """
        获取返回值
        :return:
        """
        response_data, err, _ = self.get_describe_db_instances_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False
        list1 = []
        for each in response_data["DBInstances"]:
            rds_data = {}
            response_data_cloudwatach, err = self.get_conn_cloudwatch_response(each["DBInstanceIdentifier"])
            if err:
                ins_log.read_log('error', '获取cloudwatch失败：{}'.format(err))
                return False
            num = int(response_data_cloudwatach["Datapoints"][0].get('Maximum'))

            if each["PubliclyAccessible"] == True or each["BackupRetentionPeriod"] == 0 or each[
                "BackupRetentionPeriod"] < 15 or each["StorageEncrypted"] == False or num == 0:
                # 判断七天内的连接数是否为0
                if num == 0:
                    rds_data['db_conn'] = False
                else:
                    rds_data['db_conn'] = True
                # 判断是否符合已关闭公网访问
                if each["PubliclyAccessible"] == False:
                    rds_data['db_public_access'] = True
                else:
                    rds_data['db_public_access'] = False
                # 判断是否符合已打开自动备份
                if each["BackupRetentionPeriod"] == 0:
                    rds_data['db_backup'] = False
                else:
                    rds_data['db_backup'] = True
                # 判断是否符合已自动备份时间超过15天
                if each["BackupRetentionPeriod"] >= 15:
                    rds_data['db_backup_period'] = True
                else:
                    rds_data['db_backup_period'] = False
                # 判断tag是type的rds 是否启用加密
                tag_response, err = self.get_tags_response(each.get('DBInstanceArn'))
                if err:
                    ins_log.read_log('error', '获取rds的tag失败：{}'.format(err))
                    return False
                key_list = []
                for x in tag_response["TagList"]:
                    key_list.append(x["Key"])
                if each["StorageEncrypted"] == False and self.tag in key_list:
                    rds_data['db_enncrypted'] = False
                else:
                    rds_data['db_enncrypted'] = True
                # 提取其他数据
                rds_data['db_Identifier'] = each.get('DBInstanceIdentifier')
                rds_data['db_region'] = each.get('AvailabilityZone')
                rds_data['db_host'] = each.get('Endpoint').get('Address')
                rds_data['db_instance_id'] = each.get('DbiResourceId')
                self.rds_list.append(rds_data)
                list1.append(rds_data['db_Identifier'])
        return self.rds_list

    def get_all_db_info(self):
        self.get_not_compliance_rds_data()

        return self.rds_list

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.rds_client.describe_db_instances()

        return response_data
