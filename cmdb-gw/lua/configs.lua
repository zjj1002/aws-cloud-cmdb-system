json = require("cjson")

--mysql_config = {
--    host = "127.0.0.1",
--    port = 3306,
--    database = "lua",
--    user = "root",
--    password = "",
--    max_packet_size = 1024 * 1024
--}

redis_config = {
    host = '172.21.20.221',
    --host = '172.16.0.121',
    port = 6379,
    auth_pwd = 'cWCVKJ72HUK12mVbivUf',
    db = 8,
    alive_time = 3600 * 24 * 7,
    channel = 'gw'
}

--mq_conf = {
--	host = '172.16.0.121',
--	port = 5672,
--	username = 'sz',
--	password = '123456',
--	vhost = '/'
--}

token_secret = "pXFb4i%*824gfdh963df718iodGq4dsafsdadg7yI6ImF1999aaG7"
logs_file = '/var/log/gw.log'

--刷新权限到redis接口
rewrite_cache_url = 'http://mg.awscmdb.cn:8010/v2/accounts/verify/'
rewrite_cache_token = '8b888a62-3edb-4920-b446-697a472b4001'

--并发限流配置
limit_conf = {
    rate = 10, --限制ip每分钟只能调用n*60次接口
    burst = 10, --桶容量,用于平滑处理,最大接收请求次数
}

--upstream匹配规则
gw_domain_name = 'gw.awscmdb.cn'

rewrite_conf = {
    [gw_domain_name] = {
        rewrite_urls = {
            {
                uri = "/dns",
                rewrite_upstream = "dns.awscmdb.cn:8060"
            },
            {
                uri = "/cmdb2",
                rewrite_upstream = "cmdb2.awscmdb.cn:8050"
            },
            {
                uri = "/tools",
                rewrite_upstream = "tools.awscmdb.cn:8040"
            },
            {
                uri = "/kerrigan",
                rewrite_upstream = "kerrigan.awscmdb.cn:8030"
            },
            {
                uri = "/cmdb",
                rewrite_upstream = "cmdb.awscmdb.cn:8002"
            },
            {
                uri = "/k8s",
                rewrite_upstream = "k8s.awscmdb.cn:8001"
            },
            {
                uri = "/task",
                rewrite_upstream = "task.awscmdb.cn:8020"
            },
            {
                uri = "/cron",
                rewrite_upstream = "cron.awscmdb.cn:9900"
            },
            {
                uri = "/mg",
                rewrite_upstream = "mg.awscmdb.cn:8010"
            },
            {
                uri = "/accounts",
                rewrite_upstream = "mg.awscmdb.cn:8010"
            },
        }
    }
}
