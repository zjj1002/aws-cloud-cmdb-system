### 1.查询iam用户未使用的用户权限
#### 描述
```
查询出90天内iam用户未使用的用户权限
```
#### 请求地址

| 操作 | 操作名称                 |
| :--: | :----------------------- |
| 协议 | HTTP                     |
| 方式 | GET                      |
| 地址 | /v1/cmdb/iam_permission/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 |
| ---- | :----- | :------- | :--- | :------- | :--- |
| 1    | page   | 当前页码 | N    | Int      | 2    |
| 2    | size   | 每页数量 | N    | Int      | 2    |
| 3    | key    | 模糊查询 | N    | String   |      |

#### 返回数据
| 序号 | 返回值 |    中文名称    | 备注         |
| :--: | :----- | :------------: | :----------- |
|  1   | code   |   请求状态码   | 0代表成功    |
|  1   | msg    |    返回消息    | 消息说明     |
|  1   | total  | 返回数据的总数 | 数据的总数   |
|  1   | data   |    返回数据    | 返回具体数据 |

#### data数据字段说明

| 序号 | 返回值             | 中文名称           | 备注               |
| :--: | :----------------- | :----------------- | :----------------- |
|  1   | user_name          | 用户姓名           | 用户姓名           |
|  2   | user_id            | 用户ID             | 用户ID             |
|  3   | user_arn           | cloudtrail回逆查询 | cloudtrail回逆查询 |
|  4   | services_name      | 大数据查询方式     | 大数据查询方式     |
|  5   | un_used_permission | 未使用的权限       | 未使用的操作权限   |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/iam_permission/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 99,
    "data": [
        {
            "id": 298,
            "user_name": "linjianxing",
            "user_id": "AIDA4VTAMCKRILZO35ZXZ",
            "user_arn": "arn:aws-cn:iam::871006737058:user/linjianxing",
            "services_name": "iam",
            "un_used_permission": "changepassword"
        },
        {
            "id": 299,
            "user_name": "linjianxing",
            "user_id": "AIDA4VTAMCKRILZO35ZXZ",
            "user_arn": "arn:aws-cn:iam::871006737058:user/linjianxing",
            "services_name": "iam",
            "un_used_permission": "getaccountpasswordpolicy"
        },
        {
            "id": 300,
            "user_name": "test-police",
            "user_id": "AIDA4VTAMCKRLFPFSBKZF",
            "user_arn": "arn:aws-cn:iam::871006737058:user/test-police",
            "services_name": "athena",
            "un_used_permission": "batchgetnamedquery"
        },
     ]
}
```