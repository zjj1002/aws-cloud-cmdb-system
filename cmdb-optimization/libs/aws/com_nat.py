import boto3
from libs.web_logs import ins_log


class ComplianceNatGateWayApi():
    def __init__(self, session):
        self.nat_list = []
        # 获取ec2的client
        self.nat_client = session.client('ec2')

    def get_nat_gate_ways_response(self):
        """
        获取返回值
        :return:
        """
        response_data = {}
        err = None
        try:
            response_data = self.nat_client.describe_nat_gateways()
        except Exception as e:
            err = e
        return response_data, err

    def get_unused_nat_list(self):
        """
        获取返回值
        :return:
        """
        response_data, err = self.get_nat_gate_ways_response()

        if err:
            ins_log.read_log('error', '获取失败：{}'.format(err))
            return False

        # pending | failed | available | deleting | deleted
        for each in response_data["NatGateways"]:
            nat_dict ={}
            if each["State"] != "available":
                nat_dict["is_use"] = False
                nat_dict["natgatewayid"] = each["NatGatewayId"]
                nat_dict["state"] = each["State"]
                nat_dict["subnetId"] = each["SubnetId"]
                nat_dict["vpcid"] = each["VpcId"]
                nat_dict["createTime"] = each["CreateTime"]
                self.nat_list.append(nat_dict)
        return self.nat_list

    def main(self):
        result = self.get_unused_nat_list()
        return result


    def test_auth(self):
        """
        测试接口权限等信息是否异常
        :return:
        """
        response_data = self.nat_client.describe_nat_gateways()

        return response_data




