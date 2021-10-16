[TOC]

# 文档说明
  本接口文档给予《ResfulAPI接口开放规范》编写。

# 功能列表

##  网站漏洞扫描
### 1. 获取扫描目标列表 ，添加扫描目标
#### 描述
```
   
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET & post&delete |
| 地址 | /v1/scanner/poc/target |

#### 1.get 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | key | 模糊查询关键词 |  N  |  String |  18  | 无  | 模糊查询关键词 |
| 2 | page | 当前页码 |  N  |  Int |  2  |  1  | 当前页码    |
|3| size | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | data | 返回数据 | 返回具体数据  |
|  1  | total | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | id | 目标id |  |
|  2  | url | 域名 |                    |
|  3  | vul_count | 漏洞数量 |                    |
|  4  | last_modifield | 添加时间 |               |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8000/v1/scanner/poc/target"

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "获取成功",
    "count": 2,
    "data": [
        {
            "id": "target_3ZuTZr6p7JfU5enfXkynGw",
            "url": "www.baidu.com",
            "vul_count": "",
            "last_modifield": ""
        },
        {
            "id": "target_GiqeGDb8XWxFtq2sqHuCMr",
            "url": "www.qq.com",
            "vul_count": "",
            "last_modifield": ""
        }
    ]
}
```

#### 2.post 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | url | 网站url |  Y  |  String |    |   |  |


#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | message | 返回消息 | 消息说明  |



#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8000/v1/scanner/poc/target"

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success"
}
```
#### 3.delete 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | url | 网站url |  Y  |  String |    |   |  |


#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | message | 返回消息 | 消息说明  |



#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8000/v1/scanner/poc/target"

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success"
}
```





### 2. 获取任务列表
#### 描述
```
 
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/scanner/poc/task |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | key | 模糊查询关键词 |  N  |  String |  18  | 无  | 模糊查询关键词 |
| 2 | page | 当前页码 |  N  |  Int |  2  |   1  | 当前页码   |
|3| size | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
| 2  | message | 返回消息 | 消息说明  |
|  3 | data | 返回数据 | 返回具体数据  |
|  4  | total | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | id | 任务id | 显示 |
|  2  | name |   任务名字  | 显示 |
|  3  | poc |     poc集合     |  |
|  4  | target |    vpcid     |  |
|  5  | status |   执行状态   | 显示 |
|  6  | op | 项目组 |      |
|  7  | vul_count | 漏洞数 | 显示 |
|  8  | thread | 线程数 |  |
|  9  | date | 创建日期 | 显示 |
|  10  | end_date | 结束日期 | 显示 |


#### 请求URL实例

``` bash
  $ curl -X get http://127.0.0.1:8000/v1/scanner/poc/task

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 1,
    "data": [
        {
            "id": "task_HAWJgL3V2PrembEfb8m83h",
            "name": "test",
            "target": "target_3ZuTZr6p7JfU5enfXkynGw,target_GiqeGDb8XWxFtq2sqHuCMr",
            "poc": "poc_2RnvfSWsnbaMh75HMTqwJ6,poc_4589WPmR4aExPh9cCKf4eY,poc_4aATiLNuXwPztHPWztRAJh,poc_FVHbkyGJkuCPKonGHoStBt,poc_FzhnHz9XKPhdQrSEEgYhiJ,poc_GAuAEJSoMPJHwVwN9Vs44i,poc_gTWZobZVEp2UQsQVDbhNYa,poc_KkVWaHtSLbRFMamTSvwxhC,poc_LtUqDcH9DutYZWta8JrP8X,poc_NVgxBq8eWjGAQWva7NZdbv,poc_PMZPXYASPRAhFahvCeACAX,poc_R6v7XtuFqFaxx9PrHcSLcj,poc_UQhassvYzNir5NriQZVtCD,poc_ZxAbpdWrSmZKfYqWWNF3JJ,poc_ZzZKvtGhNvNDERnQZaGmbg",
            "thread": null,
            "date": "2020-07-14 01:18:17.260681",
            "end_date": null,
            "status": "2",
            "vul_count": "0",
            "op": null
        }
    ]
}
```

#### 2.post 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | name | 任务名 |  Y  |  String |    |   |  |
| 1 | target_list | 目标网站_id|  Y  |  String |    |   |  |
| 1 | plugin_list | poc_Id |  Y  |  String |    |   |  |


#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | message | 返回消息 | 消息说明  |

#### 3.delete 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | task_id | 任务ID|  Y  |  String |    |   |  |



#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | message | 返回消息 | 消息说明  |



#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8000/v1/scanner/poc/task"

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success"
}
```









