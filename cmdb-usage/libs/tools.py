#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-05-17 08:28
# @Author : jianxlin
# @Site : 
# @File : tools.py
# @Software: PyCharm

import logging


def human2byte(number=None):
    """
        换算到Bite
    :param number:
    :return:
    """
    num = ""
    unit = ""
    units = {
        "B": 1,
        "K": 1024,
        "M": 1024 * 1024,
        "G": 1024 * 1024 * 1024,
        "T": 1024 * 1024 * 1024 * 1024,
    }

    number = number.strip()

    for b in number:
        if b.isalpha():
            unit = "".join([unit, b])
        else:
            num = "".join([num, b])
    unit = "B" if unit == "" else unit
    assert number.startswith(num)
    assert unit in units.keys()
    return float(num) * units[unit]


def instance_type_format(instance_type=None, usage_type=None):
    """
        转化实例类型到xlarge。
    :param usage_type:
    :param instance_type:
    :return:
    """
    n = {
        "large": 0.5,
        "medium": 0.25,
        "small": 0.125,
        "micro": 0.0625,
        "nano": 0.03125
    }
    num = 0
    instance_type = instance_type or usage_type.split(":")[1]
    family, name = instance_type.split(".")
    if name.endswith("xlarge"):
        _ = name.replace("xlarge", "")
        num = 1 if _ == "" else int(_)
    else:
        num = n.get(name)
    assert num is not None
    return num


def get_usage_type_from_item_description(item_description=None):
    """
        解析字符串'CNY 0.891 hourly fee per Linux/UNIX (Amazon VPC), m4.2xlarge instance; UsageType: CNN1-BoxUsage:m4.large'
        中 "CNN1-BoxUsage:m4.large"
    :param item_description:
    :return:
    """
    return item_description.split(" ")[-1]


def is_heavy_usage_type(usage_type):
    """
        CNN1-HeavyUsage:m4.2xlarge
    :param usage_type:
    :return:
    """
    return usage_type.split(":")[0].endswith("HeavyUsage")


def is_heavy_usage_item_scription(item_description):
    """
        CNN1-HeavyUsage:m4.2xlarge
    :param item_description:
    :return:
    """
    return len(item_description.split(";")) == 2


def get_operation_name(operation):
    return {
        "RunInstances": "Linux",
        "RunInstances:0002": "Windows"
    }.get(operation, "Unknown")


def get_instance_series(usage_type=None, instance_type=None):
    """
        获取实例系列信息
    :param usage_type:
    :param instance_type:
    :return:
    """
    instance_type = instance_type or get_instance_type_from_usage_type(usage_type=usage_type)
    return instance_type.split(".")[0]


def get_instance_type_from_usage_type(usage_type):
    return usage_type.split(":")[-1]


def get_lower_case_name(text):
    lst = []
    for index, char in enumerate(text):
        if char == ' ':
            continue
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


if __name__ == '__main__':
    print(get_lower_case_name("Abc Def"))
