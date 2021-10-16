import boto3
from libs.web_logs import ins_log


class ELBApi():
    def __init__(self, session):
        self.elb_list = []
        # 获取elb的client
        self.elb_client = session.client('elb')
        self.elbv2_client = session.client('elbv2')

    def get_elb_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.elb_client.describe_load_balancers()
        except Exception as e:
            err = e
        return response_data, err

    def get_elbv2_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.elbv2_client.describe_load_balancers()
        except Exception as e:
            err = e
        return response_data, err

    def get_elv2_describe_listeners_response(self, LoadBalancerArn):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.elbv2_client.describe_listeners(LoadBalancerArn=LoadBalancerArn)
        except Exception as e:
            err = e
        return response_data, err

    def get_elb_list(self):
        """
        获取返回值
        :return:
        """
        response_data, err = self.get_elb_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False

        for each in response_data["LoadBalancerDescriptions"]:
            elb = {}
            instance = []
            elb["name"] = each.get("LoadBalancerName")
            elb["LoadBalancerArn"] = each.get("LoadBalancerArn")
            elb["dnsname"] = each.get("DNSName")
            if each["Instances"]:
                for i in each["Instances"]:
                    instance.append(i["InstanceId"])
            elb["instance"] =instance
            self.elb_list.append(elb)
        return self.elb_list

    def get_elbv2_list(self):
        """
        获取返回值
        :return:
        """
        response_data, err = self.get_elbv2_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False
        for each in response_data["LoadBalancers"]:
            elb = {}
            elb["LoadBalancerArn"] = each.get("LoadBalancerArn")
            elb["name"] = each.get("LoadBalancerName")
            elb["dnsname"] = each.get("DNSName")
            instance_list  = []
            response = self.elbv2_client.describe_target_groups(LoadBalancerArn=each.get("LoadBalancerArn"))
            if response['TargetGroups']:
                for i in response['TargetGroups']:
                    response1 = self.elbv2_client.describe_target_health(TargetGroupArn=i['TargetGroupArn'])
                    if response1['TargetHealthDescriptions']:
                        for m in response1['TargetHealthDescriptions']:
                            instance_list.append(m["Target"]["Id"])
            elb["instance"] = list(set(instance_list))
            self.elb_list.append(elb)
        return self.elb_list

    def main(self):
        self.get_elb_list()
        self.get_elbv2_list()
        return self.elb_list

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        elb_response_data = self.elb_client.describe_load_balancers()
        elbv2_response_data = self.elbv2_client.describe_load_balancers()

        return elb_response_data, elbv2_response_data
