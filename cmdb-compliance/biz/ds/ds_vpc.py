from libs.aws.vpc import get_vpc_list
from libs.db_context import DBContext
from models.vpc import Vpc


def vpc_sync_cmdb():
    """vpc数据同步到数据库"""
    vpc_list = get_vpc_list()
    with DBContext('w') as session:
        session.query(Vpc).delete(synchronize_session=False)  # 清空数据库的所有记录
        for vpc in vpc_list:
            vpc_id = vpc.get("VpcId", "")
            state = vpc.get("State", "")
            cidr_block = vpc.get("CidrBlock", "")
            dhcp_options_id = vpc.get("DhcpOptionsId", "")
            new_vpc = Vpc(
                vpc_id=vpc_id, state=state, cidr_block=cidr_block,dhcp_options_id=dhcp_options_id)
            session.add(new_vpc)
        session.commit()


if __name__ == '__main__':
    pass