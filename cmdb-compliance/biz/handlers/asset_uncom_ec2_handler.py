from sqlalchemy import or_
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.uncom_ec2 import UnComEc2, model_to_dict


class UncomEc2Handler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        uncom_ec2_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                uncom_ec2_info = session.query(UnComEc2).filter(
                    or_(UnComEc2.instance_id.like('%{}%'.format(key)),
                        UnComEc2.ami_id.like('%{}%'.format(key)),
                        UnComEc2.instance_type.like('%{}%'.format(key)),
                        UnComEc2.key_name.like('%{}%'.format(key)),
                        UnComEc2.launch_time.like('%{}%'.format(key)),
                        UnComEc2.placement.like('%{}%'.format(key)),
                        UnComEc2.private_dns_name.like('%{}%'.format(key)),
                        UnComEc2.private_ip_address.like('%{}%'.format(key)),
                        UnComEc2.public_dns_name.like('%{}%'.format(key)),
                        UnComEc2.public_ip_address.like('%{}%'.format(key)))
                ).order_by(
                    UnComEc2.id
                ).all()
            else:
                uncom_ec2_info = session.query(UnComEc2).order_by(
                    UnComEc2.id
                ).all()

        for data in uncom_ec2_info:
            data_dict = model_to_dict(data)
            uncom_ec2_list.append(data_dict)
        return uncom_ec2_list


uncom_ec2_host_urls = [
    (r"/v1/cmdb/uncom_ec2/", UncomEc2Handler),
]


if __name__ == '__main__':
    pass