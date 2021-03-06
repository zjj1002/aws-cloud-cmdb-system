[TOC]

# 文档说明
  本接口文档给予《ResfulAPI接口开放规范》编写。

# 功能列表

##  资产管理模块接口添加
### 1. 获取主域名接口
#### 描述
```
 获取主域名接口
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | https://cmdb.jncapp.com:8443/api/cmdb2/v1/cmdb/main_dns/ |

#### get 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
|      |        |          |      |          |      |        |      |


#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功，-2请求失败 |
|  2  | msg | 返回消息 | 消息说明  |
|  3  | data | 返回数据 | 返回具体数据  |
|  4  | count  | 返回数据总数 |  返回数据总数  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|    |  |  |  |



#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com:8443/api/cmdb2/v1/cmdb/main_dns/"

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "获取成功",
    "data": [
        "jncapp.cn",
        "jncapp.com"
    ],
    "count": 2
}
```





