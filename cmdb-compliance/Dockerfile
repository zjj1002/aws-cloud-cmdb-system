FROM 309544246384.dkr.ecr.cn-northwest-1.amazonaws.com.cn/cmdb-base-py

#修改nginx配置和守护配置

COPY doc/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY doc/supervisor_ops.conf  /etc/supervisord.conf

#修改应用配置
COPY *.* /var/www/cmdb-compliance/
COPY biz  /var/www/cmdb-compliance/biz
COPY doc /var/www/cmdb-compliance/doc
COPY libs /var/www/cmdb-compliance/libs
COPY models /var/www/cmdb-compliance/models
COPY static /var/www/cmdb-compliance/static
COPY prowler /var/www/cmdb-compliance/prowler
COPY clair /var/www/cmdb-compliance/clair
COPY pocsuite /var/www/cmdb-compliance/pocsuite
COPY gitsecrets /var/www/cmdb-compliance/gitsecrets
COPY awssts /var/www/cmdb-compliance/awssts
COPY kube_bench /var/www/cmdb-compliance/kube_bench

ENV PATH /usr/local/bin:$PATH
RUN ln -s /usr/local/bin/aws /usr/bin
RUN apt-get -y install jq
RUN apt-get -y install curl
RUN pip3 install -r /var/www/cmdb-compliance/doc/requirements.txt -i "https://pypi.doubanio.com/simple/"
RUN apt-get install make
RUN git clone https://github.com/awslabs/git-secrets.git;cd git-secrets;make install;git secrets --register-aws --global
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone


EXPOSE 80
CMD ["/usr/local/bin/supervisord"]
