FROM cmdb_base_py

#修改应用配置
ADD settings.py /var/www/cmdb-usage/
COPY *.* /var/www/cmdb-usage/
COPY doc /var/www/cmdb-usage/doc
COPY biz /var/www/cmdb-usage/biz
COPY libs /var/www/cmdb-usage/libs
COPY conf /var/www/cmdb-usage/conf
COPY tmp /var/www/cmdb-usage/tmp
COPY models /var/www/cmdb-usage/models
# COPY __pycache__ /var/www/cmdb-usage/__pycache__
COPY static   /var/www/cmdb-usage/static

#修改nginx配置和守护配置
COPY doc/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY doc/supervisor_ops.conf  /etc/supervisord.conf
RUN pip3 install git+https://github.com/shaneliuyx/awscnprice.git && pip3 install -U git+https://github.com/linjianxing/ops_sdk.git &&  pip3 install -r /var/www/cmdb-usage/doc/requirements.txt -i "https://pypi.douban.com/simple/" --trusted-host pypi.douban.com
# RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
EXPOSE 80
CMD ["/usr/local/bin/supervisord"]
