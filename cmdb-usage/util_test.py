import pandas as pd
from pandasql import sqldf

bill = pd.read_csv(
    filepath_or_buffer="/Users/jianxlin/Documents/PythonWorkspace/jnc-cmdb/cmdb-usage/tmp/309544246384-aws-billing-detailed-line-items-with-resources-and-tags-ACTS-Ningxia-2020-08.csv.zip")
bill.columns = bill.columns.str.replace(':', '')
bill.rename(columns={"UnBlendedCost": "Cost", "UnBlendedRate": "Rate"}, inplace=True)
bill.fillna("NULL", inplace=True)
usage_start_date = "2020-08-01 00:00:00"
usage_end_date = "2020-09-01 00:00:00"

sql = """
    select sum(Cost) as Rounding
    from bill 
    where RecordType = 'Rounding'
"""
rounding = sqldf(sql, {"bill": bill})
rounding["userproject"] = "aiops"
print(rounding)



def run(_sql=None, _bill=None):
    b = sqldf(_sql, {"bill": _bill})
    pd.set_option('display.max_rows', 10000)  # 具体的行数或列数可自行设置
    pd.set_option('display.max_columns', 100)
    print(b)
    return b


sql = """
    select *
    from bill
    where SubscriptionId = "NULL"

    """ % locals()

print('SubscriptionId = "NULL" ')

run(sql, bill)

"""
       RateId SubscriptionId PricingPlanId UsageType Operation AvailabilityZone ReservedInstance                                    ItemDescription       UsageStartDate         UsageEndDate UsageQuantity BlendedRate        BlendedCost  Rate               Cost ResourceId userName userkubernetes.io/service-name userproject
    1494763 1,320,575,235.0000000000    309544246384 309,544,246,384.0000000000        LineItem        0        NULL 0.0000000000           NULL          NULL      NULL      NULL             NULL                N                                          税金 VAT 类型  2020-08-01 00:00:00  2020-08-31 23:59:59          NULL        NULL  10,374.7400000000  NULL  10,374.7400000000       NULL     NULL   NULL        NULL
    1494764 1,320,575,235.0000000000    309544246384 687,267,341,391.0000000000        LineItem        0        NULL 0.0000000000           NULL          NULL      NULL      NULL             NULL                N                                          税金 VAT 类型  2020-08-01 00:00:00  2020-08-31 23:59:59          NULL        NULL      43.3400000000  NULL      43.3400000000       NULL     NULL   NULL        NULL
    1494765 1,320,575,235.0000000000    309544246384                       NULL        Rounding     NULL        NULL         NULL           NULL          NULL      NULL      NULL             NULL             NULL                       由于整合账单和小时行项目计算流程，该行项目包含舍入错误。                 NULL                 NULL          NULL        NULL       0.0025652967  NULL      -2.5094690054       NULL     NULL                           NULL        NULL
    1494766 1,320,575,235.0000000000    309544246384                       NULL    InvoiceTotal     NULL        NULL         NULL           NULL          NULL      NULL      NULL             NULL             NULL                                  发票 1320575235 的总额   NULL                 NULL          NULL        NULL 184,053.6000000000  NULL 184,053.6000000000       NULL     NULL    NULL        NULL
    1494767                     NULL    309544246384 309,544,246,384.0000000000    AccountTotal     NULL        NULL         NULL           NULL          NULL      NULL      NULL             NULL             NULL                              关联账户# 309544246384 总额    NULL                 NULL          NULL        NULL 183,287.8288184949  NULL 183,290.2815696986       NULL     NULL     NULL        NULL
    1494768                     NULL    309544246384 687,267,341,391.0000000000    AccountTotal     NULL        NULL         NULL           NULL          NULL      NULL      NULL             NULL             NULL                              关联账户# 687267341391 总额    NULL                 NULL          NULL        NULL     765.7686162084  NULL     765.8278993068       NULL     NULL     NULL        NULL
    1494769                     NULL    309544246384                       NULL  StatementTotal     NULL        NULL         NULL           NULL          NULL      NULL      NULL             NULL             NULL  2020-08-01 00:00:00 - 2020-08-31 23:59:59 期间内的...  NULL                 NULL          NULL        NULL 184,053.6000000000  NULL 184,053.6000000000       NULL     NULL   NULL        NULL
"""