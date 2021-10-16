[TOC]

# 文档说明
  本接口文档给予《ResfulAPI接口开放规范》编写。

# 功能列表

##  合规性管理功能说明
### 1. 不合规的RDS列表
#### 描述
```
    连续7天无新建链接的资源
    开启公网访问的RDS
    RDS备份保留期低于15天或者没有开启备份的
    未启用加密存储的rds
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/rds/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | key | 模糊查询关键词 |  N  |  String |  18  | 无  | 模糊查询关键词 |
| 2 | page | 当前页码 |  N  |  Int |  2  |  1  | 当前页码    |
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
|  1  | db_Identifier | rds的Identifier | db_Identifier |
|  2  | db_region | 区域 | 区域                   |
|  3  | db_host | host | host                   |
|  4  | db_instance_id | id | rds实例id              |
|  5  | db_conn | 7天连接数 | 是否符合七天内有连接   |
|  6  | db_public_access | 公网访问 | 是否符合关闭公网访问   |
|  7  | db_backup | 备份 | 是否符合打开备份       |
|  8  | db_backup_period | 备份时间 | 是否符合备份时间超15天 |
|  9  | db_enncrypted | 加密存储 | 是否符合存储加密 |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080/v1/cmdb/rds/"
  https://cmdb.jncapp.com/api/compliance/v1/cmdb/rds/

```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "db_identifier": "audit-old",
            "id": 1,
            "db_region": "cn-northwest-1b",
            "db_host": "audit-old.cotpwdfxy0tl.rds.cn-northwest-1.amazonaws.com.cn",
            "db_instance_id": "db-AS5GGRVVFY5K7GE7VXCXBOAUPY",
            "db_conn": true,
            "db_enncrypted": true,
            "db_public_access": true,
            "db_backup": true,
            "db_backup_period": false
        },
    ],
    "total": 30
}
```



### 2. 不合规的elb
#### 描述
```
  不合规的elb
  1.未使用的ELB ALB NLB 
  2.未使用加密传输的公网ELB
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/cmdb/elb/ |

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
|  1  | name | 名字 | 用户ID  |
|  2  | dnsname |   dns名字    | dns名字 |
|  3  | region |     区域     | 区域 |
|  4  | vpcid |    vpcid     | vpcid |
|  5  | scheme |   传输类型   | 传输类型（内网和外网） |
|  6  | is_use | 是否使用 | 是否使用（布尔类型）     |
|  7  | type | 类型 | 类型（alb，elb，nlb） |
|  8  | is_encry_trans | 是否加密传输 | 是否加密传输（布尔类型） |


#### 请求URL实例

``` bash
  $ curl -X get "http://127.0.0.1:8080/v1/cmdb/elb/
    https://cmdb.jncapp.com/api/compliance/v1/cmdb/elb/
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 65,
            "name": "api-dev-cluster-zhy-k8s-l-imcvvh",
            "dnsname": "api-dev-cluster-zhy-k8s-l-imcvvh-1390682017.cn-northwest-1.elb.amazonaws.com.cn",
            "region": "cn-northwest-1a/cn-northwest-1b/cn-northwest-1c",
            "vpcid": "vpc-ee67da87",
            "scheme": "internet-facing",
            "is_use": true,
            "type": "network",
            "is_encry_trans": false
        },
    ],
    "total": 1
}
```


### 3. 不合规的NatGateWay
#### 描述
```
  未使用的nat网关
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/natgateway/ |

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
|  1  | natgatewayid | 用户名 | NULL表示未知  |
|  2  | state | 状态 | NULL表示未知  |
| 3  | subnetId | subnetId | NULL表示未知  |
|  4  | vpcid | vpcid | NULL表示未知  |
|  5  | is_use | 是否可用 | NULL表示未知  |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080/v1/cmdb/natgateway/"
  https://cmdb.jncapp.com/api/compliance/v1/cmdb/natgateway/
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 12,
            "natgatewayid": "nat-021513a97af0cccdb",
            "state": "available",
            "subnetId": "subnet-02c26dcad67717ea3",
            "vpcid": "vpc-011e0c0779abc4792",
            "is_use": false
        }
    ],
    "total": 1
}
```


