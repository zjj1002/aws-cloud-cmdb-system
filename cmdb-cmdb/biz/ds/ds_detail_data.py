import json

from libs.db_context import DBContext
from models.all_assets import DetailTable, model_to_dict, AllAssets


def get_detail_data():
    """定时任务，拆分树状图数据入库"""
    with DBContext('w') as session:
        session.query(DetailTable).delete(synchronize_session=False)  # 清空数据库的所有记录
        all_data_info = session.query(AllAssets).all()
        temp_list = []
        for data_info in all_data_info:
            dict_data = model_to_dict(data_info)
            service_name = dict_data["service_name"]
            regions = dict_data["regions"]
            operation = dict_data["operation"]
            temp_operation_data = json.loads(dict_data["operation_data"])
            try:
                operation_data = temp_operation_data[list(temp_operation_data.keys())[0]]
            except Exception as e:
                print(e)
            try:
                if type(operation_data) == list:
                    length = len(operation_data)
                    step = 500
                    for i in range(0, length, step):
                        for index, data in enumerate(operation_data[i:i+step]):
                            print(index)
                            str_data = service_name + '-' +regions + '-' + operation + str(index+1)
                            temp_list.append(str_data)
                            new_data = DetailTable(service_name=service_name, regions=regions, operation=operation,
                                                   temp_data=str_data, detail_data=data)
                            session.add(new_data)
                        session.commit()
                elif type(operation_data) == dict:
                    keys = list(operation_data.keys())[0]
                    for index, data in enumerate(operation_data[keys]):
                        print(index)
                        str_data = service_name + '-' + regions + '-' + operation + str(index + 1)
                        temp_list.append(str_data)
                        new_data = DetailTable(service_name=service_name, regions=regions, operation=operation,
                                               temp_data=str_data, detail_data=data)
                        session.add(new_data)
                    session.commit()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    pass