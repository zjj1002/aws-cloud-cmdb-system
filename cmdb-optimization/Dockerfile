FROM cmdb_base_py

#修改nginx配置和守护配置

COPY doc/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY doc/supervisor_ops.conf  /etc/supervisord.conf

#修改应用配置
COPY *.* /var/www/cmdb-optimization/
COPY biz  /var/www/cmdb-optimization/biz
COPY doc /var/www/cmdb-optimization/doc
COPY libs /var/www/cmdb-optimization/libs
COPY models /var/www/cmdb-optimization/models
COPY static /var/www/cmdb-optimization/static


ENV PATH /usr/local/bin:$PATH
RUN ln -s /usr/local/bin/aws /usr/bin
RUN apt-get -y install jq
RUN apt-get -y install curl
RUN pip3 install -r /var/www/cmdb-optimization/doc/requirements.txt -i "https://pypi.doubanio.com/simple/"
RUN apt-get install make
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone


EXPOSE 80
CMD ["/usr/local/bin/supervisord"]
