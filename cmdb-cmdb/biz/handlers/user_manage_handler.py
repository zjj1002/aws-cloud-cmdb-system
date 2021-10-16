import string
import random
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import or_
from tornado.web import RequestHandler

from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext
from models.user import User, model_to_dict, LoginRecord


class UserManageHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询出用户数据接口"""
        search_key = self.get_argument('search_key', default=None, strip=True)
        user_list = []
        with DBContext('r') as session:
            if search_key:
                # 模糊查所有
                user_info = session.query(User).filter(
                    or_(User.ID.like('%{}%'.format(search_key)),
                        User.password.like('%{}%'.format(search_key)),
                        User.name.like('%{}%'.format(search_key)),
                        User.department.like('%{}%'.format(search_key)),
                        User.project.like('%{}%'.format(search_key)),
                        User.phone.like('%{}%'.format(search_key)),
                        User.email.like('%{}%'.format(search_key)),
                        User.over_time.like('%{}%'.format(search_key)))
                ).order_by(
                    User.ID
                ).all()
            else:
                user_info = session.query(User).order_by(
                    User.ID
                ).all()
        for data in user_info:
            data_dict = model_to_dict(data)
            dates = datetime.datetime.now().date()
            if data_dict["over_time"] == str(dates):
                data_dict["status"] = 2
            data_dict["password"] = data_dict["password"][:5] + "***"
            user_list.append(data_dict)
        return user_list

    def post(self, *args, **kwargs):
        """添加用户"""
        ID = self.get_argument('ID', default=None, strip=True)
        name = self.get_argument('name', default=None, strip=True)
        department = self.get_argument('department', default=None, strip=True)
        project = self.get_argument('project', default=None, strip=True)
        phone = self.get_argument('phone', default=None, strip=True)
        email = self.get_argument('email', default=None, strip=True)

        num = random.sample(string.digits, 1)  # 随机取1位数字
        lower = random.sample(string.ascii_lowercase, 1)  # 随机取1位小写字母
        upper = random.sample(string.ascii_uppercase, 1)  # 随机取1位大写字母
        other = random.sample(string.ascii_letters + string.digits, 5)  # 随机取5位
        password_list = num + lower + upper + other  # 产生的8位密码
        password = "".join(password_list)
        over_time = datetime.date.today() + relativedelta(days=+90)  # 过期时间
        if not all([ID, name, email, phone]):
            return self.write(dict(code=-2, msg='关键参数不能为空'))

        with DBContext('r') as session:
            exist_id = session.query(User.ID).filter(User.ID == ID).first()
        if exist_id:
            return self.write(dict(code=-2, msg='不要重复记录,已存在该用户'))
        with DBContext('w') as session:
            new_user = User(
                ID=ID, name=name, department=department, project=project,
                phone=phone, email=email, password=password, status=3, over_time=str(over_time)
            )
            session.add(new_user)
            session.commit()
        return self.write(dict(code=0, msg='添加用户成功'))

    def delete(self, *args, **kwargs):
        """删除用户(可以批量删除，也可以单个删除)"""
        ID = self.get_argument('ID', default=None, strip=True)  # 批量传入
        id_list = ID.split(',')
        with DBContext('r') as session:
            for id in id_list:
                session.query(User).filter(User.ID == id).delete()
            session.commit()
        return self.write(dict(code=0, msg='删除成功'))


class ResetPasswordHandler(BaseHandler):

    def put(self, *args, **kwargs):
        """重置密码接口"""
        ID = self.get_argument('ID', default=None, strip=True)
        with DBContext('w') as session:
            user_info = session.query(User).filter(User.ID == ID).first()
            num = random.sample(string.digits, 1)  # 随机取1位数字
            lower = random.sample(string.ascii_lowercase, 1)  # 随机取1位小写字母
            upper = random.sample(string.ascii_uppercase, 1)  # 随机取1位大写字母
            other = random.sample(string.ascii_letters + string.digits, 5)  # 随机取5位
            password_list = num + lower + upper + other  # 产生的8位密码
            password = "".join(password_list)
            if user_info:
                user_info.password = password
                session.commit()
        return self.write(dict(code=0, msg='重置密码成功'))


class ResetOverTimeHandler(BaseHandler):

    def put(self, *args, **kwargs):
        """修改过期时间接口"""
        ID = self.get_argument('ID', default=None, strip=True)
        times = self.get_argument('times', default=None, strip=True)  # 2020-12-20 传入时间 字符串
        with DBContext('w') as session:
            user_info = session.query(User).filter(User.ID == ID).first()
            user_info.over_time = times
            session.commit()
        return self.write(dict(code=0, msg='修改时间成功'))


class StartStopHandler(BaseHandler):

    def post(self, *args, **kwargs):
        """启用账号/禁用账号功能接口"""
        ID = self.get_argument('ID', default=None, strip=True)
        key = self.get_argument('key', default=None, strip=True)
        id_list = ID.split(',')
        if key == "启用账号" or key == "批量启用":
            with DBContext('w') as session:
                for id in id_list:
                    user_info = session.query(User).filter(User.ID == id).first()
                    user_info.status = 1
                session.commit()
            return self.write(dict(code=0, msg='启用成功'))
        elif key == "禁用账号" or key == "批量禁用":
            with DBContext('w') as session:
                for id in id_list:
                    user_info = session.query(User).filter(User.ID == id).first()
                    user_info.status = 0
                session.commit()
            return self.write(dict(code=0, msg='禁用成功'))


class LoginRecordHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        """查询出用户登录记录接口"""
        search_key = self.get_argument('search_key', default=None, strip=True)
        login_list = []
        with DBContext('r') as session:
            if search_key:
                # 模糊查所有
                login_info = session.query(LoginRecord).filter(
                    or_(LoginRecord.ID.like('%{}%'.format(search_key)),
                        LoginRecord.name.like('%{}%'.format(search_key)),
                        LoginRecord.ip_address.like('%{}%'.format(search_key)),
                        LoginRecord.login_date.like('%{}%'.format(search_key)))
                ).order_by(
                    LoginRecord.ID
                ).all()
            else:
                login_info = session.query(LoginRecord).order_by(
                    LoginRecord.ID
                ).all()
        if login_info:
            for data in login_info:
                data_dict = model_to_dict(data)
                login_list.append(data_dict)
        return login_list


user_manage_host_urls = [
    (r"/v1/cmdb/user_manage/", UserManageHandler),
    (r"/v1/cmdb/reset_password/", ResetPasswordHandler),
    (r"/v1/cmdb/reset_time/", ResetOverTimeHandler),
    (r"/v1/cmdb/start_or_stop_user/", StartStopHandler),
    (r"/v1/cmdb/login_record/", LoginRecordHandler),
]


if __name__ == '__main__':
    pass
