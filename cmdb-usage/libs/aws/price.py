#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-07-15 23:19
# @Author : jianxlin
# @Site : 
# @File : price.py
# @Software: PyCharm

import json
import os
import logging

import awscnpricing
import pandas as pd

from libs.config import config
from libs.decorate import show_running_time

os.environ['AWSPRICING_USE_CACHE'] = "1"
os.environ['AWSPRICING_CACHE_PATH'] = "/tmp/awscnpricing"
os.environ['AWSPRICING_CACHE_MINUTES'] = str(30 * 24 * 60)


class OnDemandInfo(object):
    def __init__(self):
        self._d = {
            "region": None,
            "platform": None,
            "instance_type": None,
            "price": None,
        }

    def __getattr__(self, item):
        assert item in self._d.keys()
        return self.item

    def __setattr__(self, key, value):
        assert key in self._d.keys()
        self.key = value


class OnDemandPrice(object):
    _offer_code = None
    _product_family = None

    def __init__(self, region='cn-northwest-1', version="current", *args, **kwargs):
        self._region = region
        self._price_offer = awscnpricing.offer(service_name=self.offer_code, version=version)
        self._offers_version = awscnpricing._fetch_available_versions(offers=awscnpricing._get_offers(),
                                                                      offer_name=self.offer_code)
        self._current_offer = None
        self._on_demand_price = None
        self.__read_cache()
        self.__init_price()
        self._append_custom_price()

    @show_running_time
    def __read_cache(self):
        _file_path = os.getenv('AWSPRICING_CACHE_PATH')
        _file_name = 'offer_{}_current'.format(self.offer_code)
        _cache_file = os.path.join(_file_path, _file_name)

        if os.path.exists(_cache_file):
            with open(_cache_file, 'r') as load_f:
                self.current_offer = json.load(load_f)
        # else:
        #     import requests
        #     offers = requests.get(
        #         'https://pricing.cn-north-1.amazonaws.com.cn/offers/v1.0/cn/index.json'
        #     )
        #     ec2_offer_path = offers.json()['offers']['AmazonEC2']['currentVersionUrl']
        #     logging.info('https://pricing.cn-north-1.amazonaws.com.cn%s' % ec2_offer_path)
        #     self.current_offer = requests.get(
        #         # 'https://pricing.cn-north-1.amazonaws.com.cn/offers/v1.0/cn/AmazonEC2/20190313005750/index.json'
        #         'https://pricing.cn-north-1.amazonaws.com.cn%s' % ec2_offer_path
        #     ).json()

    def _append_custom_price(self):
        """
            添加自定义价格。
        :return:
        """
        self.on_demand_price = self.on_demand_price.append(config.get_on_demand_price(self.offer_code),
                                                           ignore_index=True)

    @property
    def region(self):
        return self._region

    @property
    def on_demand_price(self):
        return self._on_demand_price

    @on_demand_price.setter
    def on_demand_price(self, value):
        self._on_demand_price = value

    @property
    def offer_code(self):
        return self._offer_code

    @property
    def price_offer(self):
        return self._price_offer

    @property
    def current_offer(self):
        return self._current_offer

    @property
    def offers_version(self):
        return self._offers_version

    @current_offer.setter
    def current_offer(self, value):
        self._current_offer = value

    def _get_on_demand_price(self, data):
        region = None
        platform = None
        instance_type = None
        operation = None
        price = 0

        return region, platform, operation, instance_type, price

    def __init_price(self):

        on_demand_price = []
        i_type = []
        location = []
        platforms = []
        operations = []

        for sku, data in self.current_offer['products'].items():
            if data['productFamily'] != self._product_family:
                continue

            if 'instanceType' not in data['attributes'].keys():
                continue
            region, platform, operation, instance_type, price = self._get_on_demand_price(data=data)
            if region != self.region:
                continue

            on_demand_price.append(price)
            i_type.append(instance_type)
            location.append(region)
            platforms.append(platform)
            operations.append(operation)
        df = pd.DataFrame({
            'UsageType': i_type,
            "Platform": platforms,
            "Operation": operations,
            "Region": location,
            "OnDemandPrice": on_demand_price,
        })
        df[["OnDemandPrice"]] = df[["OnDemandPrice"]].astype('float')
        df.drop_duplicates(
            subset=['UsageType', 'Platform', 'Operation', 'Region', 'OnDemandPrice'],
            keep='first',
            inplace=True)
        # df = df[(df.OnDemandPrice > 0)]
        # df = df.reset_index(drop=True)
        self.on_demand_price = df


class Ec2OnDemandPrice(OnDemandPrice):
    _offer_code = 'AmazonEC2'
    _product_family = 'Compute Instance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_on_demand_price(self, data):
        price = 0
        instance_type = data['attributes']['instanceType']
        platform = data['attributes']['operatingSystem']
        site = data['attributes']['location']
        usage_type = data['attributes']['usagetype']
        operation = data['attributes']['operation']

        region = ""
        if site == "China (Beijing)":
            region = "cn-north-1"
        if site == "China (Ningxia)":
            region = "cn-northwest-1"
        # if data['attributes']['tenancy'] != 'Shared':
        #     return region, platform, operation, usage_type, price
        try:
            price = self.price_offer.ondemand_hourly(
                instance_type,
                operating_system=platform,
                tenancy=data['attributes']['tenancy'],
                preinstalled_software=data['attributes']['preInstalledSw'],
                license_model=data['attributes']['licenseModel'],
                region=region,
                capacity_status=data['attributes']['capacitystatus']
            )
        except Exception as e:
            pass
        return region, platform, operation, usage_type, price


class RdsOnDemandPrice(OnDemandPrice):
    _offer_code = 'AmazonRDS'
    _product_family = 'Database Instance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_on_demand_price(self, data):
        price = 0
        usage_type = data['attributes']['usagetype']
        platform = data['attributes']['databaseEngine']
        site = data['attributes']['location']
        operation = data['attributes']['operation']
        database_edition = data['attributes'].get('databaseEdition', None)
        region = ""
        if site == "China (Beijing)":
            region = "cn-north-1"
        if site == "China (Ningxia)":
            region = "cn-northwest-1"
        try:
            price = self.price_offer.ondemand_hourly(
                data['attributes']['instanceType'],
                database_engine=platform,
                license_model=data['attributes']['licenseModel'],
                deployment_option=data['attributes']['deploymentOption'],
                database_edition=database_edition,
                region=region
            )
        except Exception as e:
            # logging.info(e)
            pass
        return region, platform, operation, usage_type, price


if __name__ == '__main__':
    # p = Ec2OnDemandPrice()
    p = RdsOnDemandPrice()
    o = p.on_demand_price

    logging.info(p.offers_version.keys())
    # p = RdsOnDemandPrice()
    # import requests
    # requests.get('https://pricing.cn-north-1.amazonaws.com.cn/offers/v1.0/cn/AmazonEC2/20190313005750/index.json').json()

    # o.drop_duplicates(subset=['UsageType'], keep='first', inplace=True)
    #
    # pd.set_option('display.max_rows', 10000)  # 具体的行数或列数可自行设置
    # pd.set_option('display.max_columns', 100)
    # logging.info(o[["UsageType", 'Operation', 'OnDemandPrice']])
    logging.info(o[(o.UsageType == "CNW1-InstanceUsage:db.m5.2xl")][["UsageType", 'Operation', 'OnDemandPrice']])
    # logging.info(o[(o.Operation == "CreateDBInstance:0005")][["UsageType", 'Operation', 'OnDemandPrice']])
