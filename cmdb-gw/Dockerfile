FROM 871006737058.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-gw:latest

#修改配置
ADD . /usr/local/openresty/nginx/

EXPOSE 80
CMD ["/usr/bin/openresty", "-g", "daemon off;"]
