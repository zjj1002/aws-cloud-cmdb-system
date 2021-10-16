from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class OwnerList(Base):

    __tablename__ = 'owner_list'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # id自增
    owner_id = Column('owner_id', String(32), nullable=False)  # owner id
    name = Column('name', String(32))


