FROM 309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-base-py

#修改nginx配置和守护配置

COPY doc/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY doc/supervisor_ops.conf  /etc/supervisord.conf

#修改应用配置
COPY *.* /var/www/cmdb-cmdb/
COPY biz  /var/www/cmdb-cmdb/biz
COPY doc /var/www/cmdb-cmdb/doc
COPY libs /var/www/cmdb-cmdb/libs
COPY models /var/www/cmdb-cmdb/models
COPY static /var/www/cmdb-cmdb/static
COPY inventory /var/www/cmdb-cmdb/inventory

RUN pip3 install -r /var/www/cmdb-cmdb/doc/requirements.txt -i "https://pypi.doubanio.com/simple/"


EXPOSE 80
CMD ["/usr/bin/supervisord"]
