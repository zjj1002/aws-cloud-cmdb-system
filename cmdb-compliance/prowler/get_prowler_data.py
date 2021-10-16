import os
import sys

from libs.catch_execption import catch_exceptions_util


def get_prowler_data():
    try:
        for i in os.listdir('/var/www/cmdb-compliance/prowler/output'):
            os.remove(f'/var/www/cmdb-compliance/prowler/output/{i}')
        os.system("chmod 777 /var/www/cmdb-compliance/prowler/prowler")
        print('info: 开始获取prowler数据')
        os.system("aws configure set region cn-northwest-1 && /var/www/cmdb-compliance/prowler/prowler -M csv")
        print('info: prowler数据获取完毕')
    except Exception as e:
        print("异常:{}".format(e))


def worker(ex_code):
    status = 0
    try:
        pid = os.fork()
        if pid == 0:
            get_prowler_data()
            sys.exit(ex_code)
        else:
            _, code = os.waitpid(pid, status)
            real_code = code >> 8
            return real_code
    except OSError as e:
        print(e)


@catch_exceptions_util
def run_get_prowler_data():
    ex_code = 99
    result = worker(ex_code)
    if result != ex_code:
        for _ in range(3):  # 重试3次
            worker(ex_code)


if __name__ == '__main__':
    run_get_prowler_data()

