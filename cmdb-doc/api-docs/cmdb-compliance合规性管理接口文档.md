[TOC]

# 文档说明
  本接口文档给予《ResfulAPI接口开放规范》编写。

# 功能列表

## 合规性管理
### 1. 查询未使用的EIP列表
#### 描述
```
  查询未使用的EIP列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/eip/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | public_ip | 公网ip | NULL表示未知  |
|  2  | allocation_id | 分配的id | NULL表示未知  |
| 3 | public_ipv4_pool | 公网ipv4池 | NULL表示未知 |
| 4 | network_border_group | 网络边界组 | NULL表示未知 |
| 5 | is_used | 是否使用 | NULL表示未知 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/eip/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 2，
    "data": [
        {
            "id": 27,
            "public_ip": "52.80.140.119",
            "allocation_id": "eipalloc-0f825faa70001a752",
            "public_ipv4_pool": "amazon",
            "network_border_group": "cn-north-1",
            "is_used": 0
        },
        {
            "id": 28,
            "public_ip": "52.80.140.119",
            "allocation_id": "eipalloc-0f825faa70001a752",
            "public_ipv4_pool": "amazon",
            "network_border_group": "cn-north-1",
            "is_used": 0
        }
    ] 
}
```



### 2. 没有和任何资源关联的安全组
#### 描述
```
  查询出没有和任何资源关联的安全组
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/sgs |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | security_group_id | 安全组id | 安全组id |
| 2 | security_group_name | 安全组名称 | 安全组名称 |
| 3 | vpc_id | vpc的id | vpc的id |
| 4 | description | 安全组描述 | 安全组描述 |
| 5 | owner_id | owner的id | owner的id |
| 6 | ip_permissions_egress | IpRanges | IpRanges |
| 7 | ip_permissions | 限制ip | 限制ip |
| 8 | is_used | 是否使用 | 是否使用 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/sgs/" 
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 23,
    "data": [
        {
            "id": 131,
            "security_group_id": "sg-01f09e6717c0d23ff",
            "security_group_name": "rds-launch-wizard-2",
            "to_port": "",
            "ip_permissions_egress": "[{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 'Ipv6Ranges': [], 'PrefixListIds': [], 'UserIdGroupPairs': []}]",
            "ip_permissions": "[{'FromPort': 3306, 'IpProtocol': 'tcp', 'IpRanges': [{'CidrIp': '172.31.0.0/16'}], 'Ipv6Ranges': [], 'PrefixListIds': [], 'ToPort': 3306, 'UserIdGroupPairs': []}]",
            "vpc_id": "vpc-b5ff27d1",
            "owner_id": "871006737058",
            "is_used": 0,
            "description": "Created from the RDS Management Console: 2018/10/23 07:49:22"
        },
    ]
}
```


### 3. 查询最小和所需都为0的ASG
#### 描述
```
  查询最小和所需都为0的ASG
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/asg/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功  |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | asg_name | asg名称 | asg名称 |
|  2  | asg_arn | amazon资源名称 | amazon资源名称 |
| 3 | launch_template | 启用模板 | 启用模板 |
| 4 | min_size | 最小值 | 最小值 |
| 5 | max_size | 最大值 | 最大值 |
| 6 | desirced_capacity | 所需容量 | 所需容量 |
| 7 | availability_zones | 可用区 | 可用区 |
| 8 | health_check_type | 运行状况检查类型 | 运行状况检查类型 |
| 9 | asg_created_time | asg创建的时间 | asg创建的时间 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/asg/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 1,
    "data": [
        {
            "id": 1,
            "asg_name": "my_test",
            "asg_arn": "arn:aws-cn:autoscaling:cn-north-1:871006737058:autoScalingGroup:96df7880-0aee-438c-834e-b3cfca2313ee:autoScalingGroupName/my_test",
            "launch_template": "{'LaunchTemplateId': 'lt-0ba3d3e2e7c786122', 'LaunchTemplateName': 'my_template', 'Version': '$Default'}",
            "min_size": 0,
            "max_size": 1,
            "desirced_capacity": 0,
            "availability_zones": "cn-north-1a",
            "health_check_type": "EC2",
            "asg_created_time": "2020-06-11 02:45:15.995000+00:00"
        }
    ]
}
```


