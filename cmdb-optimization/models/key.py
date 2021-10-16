

from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class KEY(Base):
    __tablename__ = 'aws_key'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(80), unique=True, nullable=False)
    account = Column('account', String(50), nullable=False)
    account_id = Column('account_id', String(50), nullable=False)
    region = Column('region', String(50), nullable=False)
    access_id = Column('access_id', String(255))
    access_key = Column('access_key', String(255))
    aws_session_token = Column('aws_session_token', String(1024))
    durationseconds = Column('durationseconds', String(255))
    state = Column('state', String(50), nullable=False)
    add_time = Column('add_time', String(255))
    create_time = Column('create_time', DateTime(), default=datetime.now)
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)



