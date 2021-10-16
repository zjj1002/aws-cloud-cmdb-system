
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class TagList(Base):
    """标签表"""
    __tablename__ = 'tag_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    key = Column('key', String(128), nullable=False)  # 标签的key
    value = Column('value', Text)  # 合规的value的一个列表
    describe = Column('describe', String(255))  # 标签的描述
    service_name = Column('service_name', String(255)) # 标签关联的服务
    __table_args__ = (UniqueConstraint('key'),)


class ServicesList(Base):
    """服务表"""
    __tablename__ = 'services_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    services_name = Column('services_name', String(128), nullable=False)  # 服务的名称
    __table_args__ = (UniqueConstraint('services_name'),)


class ServicesTagMiddle(Base):
    """服务标签中间表"""
    __tablename__ = 'services_tag_middle'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    tag_id = Column(Integer, ForeignKey("tag_list.id"))  # 标签的id
    services_id = Column(Integer, ForeignKey("services_list.id"))  # 服务的id
    __table_args__ = (UniqueConstraint('tag_id', 'services_id'),)


class ResultList(Base):
    """查询出来的一个结果表"""
    __tablename__ = 'result_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    services_name = Column('services_name', String(128), nullable=False)  # 服务的名称
    services_resource_id = Column('services_resource_id', String(256), nullable=False)  # 服务资源的id
    key = Column('key', String(128), nullable=False)  # 标签的key
    value = Column('value', String(255))  # 标签的value
    is_valid = Column('is_valid', Integer, nullable=False)  # 是否是有效的（1代表true, 0代表false)


class ChangeResultList(Base):
    """修改检测结果表"""
    __tablename__ = 'change_result_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    services_name = Column('services_name', String(128), nullable=False)  # 服务的名称
    services_resource_id = Column('services_resource_id', String(128), nullable=False)  # 服务资源的id
    key = Column('key', String(128), nullable=False)  # 标签的key
    value = Column('value', String(255))  # 标签的value


class EC2Instance(Base):
    """ec2实例表"""
    __tablename__ = 'ec2_instance_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    service_name = Column('service_name', String(128), nullable=False)  # 服务的名称
    instance_id = Column('instance_id', String(255), nullable=False)  # 实例id
    instance_type = Column('instance_type', String(128))  # 实例类型
    tag_name = Column('tag_name', String(64))  # Name标签的值
    private_ip = Column('private_ip', String(64))  # 私有IP
    uptime = Column('uptime', String(64))  # 开机时间
    downtime = Column('downtime', String(64))  # 关机时间