### 4. 查询出不合规的ec2主机
#### 描述
```
  查询出未使用合规ami启动的ec2主机
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/uncom_ec2/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功  |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | instance_id | 实例id | 实例id       |
| 2 | ami_id | 镜像id | 镜像id |
| 3 | instance_type | 实例类型 | 实例类型 |
| 4 | key_name | 密钥对名称 | NULL表示未知 |
| 5 | launch_time | 启动时间 | 启动时间 |
| 6 | placement | 置放信息 | 置放信息 |
| 7 | private_dns_name | 私有dns名称 | 私有dns名称 |
| 8 | private_ip_address | 私有ip | 私有ip |
| 9 | public_dns_name | 公有dns名称 | 公有dns名称 |
| 10 | public_ip_address | 公有ip | 公有ip |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/uncom_ec2/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 4,
    "data": [
        {
            "id": 5,
            "instance_id": "i-0021705a9f56a849c",
            "ami_id": "ami-088b61f50b18f807e",
            "instance_type": "c4.4xlarge",
            "key_name": "cmdb",
            "launch_time": "2020-03-06 09:11:31",
            "placement": "{'AvailabilityZone': 'cn-north-1a', 'GroupName': '', 'Tenancy': 'default'}",
            "private_dns_name": "ip-172-31-31-79.cn-north-1.compute.internal",
            "private_ip_address": "172.31.31.79",
            "public_dns_name": "ec2-52-81-23-137.cn-north-1.compute.amazonaws.com.cn",
            "public_ip_address": "52.81.23.137"
        }
    ]
}
```



### 5. 把不合规的ami信息插入到cmdb数据库中
#### 描述
```
  把不合规的ec2的ami添加到cmdb数据库中，让ami变成合规的ami
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | POST |
| 地址 | /v1/cmdb/ami/<ami_id> |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注                           |
| ----- |:----|:-------|:-----|:-----|:---|:----|:-----------------------------|
| 1 | ami_id | ami的id |  Y  | String |  32  |   无  | ami的id   |

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0请求成功    |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | ami_id | ami的id | ami的id |


#### 请求URL实例

``` bash
  $ curl -X POST "https://cmdb.jncapp.com/api/compliance/v1/cmdb/ami" -d '{"ami_id":"ami-0eeb3a63"}'
