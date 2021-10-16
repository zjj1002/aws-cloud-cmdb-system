[TOC]

# 文档说明
  本接口文档给予《ResfulAPI接口开放规范》编写。

# 功能列表

##  usage接口文档
### 1. 根据服务类型查询资源的月度总账单
#### 描述
```
    
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/usage/bill/server/monthly/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | service_name | 服务名称 |  Y  |  String |  64  | 无  | 查询服务的名字 |
| 2 | month | 查询月份 |  N  | datetime |  64  | 当前月 | 查询账单的日期 |
| 3| pageNum | 当前页码 |  N  |  Int |  2  |  1  | 当前页码    |
|4| pageSize | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | count | 返回数据总数 | 返回数据总数 |
|  4  | data | 返回数据 |  返回数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | resource_id | 资源id | 资源id |
|  2  | service_name | 服务名字 | 服务名字               |
|  3  | userproject | 项目名 | 项目名                |
|  4  | total_cost | 账单花费 | 账单花费          |
|  5  | bill_date | 账单日期 | 账单日期 |



#### 请求URL实例

``` bash
  $ curl http://127.0.0.1:8000/v1/usage/bill/server/monthly/?service_name=EC2&month=2020-05
  
  https://cmdb.jncapp.com/api/usage/v1/usage/bill/server/monthly/?service_name=EC2&month=2020-05
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "获取成功",
    "count": 11,
    "data": [
        {
            "id": 404,
            "resource_id": "i-00151d56237f0476e",
            "service_name": "EC2",
            "userproject": "Weaver-OA",
            "total_cost": "43.69576",
            "bill_date": "2020-05-06 00:00:00"
        },
}
```



### 2. 根据月份查询所有BU总账单
#### 描述
```

```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/usage/bill/bu/monthly/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | bill_date | 账单日期   |  Y  | str |  64  | 无  | 账单日期 |
| 2 | pageNum | 当前页码 |  N  |  Int |  2  |   1  | 当前页码   |
|3| pageSize | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | count | 返回数据总数 | 返回数据总数 |
|  4  | data | 返回数据 |  返回数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | userproject | 项目名 |   |
|  2  | ec2_cost | ec2账单 |      |
|  3  | ebs_cost |     ebs账单     |  |
|  4  | snapshot_cost | snapshot账单 |  |
|  5  | s3_cost |     s3账单    |  |
|  6  | rds_cost | rds账单 |      |
|  7  | elasticache_cost | ElastiCache账单 |  |
|  8  | credit |   Credit账单  |  |
|  9  | support_cost | Support费用 |      |
|  10  | t_a_x |    税费     |      |
|  11  | aws_total_cost |   总费用    |  |
|  12  | bill_date |  账单日期   |      |


#### 请求URL实例

``` bash
  $ curl -X get http://127.0.0.1:8000/v1/usage/bill/bu/monthly/?bill_date=2020-06
  https://cmdb.jncapp.com/api/usage/v1/usage/bill/bu/monthly/?bill_date=2020-05
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "获取成功",
    "count": 1,
    "data": [
        {
            "id": 1,
            "userproject": "qwe",
            "ec2_cost": "0.00001",
            "dep_ebs_cost": "0.00001",
            "dep_snap_cost": "0.00001",
            "bu_s3_cost": "0.00001",
            "r_d_s_cost": "0.00001",
            "dep_elasti_cache_cost": "0.00001",
            "credit": "0.00001",
            "support_cost": "0.00001",
            "t_a_x": "0.00001",
            "aws_total_cost": "0.00001",
            "bill_date": "2020-06-01 00:00:00"
        }
    ]
}
```


### 3. 根据资源ID和服务类型查询月份内资源每日总账单
#### 描述
```

