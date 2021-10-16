from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class FreeSgs(Base):

    __tablename__ = 'free_sgs'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    security_group_id = Column('security_group_id', String(128), nullable=False)  # 安全组id
    security_group_name = Column('security_group_name', String(255), nullable=False)  # 安全组名称
    to_port = Column('to_port', String(255), nullable=False)  # 端口
    ip_permissions_egress = Column('ip_permissions_egress', Text, nullable=False)  # IpRanges
    ip_permissions = Column('ip_permissions', Text, nullable=False)  # 限制ip
    vpc_id = Column('vpc_id', String(255), nullable=False)  # vpc id
    owner_id = Column('owner_id', String(255), nullable=False)  # owner id
    is_used = Column('is_used', Integer, nullable=False)  # 是否使用Eip 0代表未使用  1代表使用
    description = Column('description', String(512), nullable=False)  # 描述