from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class PermissionOptimize(Base):
    __tablename__ = 'permission_optimize'

    id = Column(Integer, primary_key=True, autoincrement=True)  # id自增
    user_name = Column('user_name', String(64), nullable=False)  # 用户名称
    user_id = Column('user_id', String(128), nullable=False)  # 用户id
    user_arn = Column('user_arn', String(255), nullable=False)  # 用户arn
    services_name = Column('services_name', String(128), nullable=False)  # 服务名称
    un_used_permission =Column('un_used_permission', String(128), nullable=False)  # 90天未使用的权限