```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/usage/bill/resource/dayly/ |

#### 请求参数                                                                                          （修改日期：2020/7/5 修改内容：请求参数增加service_name）

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | resource_id | 资源id |  Y  |  String |  64  | 无  |  |
| 2 | month | 查询月份 |  N  | datetime |    | 本月  |    |
| 3 | service_name | 服务类型 |  Y  | string |    | 无 |    |


#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | count | 返回数据总数 | 返回具体总数 |
|  4  | data | 返回数据 |  返回数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | resource_id | 资源id | 资源id |
|  2  | service_name | 服务名字 | 服务名字               |
|  3  | userproject | 项目名 | 项目名                |
|  4  | total_cost | 账单花费 | 账单花费          |
|  5  | bill_date | 账单日期 | 账单日期 |


#### 请求URL实例

``` bash
  $ curl http://127.0.0.1:8000/v1/usage/bill/resource/dayly/?month=2020-05&resource_id=i-0074743285099039f
   https://cmdb.jncapp.com/api/usage/v1/usage/bill/resource/dayly/?month=2020-05&resource_id=i-0848198e9fe116c27
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "获取成功",
    "count": 2,
    "data": [
        {
            "id": 406,
            "resource_id": "i-0074743285099039f",
            "service_name": "EC2",
            "userproject": "sf-order",
            "total_cost": "17.91714",
            "bill_date": "2020-05-06 00:00:00"
        },
        {
            "id": 807,
            "resource_id": "i-0074743285099039f",
            "service_name": "EC2",
            "userproject": "sf-order",
            "total_cost": "17.61575",
            "bill_date": "2020-05-07 00:00:00"
        }
    ]
}
```


### 4. 根据BU查询其各个服务的每日总账单
#### 描述
```

```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/usage/bill/buserver/dayly/ |

#### 请求参数   （7/5请求数据增加月份，返回数据为空补全为0）

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | userproject | 项目名 |  Y  |  String |  64  | 无  |  |
| 2 | month | 月份 |  N  |  String |  64  | 当前月 |  |


#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | count | 返回数据总数 | 返回数据总数 |
|  4  | data | 返回数据 |  返回数据  |

#### data数据字段说明 data下面是键值对  key是服务名称 value是字典 字典下面是以日期为key  总账单的和为value



| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | service_name | 服务名称 |   |
|  2  | bill_date | 账单时间 |   |



#### 请求URL实例

``` bash
  $ curl http://127.0.0.1:8000/v1/usage/bill/buserver/dayly/?userproject=tpm&month=2020-05
  
  https://cmdb.jncapp.com/api/usage/v1/usage/bill/buserver/dayly/?userproject=tpm&month=2020-05
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "获取成功",
    "count": 3,
    "data": {
        	service_name1：{
                         bill_date1:cost
                         bill_date2:cost
            				}
            service_name2：{
                                 bill_date1:cost
                                 bill_date2:cost
                    		}

   			}
}

------------------------------------------------------------------
下面是返回示例


{
    "code": 0,
    "msg": "获取成功",
    "count": 3,
    "data": {
        "EC2": {
            "2020-05-06 00:00:00": 496.62881000000004,
            "2020-05-07 00:00:00": 489.12745
        },
        "ElastiCache": {
            "2020-05-06 00:00:00": 118.08,
            "2020-05-07 00:00:00": 118.08
        },
        "RDS": {
            "2020-05-06 00:00:00": 131.6248,
            "2020-05-07 00:00:00": 131.78074
        }
    }
}
```



### 5. 手动添加日期查询使用率（usage）
#### 描述
```
把查询任务存储在本地mysql中  等待被执行
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | post |
| 地址 | /v1/usage/report/day/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | date_period | 时间段 |  Y  | str |    |   无  |          |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | message | 返回消息 | 消息说明  |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |


#### 请求URL实例

``` bash
  $ curl -X post http://127.0.0.1:8000/v1/usage/report/day/ -d '{"date_period":"2020-06-06--2020-06-10"}'
   https://cmdb.jncapp.com/api/usage/v1/usage/report/day/ -d '{"date_period":"2020-06-06--2020-06-10"}'
   
   
```

#### 返回数据实例

