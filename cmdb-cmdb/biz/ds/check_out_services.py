from copy import deepcopy
from itertools import chain
from libs.aws.session import get_aws_session
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.tag_list import ResultList
from settings import settings
from models.tag_list import ServicesTagMiddle, TagList, model_to_dict, ServicesList


def get_tags():
    result = []
    s = get_aws_session(**settings.get("aws_key"))
    clients = s.client("resourcegroupstaggingapi")
    try:
        paginator = clients.get_paginator('get_resources')
        tag_mapping = chain.from_iterable(page['ResourceTagMappingList'] for page in paginator.paginate())
        for resource in tag_mapping:
            tags_collection = {}
            tags_collection.clear()
            tags_collection['tag_aws_service'] = resource['ResourceARN'].split(':')[2]
            tags_collection['tag_description'] = resource['ResourceARN']
            # tags_collection['tag_description'] = ":".join(tags_collection['tag_description'])  ###字符串格式入库
            for pairs in resource['Tags']:
                tags_dict = deepcopy(tags_collection)
                tags_dict['tag_name'] = pairs['Key']
                tags_dict['tag_value'] = pairs['Value']
                result.append(tags_dict)
        return result
    except Exception as e:
        ins_log.read_log('error', e)
        return False


def check_tag_services():
    """定时任务：检查检测aws服务的标签是否合规，并将结果入库"""
    tag_list = get_tags()
    tag_key_list = []
    with DBContext('r') as session:
        tag_info = session.query(TagList).all()
        for tag in tag_info:
            data = model_to_dict(tag)
            tag_key_list.append(data["key"])

    # 获取标签所对应的服务名称
    try:
        with DBContext('w') as session:
            session.query(ResultList).delete(synchronize_session=False)  # 清空数据库的所有记录
            for tag_key in tag_key_list:
                tag_info = session.query(TagList).filter(TagList.key == tag_key).first()
                tag_id = model_to_dict(tag_info)['id']
                if model_to_dict(tag_info)['value'] is not None:
                    value_list = model_to_dict(tag_info)['value'].split(',')
                else:
                    value_list = None
                data_info = session.query(ServicesTagMiddle).filter(ServicesTagMiddle.tag_id == tag_id).all()

                if data_info is not None:
                    services_list = []
                    for data in data_info:
                        services_id = model_to_dict(data)['services_id']
                        services_info = session.query(ServicesList).filter(ServicesList.id == services_id).first()
                        services_name = model_to_dict(services_info)['services_name']
                        services_list.append(services_name)

                    for services_name in services_list:
                        for tag in tag_list:
                            is_valid = 1
                            if tag["tag_aws_service"] == services_name and tag["tag_name"] == tag_key:
                                if value_list is not None and tag["tag_value"] not in value_list:
                                    is_valid = 0
                                new_data = ResultList(services_name=services_name, services_resource_id=tag["tag_description"],
                                                      key=tag["tag_name"], value=tag["tag_value"], is_valid=is_valid)
                                session.add(new_data)
                                session.commit()

    except Exception as e:
        ins_log.read_log('error', e)


if __name__ == '__main__':
    pass