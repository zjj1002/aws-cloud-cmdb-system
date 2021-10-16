FROM 309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-base-py

COPY doc/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY doc/supervisor_ops.conf  /etc/supervisord.conf

COPY *.* /var/www/cmdb-admin/
COPY doc /var/www/cmdb-admin/doc
COPY libs /var/www/cmdb-admin/libs
COPY mg /var/www/cmdb-admin/mg
COPY models /var/www/cmdb-admin/models

RUN pip3 install -r /var/www/cmdb-admin/doc/requirements.txt -i "https://pypi.doubanio.com/simple/"
EXPOSE 80
CMD ["/usr/local/bin/supervisord"]
