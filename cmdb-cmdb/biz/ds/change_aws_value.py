from libs.aws.session import get_aws_session
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.tag_list import ChangeResultList, model_to_dict
from settings import settings


def change_aws_value():
    """定时任务：修改aws服务上的标签value"""
    with DBContext('w') as session:
        change_value_list = []
        data_info = session.query(ChangeResultList).all()
        if data_info:
            for data in data_info:
                dict_data = model_to_dict(data)
                change_value_list.append(dict_data)

        s = get_aws_session(**settings.get("aws_key"))
        clients = s.client("resourcegroupstaggingapi")
        try:
            for tag_value in change_value_list:
                services_resource_id = tag_value["services_resource_id"]
                key = tag_value["key"]
                value = tag_value["value"]
                # 去除资源标签
                clients.untag_resources(
                    ResourceARNList=[
                        services_resource_id,
                    ],
                    TagKeys=[
                        key,
                    ]
                )
                # 添加资源标签
                clients.tag_resources(
                    ResourceARNList=[
                        services_resource_id,
                    ],
                    Tags={key: value}
                )
                session.query(ChangeResultList).filter_by(
                    services_resource_id=services_resource_id, key=key
                ).delete()
                session.commit()
        except Exception as e:
            ins_log.read_log('error', e)


if __name__ == '__main__':
    pass












