import csv
import codecs
import os

from libs.catch_execption import catch_exceptions_util
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.gdpr_data import GdprData


@catch_exceptions_util
def gdpr_sync_cmdb():
    """gdpr合规性检查数据入库"""
    name = list(os.walk("/var/www/cmdb-compliance/prowler/output"))[0][-1][0]
    filename = f"/var/www/cmdb-compliance/prowler/output/{name}"
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        gdpr_list = []
        for item in reader:
            if len(item) > 9:
                gdpr_list.append(list(item)[:9])
            else:
                gdpr_list.append(item)
    gdpr_list.remove(gdpr_list[0])
    with DBContext('w') as session:
        session.query(GdprData).delete(synchronize_session=False)  # 清空数据库的所有记录
        for gdpr in gdpr_list:
            ins_log.read_log('info', 'prowler信息：{}'.format(gdpr))
            profile = gdpr[0]
            account_id = gdpr[1]
            region = gdpr[2]
            check_id = float(gdpr[3])
            result = gdpr[4]
            group = gdpr[5]
            level = gdpr[6]
            check_title = gdpr[7]
            check_output = gdpr[8]
            new_data = GdprData(
                profile=profile, result=result, level=level, region=region, account_id=account_id,
                group=group, check_id=check_id, check_title=check_title, check_output=check_output
            )
            session.add(new_data)
        session.commit()
        ins_log.read_log('info', 'prowler写入数据库共{}条'.format(len(gdpr_list)))


if __name__ == '__main__':
    pass