```

#### 返回数据实例

``` json
1
```
### 6. VPC的peering中的account ID不为当前owner的账户ID
#### 描述
```
查询出VPC的peering中的account ID不为当前owner的账户ID的vpc peering列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/uncom_vpc_peering/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0代表成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:------|:---|
|  1  | id | 序号id | 序号id |
| 2 | vpc_peering_connection_id | vpc对等连接id | vpc对等连接id |
| 3 | requester_cidr_block | 请求方的cidr块 | 请求方的cidr块 |
| 4 | requester_owner_id | 请求方的owner id | 请求方的owner id |
| 5 | requester_vpc_id | 请求方的vpc id | 请求方的vpc id |
| 6 | requester_region | 请求方的区域 | 请求方的区域 |
| 7 | accepter_cidr_block | 接收方的cidr块 | 接收方的cidr块 |
| 8 | accepter_owner_id | 接收方的owner id | 接收方的owner id |
| 9 | accepter_vpc_id | 接收方的vpc id | 接收方的vpc id |
| 10 | accepter_region | 接收方的区域 | 接收方的区域 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/uncom_vpc_peering/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 1,
    "data": [
        {
            "id": 1,
            "vpc_peering_connection_id": "pcx-0fd29d0ef201a2ab6",
            "requester_cidr_block": "192.168.0.0/16",
            "requester_owner_id": "871006737058",
            "requester_vpc_id": "vpc-0ea00edac15d10858",
            "requester_region": "cn-north-1",
            "accepter_cidr_block": "172.31.0.0/16",
            "accepter_owner_id": "871006737058",
            "accepter_vpc_id": "vpc-b5ff27d1",
            "accepter_region": "cn-north-1"
        }
    ]
}
```
### 7. 未启用 S3 或者ECR ENDPOINT的VPC列表
#### 描述
```
查询出未启用S3 ENDPOINT或者 ECR ENDPOINT的VPC列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/uncom_vpc/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0代表成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:------|:---|
|  1  | vpc_id | vpc的id | vpc的id |
| 2 | state | vpc的状态      | vpc的状态 |
| 3 | cidr_block | vpc的cidr块 | vpc的cidr块 |
| 4 | dhcp_options_id | dhcp选项集的id | dhcp选项集的id |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/uncom_vpc/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 1,
    "data": [
        {
            "vpc_id": "vpc-010e4ba14a1542f24",
            "state": "available",
            "cidr_block": "32425254",
            "dhcp_options_id": "4534535345"
        }
    ]
}
```
### 8.显示 prowler data列表
#### 描述
```
显示 prowler 数据列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/prowler_data/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0代表成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:------|:---|
|  1  | profile | profile | profile |
| 2 | result | 结果    | 结果 |
| 3 | level | 等级 | 等级 |
| 4 | region | 区域 | 区域 |
| 5 | account_id | 账户id | 账户id |
| 6 | group | 组 | 组 |
| 7 | check_id | check id | check id |
| 8 | check_title | check 标题 | check 标题 |
| 9 | check_output | check 输出 | check 输出 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/unconventional_cis/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 3483,
    "data": [
        {
            "id": 24406,
            "profile": "default",
            "result": "INFO",
            "level": "Level 1",
            "region": "cn-northwest-1",
            "account_id": "309544246384",
            "group": "Scored",
            "check_id": 1.3,
            "check_title": "[check13] Ensure credentials unused for 90 days or greater are disabled (Scored)",
            "check_output": "User bi_user_gj has not logged into the console since creation"
        }
    ]
}
```

### 9.显示 gdpr data列表
#### 描述
```
显示 gdpr 数据列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/gdpr_data/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0代表成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:------|:---|
|  1  | profile | profile | profile |
| 2 | result | 结果    | 结果 |
| 3 | level | 等级 | 等级 |
| 4 | region | 区域 | 区域 |
| 5 | account_id | 账户id | 账户id |
| 6 | group | 组 | 组 |
| 7 | check_id | check id | check id |
| 8 | check_title | check 标题 | check 标题 |
| 9 | check_output | check 输出 | check 输出 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/gdpr_data/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 3483,
    "data": [
        {
            "id": 24406,
            "profile": "default",
            "result": "INFO",
            "level": "Level 1",
            "region": "cn-northwest-1",
            "account_id": "309544246384",
            "group": "Scored",
            "check_id": 1.3,
            "check_title": "[check13] Ensure credentials unused for 90 days or greater are disabled (Scored)",
            "check_output": "User bi_user_gj has not logged into the console since creation"
        }
    ]
}
```
### 10.显示 hipaa data列表
#### 描述
```
显示 hipaa 数据列表
```
#### 请求地址

|操作| 操作名称 |
|:---:|:---|
| 协议 | HTTP |
| 方式 | GET |
| 地址 | /v1/cmdb/hipaa_data/ |

#### 请求参数

| 序号 | 参数名 | 中文名称 | 必选 | 数据类型 | 长度 | 默认值 | 备注 |
| ----- |:----|:-------|:-----|:-----|:---|:---|:---|
| 1 | key | 查询关键字 |  N  |  String |  18  |无|模糊查询关键字|
| 2 | page | 当前页码 |  N  |  Int |  2  |1|当前页码|
| 3 | size | 每页数量 | N | Int | 2 |10|每页数量|

#### 返回数据
| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:-----:|:---|
|  1  | code | 请求状态码 | 0代表成功 |
|  1  | msg | 返回消息 | 消息说明  |
|  1  | total | 返回数据的总数 | 数据的总数  |
|  1  | data | 返回数据 | 返回具体数据  |

#### data数据字段说明

| 序号  | 返回值   | 中文名称  | 备注 |
|:---:|:------|:------|:---|
|  1  | profile | profile | profile |
| 2 | result | 结果    | 结果 |
| 3 | level | 等级 | 等级 |
| 4 | region | 区域 | 区域 |
| 5 | account_id | 账户id | 账户id |
| 6 | group | 组 | 组 |
| 7 | check_id | check id | check id |
| 8 | check_title | check 标题 | check 标题 |
| 9 | check_output | check 输出 | check 输出 |


#### 请求URL实例

``` bash
  $ curl "https://cmdb.jncapp.com/api/compliance/v1/cmdb/hipaa_data/"
```

#### 返回数据实例

``` json
{
    "code": 0,
    "msg": "success",
    "total": 3483,
    "data": [
        {
            "id": 24406,
            "profile": "default",
            "result": "INFO",
            "level": "Level 1",
            "region": "cn-northwest-1",
            "account_id": "309544246384",
            "group": "Scored",
            "check_id": 1.3,
            "check_title": "[check13] Ensure credentials unused for 90 days or greater are disabled (Scored)",
            "check_output": "User bi_user_gj has not logged into the console since creation"
        }
    ]
}
```