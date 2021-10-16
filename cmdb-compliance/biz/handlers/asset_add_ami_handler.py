import datetime

from tornado.web import RequestHandler
from websdk.db_context import DBContext

from libs.aws.session import get_aws_session
from libs.base_handler import BaseHandler
from libs.web_logs import ins_log
from models.com_ami import ComAmi
from models.uncom_ec2 import UnComEc2
from settings import settings


class AmiHandler(BaseHandler):

    def post(self, *args, **kwargs):
        """添加合规的ami信息"""
        key = self.get_argument('key', default=None, strip=True)
        with DBContext('w') as session:
            if not session.query(ComAmi).filter(ComAmi.ami_id == key).first():
                s = get_aws_session(**settings.get("aws_key"))
                clients = s.client("ec2")
                try:
                    resp_dict = clients.describe_images(ImageIds=[key])
                    ami_info = resp_dict.get("Images")[0]
                except Exception as e:
                    ami_info = None
                    ins_log.read_log("info", e)
                if ami_info:
                    try:
                        ami_name = ami_info["Name"]
                    except Exception as e:
                        ami_name = "UnKnown"
                        ins_log.read_log("info", e)
                    try:
                        tag = ami_info["Tags"]
                    except Exception as e:
                        tag = None
                        ins_log.read_log("info", e)
                    name = "UnKnown"
                    if tag:
                        for i in tag:
                            if i["Key"] == "Name":
                                name = i["Value"]

                    times = ami_info["CreationDate"]
                    utc_date = datetime.datetime.strptime(times, "%Y-%m-%dT%H:%M:%S.000Z")
                    local_date = utc_date + datetime.timedelta(hours=8)
                    created_times = datetime.datetime.strftime(local_date, '%Y-%m-%d %H:%M:%S')
                    describe = ami_info["Description"]
                    if not describe:
                        describe = "UnKnown"
                    new_ami = ComAmi(ami_id=key, ami_name=ami_name, name=name,
                                     creation_date=created_times, describe=describe,
                                     create_time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                    session.add(new_ami)
                else:
                    new_ami = ComAmi(ami_id=key, ami_name="UnKnown", name="UnKnown", describe="UnKnown",
                                     creation_date=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                     create_time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    session.add(new_ami)
                # 从数据库中删除ami相对应的ec2数据
                session.query(UnComEc2).filter(UnComEc2.ami_id == key).delete()
                session.commit()


ami_host_urls = [
    (r"/v1/cmdb/add_ami/", AmiHandler),
]


if __name__ == '__main__':
    pass