### 4. 不合规的iam
#### 描述
```
 拥有两个AK SK的用户
 180天内未登陆的用户列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/cmdb/iam/ |

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
|  1  | user_id | 用户ID | NULL表示未知  |
|  2  | user_name | 用户姓名 | NULL表示未知  |
|  3  | arn | 用户资源 | NULL表示未知  |
|  4  | is_180_signin | 180内有登录 | NULL表示未知  |
|  5  | is_2_keys | 有两个ak/sk | NULL表示未知  |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080/v1/cmdb/iam/
    https://cmdb.jncapp.com/api/compliance/v1/cmdb/iam/   TODO
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 65,
            "user_id": "AIDAUQESGLRYMZE43YZUP",
            "user_name": "user_oms_dev",
            "arn": "arn:aws-cn:iam::309544246384:user/user_oms_dev",
            "is_180_signin": false,
            "is_2_keys": true
        }
    ],
    "total": 1
}
```
### 5. 未使用的或加密存储的或snapshot时间大于30天的ebs
#### 描述
```
 未关联的EBS卷
 未启用加密的EBS卷
 超过一个月的EBS snapshot
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/cmdb/ebs/ |

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
|  1  | Attachments | 关联 | NULL表示未知  |
|  2  | AvailabilityZone | 区域 | NULL表示未知  |
|  3  | CreateTime | 创建时间 | NULL表示未知  |
|  4  | Encrypted | 加密 | false表示未加密 |
|  5  | Size | 大小 | NULL表示未知  |
|  6  | SnapshotId | 快照id | NULL表示未知  |
|  7 | State | 状态 | NULL表示未知  |
|  8  | VolumeId | 卷id | NULL表示未知  |
| 9  | Iops | lops | NULL表示未知  |
|  10  | VolumeType | 卷类型 | NULL表示未知  |
|  11  | Snapshot_overtime | 快照超30天 | false 表示已超时 |





#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080/v1/cmdb/ebs/
      https://cmdb.jncapp.com/api/compliance/v1/cmdb/ebs/
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 1,
    "data": [
        {
            "snapshot_overtime": "false",
            "id": 209,
            "Attachments": "磁盘有人使用",
            "AvailabilityZone": "cn-northwest-1c",
            "CreateTime": "2019-06-05",
            "Encrypted": "false",
            "Size": 30,
            "SnapshotId": "snap-0fef38e97fa28e328",
            "State": "in-use",
            "VolumeId": "vol-0f72f9d04575ab2e8",
            "Iops": 100,
            "VolumeType": "gp2"
        },
]}
```
### 6. 未使用的target_groups
#### 描述
```
 
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | /v1/cmdb/targetgroups/ |

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
|  1  | target_group_name | target_group名字 | NULL表示未知  |
|  2  | target_group_arn | target_group_arn | NULL表示未知  |
|  3  | protocol | 传输协议 | NULL表示未知  |
|  4  | port | 端口 | NULL表示未知  |
|  5  | vpc_id | vpc_id | NULL表示未知  |
|  6  | target_type | 类型 | NULL表示未知  |
|  7  | is_use | 是否使用 | false表示未使用 |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8080/v1/cmdb/targetgroups/
    https://cmdb.jncapp.com/api/compliance/v1/cmdb/targetgroups/  
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 1,
    "data": [
        {
            "id": 111,
            "target_group_arn": "arn:aws-cn:elasticloadbalancing:cn-northwest-1:309544246384:targetgroup/3988c11c-215f66220c6c56794c2/b698535f317be5d5",
            "target_group_name": "3988c11c-215f66220c6c56794c2",
            "protocol": "HTTP",
            "port": 1,
            "vpc_id": "vpc-ee67da87",
            "target_type": "instance",
            "is_use": false
        },
    ]
}
```

### 7. 合规性汇总
#### 描述
```
 
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | get |
| 地址 | http://127.0.0.1:8000/v1/cmdb/gather/|

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|



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
|  1  | EBS | 不合规的ebs |   |
|  2  | ELB | 未使用&未加密的elb |   |
|  3  | TARGETGROUP | 不合规的目标群组 |   |
|  4  | IAM | 未使用的iam |   |
|  5  | NAT | 未使用的natgateway |   |
|  6  | RDS | 七天连接数为0的rds |   |
|  7  | eip | 未使用的eip |  |
|  8  | sgs | 未与任何资源关联的安全组 |  |
|  9  | asg | 最小和所需关连的安全组 |  |
|  10  | vpc | 不合规的vpc |  |
|  11  | vpc_peeering | 不合规的vpcpeering |  |
|  12  | ec2 | 不合规的ec2 |  |
|  13  | gdpr | gdpr合规性检查 |  |
|  14  | hippa | hippa合规性检查 |  |
|  15  | prowler |  亚马逊cis合规性检查|  |


#### 请求URL实例

``` bash
  $ curl "http://127.0.0.1:8000/v1/cmdb/gather/
    https://cmdb.jncapp.com/api/compliance/v1/cmdb/gather/
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total":12
    "data": {
        "EBS_DB": 204,
        "ELB_DB": 37,
        "TARGETGROUP_DB": 22,
        "IAM_DB": 17,
        "NAT_DB": 8,
        "RDS_DB": 31，
        "eip":1
        "sgs":1
        "asg":1
        "vpc":1
        "vpc_peering":1
        "ec2":1
        "gdpr":1,
        "hippa":1,
        "prowler":1
        
    }
}
```

