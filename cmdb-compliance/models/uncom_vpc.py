from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class UncomVpc(Base):

    __tablename__ = 'uncom_vpc'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # id自增
    vpc_id = Column('vpc_id', String(64), primary_key=True)  # vpc id
    state = Column('state', String(32), nullable=False)  # 状态
    cidr_block = Column('cidr_block', String(32), nullable=False)  # cidr块
    dhcp_options_id = Column('dhcp_options_id', String(32), nullable=False)  # dhcp选择集id


