from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class Ami(Base):

    __tablename__ = 'ami'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    ami_id = Column('ami_id', String(32), nullable=False)  # ami的id
    # ami_name = Column('ami_name', String(32), nullable=False)  # ami的名称
    # image_location = Column('image_location', String(18), nullable=False)  #
    # owner_id = Column('owner_id', String(32), nullable=False)  #
    # image_type = Column('image_type', String(32), nullable=False)  #
    # creation_date = Column('creation_date', String(32), nullable=False)  #
    # state = Column('state', String(18), nullable=False)  #
    # architecture = Column('architecture', String(18), nullable=False)  #