``` json
{ 
  "code":0,
  "message": "任务添加成功，后台执行添加usage数据库",
 
}
```
### 6. 手动添加日期查询账单（bill）
#### 描述
```

```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | post |
| 地址 | http://127.0.0.1:8000/v1/usage/addbill/byday/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | date_period | 日期 |  Y  | str |  |   无  | 2020-07-04--2020-07-07 |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | message | 返回消息 | 消息说明  |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |


#### 请求URL实例

``` bash
  $ curl -X http://127.0.0.1:8000/v1/usage/addbill/byday/
  
   
   
```

#### 返回数据实例

``` json
{ 
  "code":0,
  "message": "任务添加成功，后台执行添加report数据库",
 
}
```
### 7. 手动添加预留实例使用率（一个刷新按钮ri_usageri_usage）
#### 描述
```
把手动添加日期查询使用率任务存储在本地mysql中 
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | post |
| 地址 | /v1/ri-usage/add/byday/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
|  |  |  |    |  |    |     |          |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | message | 返回消息 | 消息说明  |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |


#### 请求URL实例

``` bash
  $ curl -X post http://127.0.0.1:8000/v1/ri-usage/add/byday/ 
   https://cmdb.jncapp.com/api/usage/v1/ri-usage/add/byday/ 
   
```
#### 返回数据实例

``` json
{ 
  "code":0,
  "message": "任务添加成功，后台执行添加ri_usage数据库"
 
}
```
### 8.获取月份
#### 描述
```
获取月份
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/usage/report/months/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
|      |        |          |      |          |      |        |          |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | count | 返回总数 |   |
|  3 | data | 数据 |   |
|  4  | msg | 返回消息 | 消息说明  |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |


#### 请求URL实例

``` bash
  $ curl http://127.0.0.1:8000/v1/usage/report/months/
  
   
```
#### 返回数据实例

```
{
    "code": 0,
    "msg": "获取成功",
    "count": 2,
    "data": [
        "2020-06-01 00:00:00",
        "2020-07-01 00:00:00"
    ]
}
```
### 9.获取账单
#### 描述
```
获取账单
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | https://cmdb.jncapp.com:8443/api/usage/v1/usage/report/?pageNum=1&pageSize=15&month=2020-05 |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | month | 月份 | N | str | 7 | 当前月2020-07 |          |
| 2 | pageNum | 页码 | N | str |      | 1 |          |
| 3 | pageSize | 一页条数 | N | str |      | 10 |          |
| 4 | key | 模糊查询关键词 | N | str |      | 10 |          |
|      |          |                |      |          |      |               |          |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | count | 返回消息数 |   |
|  4  | pageTotal | 总页数 |   |
|  5  | data | 数据 |   |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |
|  1| ec2_id | 主机id | - |
|  2| host_name | 主机名 | - |
|  3| project_name | 所属项目 | - |
| 4| cpu_avg_usage | cpu使用率 | - |
|  5| mem_avg_usage | 内存使用率 | - |
|  6| disk_avg_usage | 磁盘使用率 | - |
|  7| curr_inst_type | 当前机型 | - |
|  8| suggest_inst_type | 建议机型 | - |
|  9| cost_gap | 预计节省费用 | - |
|  10| month | 月份 | - |


#### 请求URL实例

``` bash
  $ curl https://cmdb.jncapp.com:8443/api/usage/v1/usage/report/?pageNum=1&pageSize=15&month=2020-05
  
  
