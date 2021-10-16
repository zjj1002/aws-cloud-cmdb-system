from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class UnComEc2(Base):

    __tablename__ = 'uncom_ec2'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # id自增
    instance_id = Column('instance_id', String(32), nullable=False)  # 实例id
    ami_id = Column('ami_id', String(32), nullable=False)  # 不合规的ami id
    instance_type = Column('instance_type', String(32), nullable=False)  # 实例类型
    key_name = Column('key_name', String(128), nullable=False)  # 密钥对名称
    launch_time = Column('launch_time', String(32), nullable=False)  # 启动时间
    placement = Column('placement', String(128), nullable=False)  # 置放信息
    private_dns_name = Column('private_dns_name', String(64), nullable=False)  # 私有dns名称
    private_ip_address = Column('private_ip_address', String(18), nullable=False)  # 私有ip
    public_dns_name = Column('public_dns_name', String(64), nullable=False)  # 公有dns名称
    public_ip_address = Column('public_ip_address', String(18), nullable=False)  # 公有ip

