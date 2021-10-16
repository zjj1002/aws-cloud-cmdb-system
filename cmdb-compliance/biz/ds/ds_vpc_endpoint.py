from libs.aws.endpoint import get_endpoint_list
from libs.db_context import DBContext
from models.vpc_endpoint import VpcEndpoint


def vpc_endpoint_sync_cmdb():
    """vpc_endpoint数据同步到数据库"""
    vpc_endpoint_list = get_endpoint_list()
    with DBContext('w') as session:
        session.query(VpcEndpoint).delete(synchronize_session=False)  # 清空数据库的所有记录
        for vpc_endpoint in vpc_endpoint_list:
            vpc_endpoint_id = vpc_endpoint.get("VpcEndpointId", "")
            vpc_id = vpc_endpoint.get("VpcId", "")
            service_name = vpc_endpoint.get("ServiceName", "")
            vpc_endpoint_type = vpc_endpoint.get("VpcEndpointType", "")
            state = vpc_endpoint.get("State", "")
            creation_timestamp = vpc_endpoint.get("CreationTimestamp", "")
            new_vpc_endpoint = VpcEndpoint(
                vpc_endpoint_id=vpc_endpoint_id, vpc_id=vpc_id, service_name=service_name,
                vpc_endpoint_type=vpc_endpoint_type, state=state, creation_timestamp=creation_timestamp
                )
            session.add(new_vpc_endpoint)
        session.commit()


if __name__ == '__main__':
    pass