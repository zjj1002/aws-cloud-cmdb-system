from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class ComAmi(Base):

    __tablename__ = 'com_ami'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    ami_id = Column('ami_id', String(32), nullable=False)  # ami的id
    ami_name = Column('ami_name', String(32), nullable=False)  # ami的名称
    name = Column('name', String(32), nullable=False)   # tag里面的Name
    creation_date = Column('creation_date', String(64), nullable=False)  # AMI创建时间
    describe = Column('describe', String(255), nullable=False)  # 描述
    create_time = Column('create_time', String(64), nullable=False)  # AMI记录添加时间


