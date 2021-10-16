import csv
import codecs
import os

from libs.catch_execption import catch_exceptions_util
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.hipaa_data import HipaaData


@catch_exceptions_util
def hipaa_sync_cmdb():
    """hipaa合规性检查数据入库"""
    name = list(os.walk("/var/www/cmdb-compliance/prowler/output"))[0][-1][0]
    filename = f"/var/www/cmdb-compliance/prowler/output/{name}"
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        hipaa_list = []
        for item in reader:
            if len(item) > 9:
                hipaa_list.append(list(item)[:9])
            else:
                hipaa_list.append(item)
    hipaa_list.remove(hipaa_list[0])
    with DBContext('w') as session:
        session.query(HipaaData).delete(synchronize_session=False)  # 清空数据库的所有记录
        for hipaa in hipaa_list:
            ins_log.read_log('info', 'prowler信息：{}'.format(hipaa))
            profile = hipaa[0]
            account_id = hipaa[1]
            region = hipaa[2]
            check_id = float(hipaa[3])
            result = hipaa[4]
            group = hipaa[5]
            level = hipaa[6]
            check_title = hipaa[7]
            check_output = hipaa[8]
            new_data = HipaaData(
                profile=profile, result=result, level=level, region=region, account_id=account_id,
                group=group, check_id=check_id, check_title=check_title, check_output=check_output
            )
            session.add(new_data)
        session.commit()
        ins_log.read_log('info', 'prowler写入数据库共{}条'.format(len(hipaa_list)))


if __name__ == '__main__':
    pass