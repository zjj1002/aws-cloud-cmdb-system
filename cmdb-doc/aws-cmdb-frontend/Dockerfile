FROM 871006737058.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-frontend:latest

#修改nginx配置
ADD cmdb_frontend.conf  /etc/nginx/conf.d/cmdb_frontend.conf

EXPOSE 80
EXPOSE 443

STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]
