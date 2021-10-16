from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class VpcEndpoint(Base):

    __tablename__ = 'vpc_endpoint'

    id = Column('id', Integer, primary_key=True, autoincrement=True) # id自增
    vpc_endpoint_id = Column('vpc_endpoint_id', String(32), nullable=False)  # vpc终端节点id
    vpc_id = Column('vpc_id', String(32), nullable=False)  # vpc id
    service_name = Column('service_name', String(32), nullable=False)  # 服务名称
    vpc_endpoint_type = Column('vpc_endpoint_type', String(18), nullable=False)  # vpc终端节点类型
    state = Column('state', String(18), nullable=False)  # 状态
    creation_timestamp = Column('creation_timestamp', String(64), nullable=False)  # 终端节点创建时间



