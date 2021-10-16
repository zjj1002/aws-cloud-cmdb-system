import json

from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.all_assets import model_to_dict, DetailTable, AllAssets


class AllAssetsHandler(BaseHandler):

    def get(self, *args, **kwargs):
        """获取服务的服务名、区域、方法"""
        service_region_op_list = []
        with DBContext('r') as session:
            assets_info = session.query(AllAssets).all()

            service_name_list = set()  # 所有服务的列表
            for data in assets_info:
                data_dict = model_to_dict(data)
                service_name_list.add(data_dict['service_name'])

            # regions_list = ["cn-north-1", "cn-northwest-1"]  # 区域
            regions_list = set()
            for service_name in service_name_list:
                service_info = session.query(AllAssets).filter_by(service_name=service_name).all()
                for data in service_info:
                    data_dict1 = model_to_dict(data)
                    regions_list.add(data_dict1['regions'])

                op_list = []
                temp = []
                for region in regions_list:
                    op_info = session.query(AllAssets).filter_by(service_name=service_name, regions=region).all()
                    if op_info:
                        for data in op_info:
                            data_dict2 = model_to_dict(data)
                            op_list.append(data_dict2['operation'])
                        region_op_dict = [region, op_list[:]]
                        temp.append(region_op_dict)
                        op_list.clear()
                service_region_op_list.append([service_name, temp[:]])
                temp.clear()
                regions_list.clear()
        return self.write(dict(code=0, msg='获取成功', total=len(service_region_op_list), data=service_region_op_list))


class ServiceOpDataHandler(BaseHandler):

    def get(self, *args, **kwargs):
        """获取服务的操作方法"""
        service_op_data_list = []
        service_name = self.get_argument('service_name', default=None, strip=True)
        regions = self.get_argument('regions', default=None, strip=True)
        operation = self.get_argument('operation', default=None, strip=True)
        with DBContext('r') as session:
            op_data = session.query(AllAssets).filter_by(
                service_name=service_name, regions=regions, operation=operation
            ).first()
        try:
            temp_list = []
            service_op_data = model_to_dict(op_data)
            operation_data = service_op_data["operation_data"]
            loads_operation_data = json.loads(operation_data)
            operation_data_list = loads_operation_data[list(loads_operation_data.keys())[0]]
            for index, data in enumerate(operation_data_list):
                str_data = service_name + '-' + regions + '-' + operation + str(index+1)
                temp_list.append(str_data)
            service_op_data["operation_data"] = temp_list
            service_op_data_list.append(service_op_data)
        except Exception as e:
            print(e)
        return self.write(dict(code=0, msg='获取成功', total=len(service_op_data_list), data=service_op_data_list))


class DetailDataHandler(BaseHandler):

    def get(self, *args, **kwargs):
        """获取详细的数据"""
        temp_data = self.get_argument('temp_data', default=None, strip=True)
        data_list = []
        with DBContext('r') as session:
            data_info = session.query(DetailTable).filter(DetailTable.temp_data == temp_data).first()
            if data_info:
                data = model_to_dict(data_info)
                data_list.append(data)
        return self.write(dict(code=0, msg='获取成功', total=len(data_list), data=data_list))


all_assets_host_urls = [
    (r"/v1/cmdb/get_service_op/", AllAssetsHandler),
    (r"/v1/cmdb/get_service_op_data/", ServiceOpDataHandler),
    (r"/v1/cmdb/get_detail_data/", DetailDataHandler),
]

if __name__ == '__main__':
    pass
