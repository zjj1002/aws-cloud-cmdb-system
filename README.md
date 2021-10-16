
# 部署方法

## 1. 配置环境变量文件

```bash
    将目录下所有env文件按照需求进行修改.
```
    - aws-cmdb-admin.env
    - aws-cmdb-boto3.env
    - aws-cmdb-mq.env
    - aws-cmdb-mysql.env
    - aws-cmdb-redis.env
    - aws-cmdb-usage.env
    - aws-cmdb-zabbix.env

## 2. 生成gw服务配置文件

```bash
    sh init.sh
```


## 启动容器

```bash
    docker-compose up -d
```

## 创建数据库
```bash
    sh init_db.sh
```

## 测试

```bash

    curl http://127.0.0.1

```

## 默认帐号密码

  - admin/amazonaws

