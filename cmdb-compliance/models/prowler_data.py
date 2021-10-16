
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class ProwlerData(Base):

    __tablename__ = 'prowler_data'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # ID自增长
    profile = Column('profile', String(18), nullable=False)  #
    result = Column('result', String(18), nullable=False)  #
    level = Column('level', String(18), nullable=False)  #
    region = Column('region', String(32), nullable=False)  #
    account_id = Column('account_id', String(18), nullable=False)  #
    group = Column('group', String(18), nullable=False)
    check_id = Column('check_id', Float, nullable=False)
    check_title = Column('check_title', String(255), nullable=False)
    check_output = Column('check_output', String(255), nullable=False)



