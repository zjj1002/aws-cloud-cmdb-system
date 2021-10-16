from tornado.web import RequestHandler
from libs.base_handler import BaseHandler
from sqlalchemy import or_
from libs.pagination import pagination_util
from models.rds import DB, model_to_dict
from websdk.db_context import DBContext
from biz.ds.ds_rds import main as  aws_rds_refresh


class GetRdsHandler(BaseHandler):
    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        button = int(self.get_argument('button', default='0', strip=True))
        if button == 1:
            aws_rds_refresh()
        rds_list = []
        with DBContext('w') as session:
            if key:
                rds_info = session.query(DB).filter(
                    or_(DB.db_Identifier.like('%{}%'.format(key)),
                        DB.db_region.like('%{}%'.format(key)),
                        DB.db_host.like('%{}%'.format(key)),
                        DB.db_instance_id.like('%{}%'.format(key)),
                        )
                ).filter(or_(DB.db_conn == False,
                             DB.db_public_access == False,
                             DB.db_backup == False,
                             DB.db_enncrypted == False,
                             DB.db_backup_period == False)
                         ).all()

            else:
                rds_info = session.query(DB).filter(
                    or_(DB.db_conn == False,
                        DB.db_public_access == False,
                        DB.db_backup == False,
                        DB.db_enncrypted == False,
                        DB.db_backup_period == False)
                ).all()

        for data in rds_info:
            data_dict = model_to_dict(data)
            data_dict.pop("update_time")
            rds_list.append(data_dict)
        return rds_list


aws_rds_urls = [
    (r"/v1/cmdb/rds/", GetRdsHandler ),
]