```
#### 返回数据实例

```json
{

  "code": 0,

  "msg": "获取成功",

  "count": 1,

  "pageTotal": 1,

  "data": [

​    {

​      "id": 426,

​      "ec2_id": "i-0dc802bd6b27c2843",

​      "host_name": "NFS-Server02",

​      "project_name": "tpm",

​      "cpu_avg_usage": 2,

​      "mem_avg_usage": 58,

​      "disk_avg_usage": 37,

​      "curr_inst_type": "t2.micro",

​      "suggest_inst_type": "",

​      "cost_gap": "0.00000",

​      "month": "2020-07-01 00:00:00"

​    },

  ]

}
```


### 10.获取report和资源使用率
#### 描述
```
获取账单和资源使用率
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | https://cmdb.jncapp.com:8443/api/usage/v1/usage/resource/?ec2_id=i-0dc802bd6b27c2843&month=2020-05 |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | ec2_id | 主机id | Y | str |      |        |          |
| 2    | month | 月份 | N | str | 7 | 当前月 | 2020-05 |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3 | count | 总条数 |   |
|  4  | data | 数据 |   |

#### data数据字段说明 有两个字典 ec2_info 和usage_list

ec2_info:

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1| ec2_id | 主机id | - |
|  2| host_name | 主机名 | - |
|  3| project_name | 所属项目 | - |
| 4| cpu_avg_usage | cpu使用率 | - |
|  5| mem_avg_usage | 内存使用率 | - |
|  6| disk_avg_usage | 磁盘使用率 | - |
|  7| curr_inst_type | 当前机型 | - |
|  8| suggest_inst_type | 建议机型 | - |
|  9| cost_gap | 预计节省费用 | - |
|  10| month | 月份 | - |

usage_list:
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1| ec2_id | 主机id | - |
|  2| cpu_usage | cpu使用率 | - |
|  3| mem_usage | 内存使用率 | - |
| 4| disk_usage | 磁盘使用率 | - |
|  5| date | 日期 | - |





#### 请求URL实例

``` bash
  $ curl https://cmdb.jncapp.com:8443/api/usage/v1/usage/resource/?ec2_id=i-0dc802bd6b27c2843&month=2020-05
  
  
```
#### 返回数据实例

```json
{
    "code": 0,
    "msg": "获取成功",
    "count": 2,
    "data": {
        "ec2_info": {
            "id": 426,
            "ec2_id": "i-0dc802bd6b27c2843",
            "host_name": "NFS-Server02",
            "project_name": "tpm",
            "cpu_avg_usage": 2,
            "mem_avg_usage": 58,
            "disk_avg_usage": 37,
            "curr_inst_type": "t2.micro",
            "suggest_inst_type": "",
            "cost_gap": "0.00000",
            "month": "2020-07-01 00:00:00"
        },
        "usage_list": [
            {
                "id": 2676,
                "ec2_id": "i-0dc802bd6b27c2843",
                "cpu_usage": 2,
                "mem_usage": 58,
                "disk_usage": 37,
                "date": "2020-07-01 00:00:00"
            },
            {
                "id": 3370,
                "ec2_id": "i-0dc802bd6b27c2843",
                "cpu_usage": 2,
                "mem_usage": 58,
                "disk_usage": 37,
                "date": "2020-07-02 00:00:00"
            }
        ]
    }
}
```
### 11.获取今日预留实例
#### 描述
```
获取今日预留实例
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | https://cmdb.jncapp.com:8443/api/usage/v1/ri-usage/today/?pageNum=1&pageSize=15 |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | pageNum | 页码 | N | str |      | 1 |          |
| 2 | pageSize | 一页条数 | N |          |      | 15 |          |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | count | 总条数 |   |
|  4  | pageTotal | 总页数 |   |
|  5 | data | 数据 |   |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| 1 | family | 系列 |  |
| 2 | size | 类型 |  |
| 3| platform | 操作系统 |  |
| 4| total_running | 当前运行（因子）总和 |  |
| 5 | total_ri | 已购（因子）总和 |  |
| 6 | coverage_rate | 预留覆盖率（%） |  |
| 7| date | 日期 |  |



#### 请求URL实例

``` bash
  $ curl https://cmdb.jncapp.com:8443/api/usage/v1/ri-usage/today/?pageNum=1&pageSize=15
  
  
