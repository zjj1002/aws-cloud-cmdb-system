
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class AllAssets(Base):
    """资产表"""
    __tablename__ = 'all_asset'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    service_name = Column('service_name', String(18), nullable=False)
    regions = Column('regions', String(18))
    operation = Column('operation', String(64))
    operation_data = Column('operation_data', JSON)


class DetailTable(Base):
    """操作方法详情表"""
    __tablename__ = 'detail_table'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    service_name = Column('service_name', String(18), nullable=False)
    regions = Column('regions', String(18))
    operation = Column('operation', String(64))
    temp_data = Column('temp_data', String(255))
    detail_data = Column('detail_data', JSON)
    __table_args__ = (UniqueConstraint('temp_data'),)