### 3. 获取poc列表

#### 描述
```

```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/scanner/poc/plugin |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | key | 模糊查询关键词 |  N  |  String |  18  | 无  | 模糊查询关键词 |
| 2 | page | 当前页码 |  N  |  Int |  2  |   1  | 当前页码   |
|3| size | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | message | 返回消息 | 消息说明  |
|  1  | data | 返回数据 | 返回具体数据  |
|  1  | total | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | id | pocid |   |
|  2  | app | app | 显示 |
| 3  | date | 日期 | 显示 |
|  4  | name | 名字 | 显示 |
|  5  | op | 项目组 | 显示 |
|  6  | poc_str | poc源码 |  |
|  7  | filename | poc文件名字 |   |
| 8 | poctype | poc类型 | 显示 |
|  9  | pid | 进程号 |   |
|  10  | type | 类型 |   |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080//v1/scanner/poc/plugin"

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 15,
    "data": [
        {
            "id": "poc_2RnvfSWsnbaMh75HMTqwJ6",
            "app": "Redis",
            "date": null,
            "name": "Redis Unauthenticated",
            "op": "",
            "poc_str": ""
            "filename": "redis_unauthorized_access.py",
            "poc_type": "Unauthorized access",
            "pid": null,
            "type": null
        },
```


### 4. 获取result
#### 描述
```
 
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/scanner/poc/result |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | task_id | 任务id |  N  |  String |    |   |  |
| 2 | page | 当前页码 |  N  |  Int |  2  |   1  | 当前页码   |
|3| size | 每页显示数 |  N  |  Int |  2  |  10  | 每页显示数        |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  1  | message | 返回消息 | 消息说明  |
|  1  | data | 返回数据 | 返回具体数据  |
|  1  | total | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | id | 运行结果id |   |
|  2  | tid | 任务id |   |
|  3  | poc | pocid |   |
|  4  | task_name | 任务名字 | 显示 |
|  5  | status | 状态 | 显示 |
|  6  | result | 运行结果 | 显示 |
|  7  | url | 网址url | 显示 |
|  8  | mode | 检测类型 | 显示 |
|  9  | vul_id | 漏洞id | 显示 |
|  10  | name | 名字 | 显示 |
|  11  | app_name | app_name | 显示 |
|  12  | app_version | app版本 | 显示 |
|  13  | target | 检测目标 | 显示 |
|  14  | poc_name | poc名字 | 显示 |
|  18  | created     |  检测时间   | 显示 |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080/v1/scanner/poc/result
 
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 2,
    "data": [
        {
            "id": "result_BsybrxVZttV32wztVwm2Uw",
            "tid": "task_Cut8w7fZLoAZYN66YRyufL",
            "poc": "poc_2RnvfSWsnbaMh75HMTqwJ6",
            "task_name": "test",
            "status": "failed",
            "result": "target is not vulnerable",
            "url": null,
            "mode": null,
            "vul_id": "89339",
            "name": "Redis Unauthenticated",
            "app_name": "Redis",
            "app_version": "All",
            "target": "www.baidu.com",
            "poc_name": "Redis Unauthenticated",
            "created": "2020-07-14 13:53:56"
        },
        {
            "id": "result_EJ9PB3Wp59GGHbiXDKd7ia",
            "tid": "task_Cut8w7fZLoAZYN66YRyufL",
            "poc": "poc_2RnvfSWsnbaMh75HMTqwJ6",
            "task_name": "test",
            "status": "failed",
            "result": "target is not vulnerable",
            "url": null,
            "mode": null,
            "vul_id": "89339",
            "name": "Redis Unauthenticated",
            "app_name": "Redis",
            "app_version": "All",
            "target": "www.qq.com",
            "poc_name": "Redis Unauthenticated",
            "created": "2020-07-14 13:53:56"
        }
    ]
}
```
