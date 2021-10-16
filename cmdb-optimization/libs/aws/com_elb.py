import boto3
from libs.web_logs import ins_log


class ComplianceELBApi():
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

    def get_unused_elb_list(self):
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
            if len(each["Instances"]) == 0 or each["Scheme"] == "internet-facing":
                # 判断elb是否符合在使用
                if len(each["Instances"]) == 0:
                    elb["is_use"] = False
                else:
                    elb["is_use"] = True
                # 判断elb是内网还是公网访问
                elb["scheme"] = each.get("Scheme", "")
                if elb["scheme"] == "internet-facing":
                    # 判断公网访问的传输协议是否加密
                    for listener in each["ListenerDescriptions"]:
                        if listener["Listener"]["Protocol"] != "HTTPS" or listener["Listener"][ "Protocol"] != "SSL":
                            elb["is_encry_trans"] = False
                            break
                        else:
                            elb["is_encry_trans"] = True

                elif elb["scheme"] == "internal":
                    elb["is_encry_trans"] = True
                else:
                    elb["is_encry_trans"] = True
                # 获取其他数据
                elb["name"] = each.get("LoadBalancerName")
                elb["dnsname"] = each.get("DNSName")
                elb["region"] = "/".join(each.get("AvailabilityZones"))
                elb["vpcid"] = each.get("VPCId")
                elb["type"] = "network"
                self.elb_list.append(elb)
        return self.elb_list

    def get_unused_elbv2_list(self):
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
            if each["State"] == "failed" or each["Scheme"] == "internet-facing":
                elb["load_balancer_arn"] = each.get("LoadBalancerArn", "")
                if each["State"] == "failed":
                    elb["is_use"] = False
                else:
                    elb["is_use"] = True

                elb["scheme"] = each.get("Scheme", "")
                if elb["scheme"] == "internet-facing":
                    response_data, _ = self.get_elv2_describe_listeners_response(
                        LoadBalancerArn=elb["load_balancer_arn"])
                    for listener in response_data["Listeners"]:
                        if listener["Protocol"] != "HTTPS" or listener["Protocol"] != "TLS":
                            elb["is_encry_trans"] = False
                            break
                        else:
                            elb["is_encry_trans"] = True
                else:
                    elb["is_encry_trans"] = True
                elb["name"] = each.get("LoadBalancerName")
                elb["dnsname"] = each.get("DNSName")
                elb["region"] = "/".join([i["ZoneName"] for i in each["AvailabilityZones"]])
                elb["vpcid"] = each.get("VpcId")
                elb["type"] = each.get("Type")
                self.elb_list.append(elb)

        return self.elb_list

    def main(self):
        self.get_unused_elb_list()
        self.get_unused_elbv2_list()
        return self.elb_list

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        elb_response_data = self.elb_client.describe_load_balancers()
        elbv2_response_data = self.elbv2_client.describe_load_balancers()

        return elb_response_data, elbv2_response_data


class ComplianceTargetGroupsApi():
    def __init__(self, session):
        self.TargetGroups_list = []
        # 获取elb的client
        self.elbv2_client = session.client('elbv2')

    def get_target_groups_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.elbv2_client.describe_target_groups()
        except Exception as e:
            err = e
        return response_data, err

    def get_unused_target_groups_list(self):
        """
        获取返回值
        :return:
        """
        response_data, err = self.get_target_groups_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False

        for each in response_data["TargetGroups"]:
            TargetGroups = {}
            if len(each["LoadBalancerArns"]) == 0:
                TargetGroups["is_use"] = False
                TargetGroups["target_group_arn"] = each.get("TargetGroupArn")
                TargetGroups["target_group_name"] = each.get("TargetGroupName")
                TargetGroups["protocol"] = each.get("Protocol")
                TargetGroups["port"] = each.get("Port")
                TargetGroups["vpc_id"] = each.get("VpcId")
                TargetGroups["target_type"] = each.get("TargetType")
                self.TargetGroups_list.append(TargetGroups)
        return self.TargetGroups_list

    def main(self):
        result = self.get_unused_target_groups_list()

        return result

    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.elbv2_client.describe_target_groups()

        return response_data
