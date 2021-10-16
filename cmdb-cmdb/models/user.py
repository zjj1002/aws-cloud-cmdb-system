
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class User(Base):
    """用户表"""
    __tablename__ = 'user'

    ID = Column('ID', String(128), primary_key=True, nullable=False)  # von登录账号
    password = Column('password', String(12))  # 密码
    name = Column('name', String(32))  # 名称
    department = Column('department', String(64))  # 部门名称
    project = Column('project', String(64))  # 项目名称
    phone = Column('phone', String(18))  # 电话
    email = Column('email', String(64))  # 邮箱
    status = Column('status', Integer)  # 状态 (0：禁用 1：启用 2：过期  3：正在初始化)
    over_time = Column('over_time', String(64))  # 过期时间


class LoginRecord(Base):
    """登录记录表"""
    __tablename__ = 'login_record'

    ID = Column('ID', String(32), primary_key=True, nullable=False)  # von登录账号
    name = Column('name', String(32))  # 名称
    op_type = Column('op_type', Integer)  # (0：登录 1：登出)
    op_result = Column('op_result', Integer)  # (0：成功 1：失败)
    ip_address = Column('ip_address', String(64))  # 登录源ip地址
    login_date = Column('login_date', String(64))  # 登录时间
    result_reason = Column('result_reason', Integer)  # (0：合法登录 1：已被禁用  2.已过期  3.认证失败)









