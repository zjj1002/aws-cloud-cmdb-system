json = require("cjson")

redis_config = {
    host = 'aws-cmdb-redis',
    port = 6379,
    auth_pwd = 'REDIS_PASSWORD',
    db = 8,
    alive_time = 3600 * 24 * 7,
    channel = 'gw'
}


-- token_secret必须要和cmdb-admin里面的token_secret保持一致
token_secret = "ADMIN_TOKEN_SECRET"
logs_file = '/var/log/gw.log'

-- 注意：rewrite_cache_token要和cmdb-admin里面的secret_key保持一致
rewrite_cache_token = 'ADMIN_SECRET_KEY'  

--刷新权限到redis接口
rewrite_cache_url = 'http://aws-cmdb-admin/v2/accounts/verify/'


--并发限流配置
limit_conf = {
    rate = 10, --限制ip每分钟只能调用n*60次接口
    burst = 10, --桶容量,用于平滑处理,最大接收请求次数
}

--upstream匹配规则,API网关域名
gw_domain_name = 'aws-cmdb-gw' 

--下面的转发一定要修改，根据自己实际数据修改
rewrite_conf = {
    [gw_domain_name] = {
        rewrite_urls = {
            {
                uri = "/usage",
                rewrite_upstream = "aws-cmdb-usage"
            },
            {
                uri = "/cmdb",
                rewrite_upstream = "aws-cmdb-cmdb"
            },
            {
                uri = "/cmdb2",
                rewrite_upstream = "aws-cmdb-cmdb"
            },
            {
                uri = "/mg",
                rewrite_upstream = "aws-cmdb-admin"
            },
            {
                uri = "/accounts",
                rewrite_upstream = "aws-cmdb-admin"
            },
            {
                uri = "/compliance",
                rewrite_upstream = "aws-cmdb-compliance"
            },
            {
                uri = "/management",
                rewrite_upstream = "aws-cmdb-management"
            },
        }
    }
}

