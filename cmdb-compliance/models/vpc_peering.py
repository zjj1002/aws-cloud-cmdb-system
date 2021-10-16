from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class VpcPeering(Base):

    __tablename__ = 'vpc_peering'

    id = Column('id', Integer, primary_key=True, autoincrement=True) # id自增
    vpc_peering_connection_id = Column('vpc_peering_connection_id', String(32), nullable=False)  # 对等连接id
    requester_cidr_block = Column('requester_cidr_block', String(32), nullable=False)  # 请求方的cidr块
    requester_owner_id = Column('requester_owner_id', String(32), nullable=False)  # 请求方的账户id
    requester_vpc_id = Column('requester_vpc_id', String(32), nullable=False)  # 请求方的vpc id
    requester_region = Column('requester_region', String(32), nullable=False)  # 请求方的区域
    accepter_cidr_block = Column('accepter_cidr_block', String(32), nullable=False)  # 接收方的cidr块
    accepter_owner_id = Column('accepter_owner_id', String(32), nullable=False)  # 接收方的账户id
    accepter_vpc_id = Column('accepter_vpc_id', String(32), nullable=False)  # 接收方的vpc id
    accepter_region = Column('accepter_region', String(32), nullable=False)  # 接收方的区域


