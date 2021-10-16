from sqlalchemy import or_
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.hipaa_data import HipaaData, model_to_dict


class HipaaDataHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        hipaa_data_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                hipaa_data_info = session.query(HipaaData).filter(
                    or_(HipaaData.profile.like('%{}%'.format(key)),
                        HipaaData.result.like('%{}%'.format(key)),
                        HipaaData.level.like('%{}%'.format(key)),
                        HipaaData.region.like('%{}%'.format(key)),
                        HipaaData.account_id.like('%{}%'.format(key)),
                        HipaaData.group.like('%{}%'.format(key)),
                        HipaaData.group.like('%{}%'.format(key)),
                        HipaaData.check_title.like('%{}%'.format(key)),
                        HipaaData.check_output.like('%{}%'.format(key)))
                ).filter(
                    HipaaData.result != "PASS"
                ).all()
            else:
                hipaa_data_info = session.query(HipaaData).filter(
                    HipaaData.result != "PASS"
                ).all()
        for data in hipaa_data_info:
            data_dict = model_to_dict(data)
            hipaa_data_list.append(data_dict)
        return hipaa_data_list


hipaa_data_host_urls = [
    (r"/v1/cmdb/hipaa_data/", HipaaDataHandler),
]


if __name__ == '__main__':
    pass