```
#### 返回数据实例

```json
{
    "code": 0,
    "msg": "获取成功",
    "count": 15,
    "pageTotal": 2,
    "data": [
        {
            "id": 79,
            "family": "t2",
            "size": "xlarge",
            "platform": "Linux/UNIX",
            "total_running": "2.28125",
            "total_ri": "2.25000",
            "coverage_rate": "0.98630",
            "date": "2020-07-04 00:00:00"
        },
      
    ]
}
```
### 11.获取历史预留实例
#### 描述
```
获取历史预留实例
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | https://cmdb.jncapp.com:8443/api/usage/v1/ri-usage/history/?start_day=2020-05-01&end_day=2020-07-03&family=c5&size=xlarge&platform=windows |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | start_day | 开始日期 | N | str | 10 | 昨年今天 | 2019-07-03 |
| 2 | end_day | 结束日期 | N | str | 10 | 今天 | 2020-07-03 |
| 3 | family | 系列 | N | str |  | c5 |  |
| 4 | size | 类型 | N | str |  | large |  |
| 5 | platform | 操作系统 | N | str |  | Linux |  |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  2  | count | 返回总数 |   |
|  2  | data | 返回的data |   |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |
| 1 | family | 系列 |  |
| 2 | size | 类型 |  |
| 3| platform | 操作系统 |  |
| 4| total_running | 当前运行（因子）总和 |  |
| 5 | total_ri | 已购（因子）总和 |  |
| 6 | coverage_rate | 预留覆盖率（%） |  |
| 7| date | 日期 |  |


#### 请求URL实例

``` bash
 https://cmdb.jncapp.com:8443/api/usage/v1/ri-usage/history/?start_day=2020-05-01&end_day=2020-07-03&family=c5&size=xlarge&platform=windows
  
  
```
#### 返回数据实例

```json
{
    "code": 0,
    "msg": "获取成功",
    "count": 5,
    "data": [
        {
            "id": 40,
            "family": "c5",
            "size": "xlarge",
            "platform": "windows",
            "total_running": "2.00000",
            "total_ri": "0.00000",
            "coverage_rate": "0.00000",
            "date": "2020-06-06 00:00:00"
        }
    ]
}
```
### 12.显示主机可以节约费用最多的10台EC2主机列表。(2020/7/6增加)
#### 描述
```
显示主机可以节约费用最多的10台EC2主机列表。
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | http://127.0.0.1:8000/v1/usage/report/top10/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-------|
|  |  |  |  |  |  |  |  |



#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  2  | count | 返回总数 |   |
|  2  | data | 返回的data |   |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| - | - | - | - |
|  1| ec2_id | 主机id | - |
|  2| host_name | 主机名 | - |
|  3| project_name | 所属项目 | - |
| 4| cpu_avg_usage | cpu使用率 | - |
|  5| mem_avg_usage | 内存使用率 | - |
|  6| disk_avg_usage | 磁盘使用率 | - |
|  7| curr_inst_type | 当前机型 | - |
|  8| suggest_inst_type | 建议机型 | - |
|  9| cost_gap | 预计节省费用 | - |
|  10| month | 月份 | - |


#### 请求URL实例

``` bash
http://127.0.0.1:8000/v1/usage/report/top10/

https://cmdb.jncapp.com:8443/api/usage/v1/usage/report/top10/
  
```
#### 返回数据实例

```json
{
    "code": 0,
    "msg": "获取成功",
    "count": 10,
    "data": [
        {
            "id": 390,
            "ec2_id": "i-0ef1ed7b9373cd9ca",
            "host_name": "Audit-UAT-Web02",
            "project_name": "Audit",
            "cpu_avg_usage": 0,
            "mem_avg_usage": 5,
            "disk_avg_usage": 4,
            "curr_inst_type": "c5.2xlarge",
            "suggest_inst_type": "t3a.small",
            "cost_gap": "1357.70400",
            "month": "2020-06-01 00:00:00"
        },
        .
        .
        .
        .
        {
            "id": 363,
            "ec2_id": "i-01628e50839c49d44",
            "host_name": "SeeyonOA-NFS",
            "project_name": "Seeyon-OA",
            "cpu_avg_usage": 0,
            "mem_avg_usage": 7,
            "disk_avg_usage": 2,
            "curr_inst_type": "m5.xlarge",
            "suggest_inst_type": "t3a.small",
            "cost_gap": "914.18400",
            "month": "2020-06-01 00:00:00"
        }
    ]
}
```
### 13.有已知项目在年度内每个月的费用信息。(2020/7/6增加)
#### 描述
```
有已知项目在年度内每个月的费用信息
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | http://127.0.0.1:8000/v1/usage/bill/project/Year/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-------|
| 1 | year | 年份 | N | str | 4 | 今年2020 |  |



