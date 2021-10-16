import csv
import codecs
import os

from libs.catch_execption import catch_exceptions_util
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.prowler_data import ProwlerData


@catch_exceptions_util
def prowler_sync_cmdb():
    """亚马逊CIS合规性检查数据入库"""
    # name = list(os.walk("/var/www/cmdb-compliance/prowler/output"))[0][-1][0]
    # filename = f"/var/www/cmdb-compliance/prowler/output/{name}"
    name = list(os.walk("./output"))[0][-1][0]
    filename = f"./output/{name}"
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        prowler_list = []
        for item in reader:
            if len(item) > 9:
                prowler_list.append(list(item)[:9])
            else:
                prowler_list.append(item)
    prowler_list.remove(prowler_list[0])
    length = len(prowler_list)
    step = 500
    with DBContext('w') as session:
        session.query(ProwlerData).delete(synchronize_session=False)  # 清空数据库的所有记录
        for i in range(0, length, step):
            for prowler in prowler_list[i: i + step]:
                ins_log.read_log('info', 'prowler信息：{}'.format(prowler))
                profile = prowler[0]
                account_id = prowler[1]
                region = prowler[2]
                check_id = float(prowler[3])
                result = prowler[4]
                group = prowler[5]
                level = prowler[6]
                check_title = prowler[7]
                check_output = prowler[8]
                new_data = ProwlerData(
                    profile=profile, result=result, level=level, region=region, account_id=account_id,
                    group=group, check_id=check_id, check_title=check_title, check_output=check_output
                )
                session.add(new_data)
            session.commit()


if __name__ == '__main__':
    prowler_sync_cmdb()