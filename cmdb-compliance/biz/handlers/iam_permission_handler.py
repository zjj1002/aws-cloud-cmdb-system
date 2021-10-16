from sqlalchemy import or_

from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from websdk.db_context import DBContext
from models.permission_optimize import PermissionOptimize, model_to_dict


class IamPermissionHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        iam_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                iam_info = session.query(PermissionOptimize).filter(
                    or_(PermissionOptimize.user_name.like('%{}%'.format(key)),
                        PermissionOptimize.user_id.like('%{}%'.format(key)),
                        PermissionOptimize.user_arn.like('%{}%'.format(key)),
                        PermissionOptimize.services_name.like('%{}%'.format(key)),
                        PermissionOptimize.un_used_permission.like('%{}%'.format(key)))
                ).order_by(
                    PermissionOptimize.id
                ).all()
            else:
                iam_info = session.query(PermissionOptimize).order_by(
                    PermissionOptimize.id
                ).all()

        for data in iam_info:
            data_dict = model_to_dict(data)
            iam_list.append(data_dict)
        return iam_list


iam_permission_host_urls = [
    (r"/v1/cmdb/iam_permission/", IamPermissionHandler),
]


if __name__ == '__main__':
    pass