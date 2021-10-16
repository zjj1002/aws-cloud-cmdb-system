#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
date   : 2017-10-11
role   : Application
"""
from awssts.hanllder.sts_handler import aws_sts_urls
from biz.handlers.asset_add_ami_handler import ami_host_urls
from biz.handlers.asset_add_owner_handler import add_owner_id_host_urls
from biz.handlers.asset_asg_handler import asg_host_urls
from biz.handlers.asset_com_ami_handler import com_ami_host_urls
from biz.handlers.asset_eip_handler import eip_host_urls
from biz.handlers.asset_gdpr_data import gdpr_data_host_urls
from biz.handlers.asset_hipaa_data import hipaa_data_host_urls
from biz.handlers.asset_owner_handler import owner_id_host_urls
from biz.handlers.asset_prowler_data import prowler_data_host_urls
from biz.handlers.asset_sgs_handler import sgs_host_urls
from biz.handlers.iam_handler import aws_iam_urls
from clair.handler.clair_scan_hanlder import aws_clair_urls
from kube_bench.handler.kube_bench_hanlder import aws_kube_scan_urls
from pocsuite.hanlder.scan_hander import aws_poc_urls
from gitsecrets.hanlder.git_secret_handler import aws_code_scan_urls
from websdk.application import Application as myApplication

#from biz.handlers.asset_server_handler import asset_server_urls
#from biz.handlers.asset_db_handler import asset_db_urls
#from biz.handlers.admin_user_handler import admin_user_urls
#from biz.handlers.asset_tag_handler import tag_urls
#from biz.handlers.system_user_handler import system_user_urls
#from biz.handlers.asset_configs_handler import asset_configs_urls
#from biz.handlers.hand_update_asset_handler import asset_hand_server_urls
#from biz.handlers.aws_events_handler import aws_events_urls
#from biz.handlers.asset_idc_handler import asset_idc_urls
#from biz.handlers.asset_operational_audit_handler import asset_audit_urls
#from biz.handlers.dangers_opened_port_host_handler import security_host_urls
#from biz.handlers.asset_s3_handler import s3_host_urls
#from biz.handlers.aws_ebs_handler import ebs_urls
#from biz.handlers.asset_dns_handler import dns_host_urls
from biz.handlers.asset_uncom_ec2_handler import uncom_ec2_host_urls
from biz.handlers.asset_uncom_vpc import uncom_vpc_host_urls
from biz.handlers.asset_uncom_vpc_peering_handler import uncom_vpc_peering_host_urls
from biz.handlers.iam_permission_handler import iam_permission_host_urls
from biz.handlers.rds_handler import aws_rds_urls
from biz.handlers.nat_handler import aws_nat_urls
from biz.handlers.elb_handler import aws_elb_urls
from biz.handlers.ebs_handler import aws_ebs_urls
from biz.handlers.gather_compliance import aws_gather_urls



class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(eip_host_urls)
        urls.extend(sgs_host_urls)
        urls.extend(asg_host_urls)
        urls.extend(uncom_ec2_host_urls)
        urls.extend(ami_host_urls)
        urls.extend(aws_rds_urls)
        urls.extend(aws_nat_urls)
        urls.extend(aws_elb_urls)
        urls.extend(aws_iam_urls)
        urls.extend(uncom_vpc_host_urls)
        urls.extend(uncom_vpc_peering_host_urls)
        urls.extend(prowler_data_host_urls)
        urls.extend(gdpr_data_host_urls)
        urls.extend(hipaa_data_host_urls)
        urls.extend(com_ami_host_urls)
        urls.extend(owner_id_host_urls)
        urls.extend(add_owner_id_host_urls)
        urls.extend(aws_poc_urls)
        urls.extend(aws_clair_urls)
        urls.extend(aws_code_scan_urls)
        #urls.extend(s3_host_urls)
        urls.extend(aws_ebs_urls)
        urls.extend(aws_gather_urls)
        urls.extend(iam_permission_host_urls)
        urls.extend(aws_sts_urls)
        #urls.extend(dns_host_urls)
        urls.extend(aws_kube_scan_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
