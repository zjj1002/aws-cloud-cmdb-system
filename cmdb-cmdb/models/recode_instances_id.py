
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class RecordInstanceId(Base):
    """需要开关机的实例Id表"""
    __tablename__ = 'record_instances_id'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    instances_id = Column('instances_id', String(128), nullable=False)  # 实例id
    __table_args__ = (UniqueConstraint('instances_id'),)