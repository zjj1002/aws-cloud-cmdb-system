from libs.aws.session import get_aws_session
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.recode_instances_id import model_to_dict, RecordInstanceId
from models.tag_list import TagList
from settings import settings
from datetime import datetime
from croniter import croniter


def get_downtime_value():
    """获取downtime标签的value"""
    with DBContext('r') as session:
        try:
            tag_info = session.query(TagList).filter(TagList.key == 'downtime').first()
            if tag_info:
                data = model_to_dict(tag_info)
                tag_value = data['value']
        except Exception as e:
            ins_log.read_log('info', e)
    return tag_value


def get_uptime_value():
    """获取uptime标签的value"""
    with DBContext('r') as session:
        try:
            tag_info = session.query(TagList).filter(TagList.key == 'uptime').first()
            if tag_info:
                data = model_to_dict(tag_info)
                tag_value = data['value']
        except Exception as e:
            ins_log.read_log('info', e)
    return tag_value


def get_downtime():
    value = get_downtime_value()
    data = value.split(' ')
    if data[0] == "0":
        hours = str(int(data[1]) - 1)
        s = "59"
        t = f'{hours}:{s}'
    else:
        s = str(int(data[0]) - 1)
        t = f'{data[1]}:{s}'

    if data[0] == "59":
        hours = str(int(data[1]) + 1)
        s = "0"
        t1 = f'{hours}:{s}'
    else:
        s = str(int(data[0]) + 1)
        t1 = f'{data[1]}:{s}'
    return t, t1


def get_uptime():
    value = get_uptime_value()
    data = value.split(' ')
    if data[0] == "0":
        hours = str(int(data[1]) - 1)
        s = "59"
        t = f'{hours}:{s}'
    else:
        s = str(int(data[0]) - 1)
        t = f'{data[1]}:{s}'

    if data[0] == "59":
        hours = str(int(data[1]) + 1)
        s = "0"
        t1 = f'{hours}:{s}'
    else:
        s = str(int(data[0]) + 1)
        t1 = f'{data[1]}:{s}'
    return t, t1


def stop_services():
    """定时任务：关机服务,目前只针对ec2服务进行关机"""
    t, t1 = get_downtime()
    value = get_downtime_value()
    times = datetime.now()
    down_time_start = datetime.strptime(str(datetime.now().date()) + t, '%Y-%m-%d%H:%M')
    down_time_end = datetime.strptime(str(datetime.now().date()) + t1, '%Y-%m-%d%H:%M')
    if down_time_start < croniter(value, times).get_next(datetime) < down_time_end:
        ins_log.read_log('info', "开始关机")
        s = get_aws_session(**settings.get("aws_key"))
        client = s.client("ec2")
        list_instances = set()
        data = client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:' + 'downtime',
                    'Values': ['*']
                },
            ], )
        for i in data['Reservations']:
            instance_id = i["Instances"][0]["InstanceId"]
            list_instances.add(instance_id)
        try:
            with DBContext('w') as session:
                for instances_id in list_instances:
                    new_instances = RecordInstanceId(instances_id=instances_id)
                    session.add(new_instances)
                session.commit()
        except Exception as e:
            ins_log.read_log('error', e)
        # 关机方法
        client.stop_instances(InstanceIds=list(list_instances))


def start_service():
    """定时任务：开机服务,目前只针对ec2服务进行开机"""
    t, t1 = get_uptime()
    print(t, t1)
    times = datetime.now()
    value = get_uptime_value()
    print(value)
    up_time_start = datetime.strptime(str(datetime.now().date()) + t, '%Y-%m-%d%H:%M')
    up_time_end = datetime.strptime(str(datetime.now().date()) + t1, '%Y-%m-%d%H:%M')
    if up_time_start < croniter(value, times).get_next(datetime) < up_time_end:
        ins_log.read_log('info', "开始开机")
        s = get_aws_session(**settings.get("aws_key"))
        client = s.client("ec2")
        with DBContext('w') as session:
            instance_info = session.query(RecordInstanceId).all()
        list_instances = []
        try:
            for instance in instance_info:
                data = model_to_dict(instance)
                instance_id = data["instances_id"]
                list_instances.append(instance_id)
                client.start_instances(InstanceIds=list_instances)  # 开机方法
        except Exception as e:
            ins_log.read_log('error', e)
        session.query(RecordInstanceId).delete(synchronize_session=False)  # 清空数据库的所有记录
        session.commit()


if __name__ == '__main__':
    pass