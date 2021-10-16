from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class DB(Base):
    __tablename__ = 'rds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    db_Identifier = Column('db_identifier', String(64), nullable=False)
    db_region = Column('db_region', String(64), nullable=False)
    db_host = Column('db_host', String(128), nullable=False)
    db_instance_id = Column('db_instance_id', String(64), nullable=False)
    db_conn = Column('db_conn', Boolean(), default=True)  # 是否符合七天内有链接 true：符合  False：不符合
    db_enncrypted = Column('db_enncrypted', Boolean(), default=True)  # 是否符合加密存储 true：符合  False：不符合
    db_public_access = Column('db_public_access', Boolean(), default=True)  # 是否符合关闭公网访问 true：符合  False：不符合
    db_backup = Column('db_backup', Boolean(), default=True, )  # 是否符合已开启备份功能 true：符合  False：不符合
    db_backup_period = Column('db_backup_period', Boolean(), default=True)  # 是否符合备份保存15天 true：符合  False：不符合
    update_time = Column('update_time', DateTime(), default=datetime.now, onupdate=datetime.now)
    account_id = Column('account_id', String(64))
    region = Column('region', String(64))