#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  2  | count | 返回总数 |   |
|  2  | data | 返回的data |   |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| 1 | userproject | 项目名 | - |
|  2| bill_date | 日期 | - |




#### 请求URL实例

``` bash
http://127.0.0.1:8000/v1/usage/bill/project/Year/

https://cmdb.jncapp.com:8443/api/usage/v1/usage/bill/project/Year/
  
```
#### 返回数据实例

```json
{
    "code": 0,
    "msg": "获取成功",
    "count": 45,
    "data": {
        "AIOPS": {
            "2020-05-01 00:00:00": "360.12747",
            "2020-04-01 00:00:00": "496.59874",
            "2020-06-01 00:00:00": "360.12747",
            "2020-07-01 00:00:00": "360.12747"
        },
        "waiqin": {
            "2020-05-01 00:00:00": "0.00000"
        },
        "waiqin365": {
            "2020-05-01 00:00:00": "2505.34557"
        },
        "weaver-oa": {
            "2020-05-01 00:00:00": "345.18219"
        }
    }
}
```
### 14.家族预留实例覆盖率列表，覆盖率数据时间范围为过去30天。。(2020/7/6增加)
#### 描述
```
家族预留实例覆盖率列表，覆盖率数据时间范围为过去30天。
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | http://127.0.0.1:8000/v1/ri-usage/30day/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-------|



#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0添加成功，-1添加失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  2  | count | 返回总数 |   |
|  2  | data | 返回的data |   |


#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
| 1 | 家族型号平台 | 家族型号平台 | - |
|  2| key | 日期 | - |
|  3| value | 覆盖率 | - |




#### 请求URL实例

``` bash
http://127.0.0.1:8000/v1/ri-usage/30day/
https://cmdb.jncapp.com:8443/api/usage/v1/ri-usage/30day/
  
```
#### 返回数据实例

```json
{
    "code": 0,
    "msg": "获取成功",
    "count": 3,
    "data": {
        KEY: {
            key: value,
        },
}

——————————————————————————————
以下是示例返回
{
    "code": 0,
    "msg": "获取成功",
    "count": 3,
    "data": {
        "t2.xlarge.Linux/UNIX": {
            "2020-06-30 00:00:00": "1.01408",
            "2020-07-02 00:00:00": "0.98630",
            "2020-06-06 00:00:00": "0.98630",
            "2020-06-07 00:00:00": "0.98630",
            "2020-06-08 00:00:00": "0.98630",
            "2020-07-04 00:00:00": "0.98630"
        },
      
        "m5.4xlarge.Windows BYOL": {
            "2020-06-30 00:00:00": "100.00000",
            "2020-07-02 00:00:00": "100.00000",
            "2020-06-06 00:00:00": "100.00000",
            "2020-06-07 00:00:00": "100.00000",
            "2020-06-08 00:00:00": "100.00000",
            "2020-07-04 00:00:00": "100.00000"
        },
        "t3.xlarge.Windows BYOL": {
            "2020-06-30 00:00:00": "100.00000",
            "2020-07-02 00:00:00": "100.00000",
            "2020-06-06 00:00:00": "100.00000",
            "2020-06-07 00:00:00": "100.00000",
            "2020-06-08 00:00:00": "100.00000",
            "2020-07-04 00:00:00": "100.00000"
        }
    }
}
```