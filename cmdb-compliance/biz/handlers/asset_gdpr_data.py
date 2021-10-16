from sqlalchemy import or_
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.gdpr_data import GdprData, model_to_dict


class GdprDataHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        gdpr_data_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                gdpr_data_info = session.query(GdprData).filter(
                    or_(GdprData.profile.like('%{}%'.format(key)),
                        GdprData.result.like('%{}%'.format(key)),
                        GdprData.level.like('%{}%'.format(key)),
                        GdprData.region.like('%{}%'.format(key)),
                        GdprData.account_id.like('%{}%'.format(key)),
                        GdprData.group.like('%{}%'.format(key)),
                        GdprData.group.like('%{}%'.format(key)),
                        GdprData.check_title.like('%{}%'.format(key)),
                        GdprData.check_output.like('%{}%'.format(key)))
                ).filter(
                    GdprData.result != "PASS"
                ).all()
            else:
                gdpr_data_info = session.query(GdprData).filter(
                    GdprData.result != "PASS"
                ).all()
        for data in gdpr_data_info:
            data_dict = model_to_dict(data)
            gdpr_data_list.append(data_dict)
        return gdpr_data_list


gdpr_data_host_urls = [
    (r"/v1/cmdb/gdpr_data/", GdprDataHandler),
]


if __name__ == '__main__':
    pass