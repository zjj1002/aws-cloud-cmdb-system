# -*- coding: utf-8 -*-
# @Time    : 2020/6/11 
# @Author  : Fred liuchuanhao
# @File    : .py
# @Role    :

from tornado.web import RequestHandler
from models.asg import Asg as ASG_DB
from models.ebs import DB as EBS_DB
from models.uncom_ec2 import UnComEc2 as UNCOMEC2_DB
from models.eip import FreeEip as EIP_DB
from models.elb import ElbDB as ELB_DB
from models.elb import TargetGroupDB as TARGETGROUP_DB
from models.iam import DB as IAM_DB
from models.nat import DB as NAT_DB
from models.rds import DB as RDS_DB
from models.sgs import FreeSgs as SGS_DB
from models.uncom_vpc import UncomVpc as UNCOMVPC_DB
from models.uncom_vpc_peering import UncomVpcPeering as UNCOMVPCPEERING_DB
from models.gdpr_data import GdprData as GDPRDATA_DB
from models.hipaa_data import HipaaData as HIPAADATA_DB
from models.prowler_data import ProwlerData as PROLERDATA_DB
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler


class GatherComplianceHandler(BaseHandler):
    def get(self, *args, **kwargs):
        comliance_dict = {
                          "EBS": EBS_DB,
                          "ELB": ELB_DB,
                          "TARGETGROUP": TARGETGROUP_DB,
                          "IAM": IAM_DB,
                          "NAT": NAT_DB,
                          "RDS": RDS_DB,
                        }
        data = {}
        with DBContext('w') as session:
            for k,v in comliance_dict.items():
                re_data = session.query(v).all()
                data[k] = len(re_data)
            eipdata = session.query(EIP_DB).filter(EIP_DB.is_used == 0).all()
            data["eip"] = len(eipdata)
            sgsdata = session.query(SGS_DB).filter(SGS_DB.is_used == 0).order_by(SGS_DB.id).all()
            data["sgs"] = len(sgsdata)
            asgdata = session.query(ASG_DB).all()
            data["asg"] = len(asgdata)
            vpcdata = session.query(UNCOMVPC_DB).all()
            data["vpc"] = len(vpcdata)
            vpc_peeringdata = session.query(UNCOMVPCPEERING_DB).all()
            data["vpc_peeering"] = len(vpc_peeringdata)
            ec2_data = session.query(UNCOMEC2_DB).all()
            data["ec2"] = len(ec2_data)
            gdpr_data_info = session.query(GDPRDATA_DB).filter(GDPRDATA_DB.result == "FAIL").all()
            data["gdpr"] = len(gdpr_data_info)
            hipaa_data_info = session.query(HIPAADATA_DB).filter(HIPAADATA_DB.result == "FAIL").all()
            data["hippa"] = len(hipaa_data_info)
            prowler_data_info = session.query(PROLERDATA_DB).filter(PROLERDATA_DB.result == "FAIL").all()
            data["prowler"] = len(prowler_data_info)
        data = sorted(data.items(), key=lambda x: x[1])
        data = {i[0]:i[1] for i in data}
        return self.write(dict(code=0, msg='success', total=len(data),data=data))


aws_gather_urls = [
    (r"/v1/cmdb/gather/", GatherComplianceHandler),
]
