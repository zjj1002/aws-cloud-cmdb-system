# API网关项目介绍
API网关系统,是基于openresty + Lua开发的一套API网关系统,主要功能如下：

- API鉴权

- API 限速

- 日志记录

- 白名单 （未完成）

- 熔断 （未完成）

# 一、服务部署
#### openresty 编译安装
```
wget https://openresty.org/download/openresty-1.13.6.2.tar.gz
tar zxf openresty-1.13.6.2.tar.gz && cd openresty-1.13.6.2
./configure --prefix=/usr/local/openresty-1.13.6.2 \
--with-luajit --with-http_stub_status_module \
--with-pcre --with-pcre-jit
gmake && gmake install
ln -s /usr/local/openresty-1.13.6.2/ /usr/local/openresty
ln -s /usr/local/openresty/bin/resty /usr/bin/resty
```

####  yum安装
```bash
# yum部署
yum install yum-utils
yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo
yum install openresty
yum install openresty-resty
```
#####  代码部署
```bash
\cp -arp api-gateway/* /usr/local/openresty/nginx/
```

# 二、 修改配置 
   ##### 文件 /usr/local/openresty/nginx/conf/nginx.conf
   -  修改 resolver 172.16.0.21; 为resolver DNS服务器。
   ##### 文件 /usr/local/openresty/nginx/conf/conf.d/gw.conf
   -  修改 lua_code_cache on; 线上环境设置为on
   -  修改 server_name  为你的网关域名
   ##### 文件 /usr/local/openresty/nginx/lua/configs.lua
   - token_secret 为你的令牌的密钥 和登录JWT 服务的key一致
   - rewrite_cache_url 刷新权限到redis接口  
   - rewrite_cache_token  为获取权限的令牌
   #### - login_url 当token 无效或者过期 跳转的登录页面
   - limit_conf 并发 限制默认即可 如有需求下面有详细介绍
   - rewrite_conf 注册API 下面有详解
          


# 三、使用配置,注册API
> 要接入API网关系统，则要先进行注册，注册方式如下：

​	a、配置文件configs.lua中的rewrite_conf

​	b、POST注册接口(暂无)

注册示例如下：
上级nginx 配置示例
```
server {
        listen      80;
        server_name demo.awscmdb.cn
        access_log /var/log/nginx/ops-demo_access.log;
        error_log  /var/log/nginx/ops-demo_error.log;

        location / {
                    root /var/www/admin-front;
                    index index.html index.htm;
                    try_files $uri $uri/ /index.html;
                    expires 3d;
        }
        location /api {
                proxy_redirect off;
                proxy_read_timeout 600;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                
                add_header 'Access-Control-Allow-Origin' '*';
                proxy_pass http://gw.awscmdb.cn;
        }
        location ~ /(.svn|.git|admin|manage|.sh|.bash)$ {
            return 403;
        }
    }
```
- 通过 api代理到api网关， 网关会把URI的第一位删除, 第二位是服务标示，之后的才是真正后端的API的URI地址，当然权限还是会从服务标示开始匹配
```lua
gw_domain_name = 'gw.awscmdb.cn'

rewrite_conf = {
    [gw_domain_name] = {
        rewrite_urls = {
            {
                uri = "/cmdb",
                rewrite_upstream = "172.16.80.12:8000"
            },
            {
                uri = "/task",
                rewrite_upstream = "172.16.0.223:8900"
            },
            {
                uri = "/cron",
                rewrite_upstream = "172.16.0.223:9900"
            },
            {
                uri = "/mg",
                rewrite_upstream = "172.16.0.223:9800"
            },
            {
                uri = "/accounts",
                rewrite_upstream = "172.16.0.223:9800"
            },
        }
    }
}
```



如上可以看到，注册了的服务【cron】【mg】【accounts】
accounts 做过处理 不用经过鉴权



# 四、API限速

在configs.lua文件中配置limit,配置示例如下

```lua
limit_conf = {
    rate = 5,   --限制ip每分钟只能调用n*60次接口
    burst = 10, 	 --桶容量,用于平滑处理,最大接收请求次数
}
```

次配置为每秒5个并发请求，并临时允许超出10个请求并平滑处理掉：

测试：（最好先关闭权限验证，方便测试）

```shell
ab -c 100 -n 1000 http://gw.awscmdb.cn/cron/v1/cron/log/
```
可以看到,差不多有21个请求是成功的
```bash
Document Path:          /cron/v1/cron/log/
Document Length:        11852 bytes

Concurrency Level:      100
Time taken for tests:   3.982 seconds
Complete requests:      1000
Failed requests:        979
```

再试试 并发5个请求 如下:
```shell
ab -c 5 -n 1000 http://gw.awscmdb.cn/cron/v1/cron/log/ 
```
```bash
Document Path:          /cron/v1/cron/log/
Document Length:        11852 bytes

Concurrency Level:      5
Time taken for tests:   199.811 seconds
Complete requests:      1000
Failed requests:        0
Write errors:           0
```



# 五、日志记录

在configs.lua文件中配置log地址及redis channel

- get请求日志会访日本地log
- 非get请求会发送给redis channel 需要自己接受记录

```bash
[root@CentOS7-Shinezone /var/log]#tailf gw.log
{"time":"2018-09-19 10:44:48","uri":"\/devops\/api\/v1.0\/job\/","login_ip":"172.16.0.121","method":"GET"}
{"time":"2018-09-19 10:44:48","uri":"\/devops\/api\/v1.0\/job\/","login_ip":"172.16.0.121","method":"GET"}
```

```
[root@CentOS7-Shinezone /var/log]#redis-cli -h 127.0.0.1 -p 6379
127.0.0.1:6379> SUBSCRIBE gw
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "gw"
3) (integer) 1


1) "message"
2) "gw"
3) "{\"time\":\"2018-09-19 10:48:52\",\"uri\":\"\\/devops\\/api\\/v1.0\\/job\\/\",\"login_ip\":\"172.16.80.12\",\"method\":\"POST\"}"
```

# docker 部署

**配置修改参考上述内容**

```
#删除前端的配置文件
mv conf/conf.d/demo.conf  conf/conf.d/demo.conf-bak

#bulid镜像
docker build . -t gateway_image

#启动
docker-compose up -d
```
**使用docker部署启动之后端口为8888，防止单机部署造成端口冲突，如果想修改端口请修改`docker-compose.yml`文件。**

**默认域名：`http://gw.awscmdb.cn:8888` 如果需要修改域名请修改`conf/conf.d/gw.conf`文件。**

## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).