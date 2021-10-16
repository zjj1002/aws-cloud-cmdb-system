
FROM 309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-gw

#修改配置
ADD conf/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
RUN rm -rf /usr/local/openresty/nginx/conf/conf.d
COPY conf/conf.d /usr/local/openresty/nginx/conf/conf.d
ADD lua/configs.lua /usr/local/openresty/nginx/lua/configs.lua


EXPOSE 80
CMD ["/usr/bin/openresty", "-g", "daemon off;"]
