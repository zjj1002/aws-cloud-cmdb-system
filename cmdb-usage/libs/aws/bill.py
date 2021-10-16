#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-10-10
# @Author : liuchuanhao
# @Site : 
# @File : bill.py
# @Software: PyCharm

from libs.db_context import DBContext
from models.db import AwsProjectBudgetControl
from models.db import AwsProjectBillReport, model_to_dict


# 更新预算控制表单
def get_project_budget():
    with DBContext('w') as session:
        data = session.query(AwsProjectBillReport).all()
    bill_list = [model_to_dict(e) for e in data]
    for i in bill_list:
        data_old = session.query(AwsProjectBudgetControl) \
            .filter(AwsProjectBudgetControl.userproject == i.get("userproject"),
                    AwsProjectBudgetControl.bill_date == i.get("bill_date")).first()
        if data_old:
            session.query(AwsProjectBudgetControl) \
                .filter(AwsProjectBudgetControl.userproject == i.get("userproject"),
                        AwsProjectBudgetControl.bill_date == i.get("bill_date")) \
                .update(
                {
                    AwsProjectBudgetControl.aws_total_cost: i.get("aws_total_cost"),
                }
            )

        else:
            new_data = AwsProjectBudgetControl(userproject=i.get("userproject"),
                                               aws_total_cost=i.get("aws_total_cost"),
                                               # aws_budget_cost=i.get("aws_total_cost"),
                                               aws_percentage=i.get("aws_total_cost")/i.get("aws_total_cost") if i.get("aws_total_cost") else 0,
                                               # aws_alert_percentage=1.2,
                                               bill_date=i.get("bill_date"))
            session.add(new_data)
    session.commit()


def update_project_budget():
    with DBContext('w') as session:
        data = session.query(AwsProjectBudgetControl).all()
    bill_list = [model_to_dict(e) for e in data]
    for i in bill_list:
        session.query(AwsProjectBudgetControl) \
            .filter(AwsProjectBudgetControl.userproject == i.get("userproject"),
                    AwsProjectBudgetControl.bill_date == i.get("bill_date")) \
            .update(
            {
                AwsProjectBudgetControl.aws_percentage: i.get("aws_total_cost") / i.get("aws_budget_cost") if i.get("aws_budget_cost") else 0,
            }
        )
    session.commit()


if __name__ == '__main__':
    get_project_budget()
    update_project_budget()
