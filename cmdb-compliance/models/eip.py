
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class FreeEip(Base):

    __tablename__ = 'free_eip'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    public_ip = Column('public_ip', String(64), nullable=False)  # 公网ip
    allocation_id = Column('allocation_id', String(128), nullable=False)  # 分配的id
    public_ipv4_pool = Column('public_ipv4_pool', String(64), nullable=False)  # 公网ipv4池
    network_border_group = Column('network_border_group', String(128), nullable=False)  # 网络边界组
    is_used = Column('is_used', Integer, nullable=False)  # 是否使用Eip 0代表未使用  1代表使用


