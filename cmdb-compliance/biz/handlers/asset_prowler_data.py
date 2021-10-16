from sqlalchemy import or_
from websdk.db_context import DBContext
from libs.base_handler import BaseHandler
from libs.pagination import pagination_util
from models.prowler_data import ProwlerData, model_to_dict


class ProwlerDataHandler(BaseHandler):

    @pagination_util
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        prowler_data_list = []
        with DBContext('r') as session:
            if key:
                # 模糊查所有
                prowler_data_info = session.query(ProwlerData).filter(
                    or_(ProwlerData.profile.like('%{}%'.format(key)),
                        ProwlerData.result.like('%{}%'.format(key)),
                        ProwlerData.level.like('%{}%'.format(key)),
                        ProwlerData.region.like('%{}%'.format(key)),
                        ProwlerData.account_id.like('%{}%'.format(key)),
                        ProwlerData.group.like('%{}%'.format(key)),
                        ProwlerData.group.like('%{}%'.format(key)),
                        ProwlerData.check_title.like('%{}%'.format(key)),
                        ProwlerData.check_output.like('%{}%'.format(key)))
                ).filter(
                    ProwlerData.result != "PASS"
                ).all()
            else:
                prowler_data_info = session.query(ProwlerData).filter(
                    ProwlerData.result != "PASS"
                ).all()
        for data in prowler_data_info:
            data_dict = model_to_dict(data)
            prowler_data_list.append(data_dict)
        return prowler_data_list


prowler_data_host_urls = [
    (r"/v1/cmdb/unconventional_cis/", ProwlerDataHandler),
]


if __name__ == '__main__':
    pass