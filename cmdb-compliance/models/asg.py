from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class Asg(Base):

    __tablename__ = 'asg'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    asg_name = Column('asg_name', String(128), nullable=False)  # asg名称
    asg_arn = Column('asg_arn', String(255), nullable=False)  # amazon资源名称
    launch_template = Column('launch_template', String(128), nullable=False)  # 启用模板
    min_size = Column('min_size', Integer, nullable=False)  # 最小值
    max_size = Column('max_size', Integer, nullable=False)  # 最大值
    desirced_capacity = Column('desirced_capacity', Integer, nullable=False)  # 所需容量
    availability_zones = Column('availability_zones', String(32), nullable=False)  # 可用区
    health_check_type = Column('health_check_type', String(11), nullable=False)  # 运行状况检查类型
    asg_created_time = Column('asg_created_time', String(32), nullable=False)  # asg创建的时间

