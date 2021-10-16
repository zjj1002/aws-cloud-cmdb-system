#!/bin/bash
#

. ./aws-cmdb-mysql.env
mysql -h127.0.0.1 -uroot -p${MYSQL_ROOT_PASSWORD} -e 'create database cmdb_admin  default character set utf8mb4 collate utf8mb4_unicode_ci;'
mysql -h127.0.0.1 -uroot -p${MYSQL_ROOT_PASSWORD} -e 'create database cmdb_cmdb default character set utf8mb4 collate utf8mb4_unicode_ci;'
docker exec -ti cmdb-doc_aws-cmdb-admin_1  /usr/local/bin/python3 /var/www/cmdb-admin/db_sync.py
docker exec -ti cmdb-doc_aws-cmdb-usage_1  /usr/local/bin/python3 /var/www/cmdb-usage/db_sync.py
docker exec -ti cmdb-doc_aws-cmdb-cmdb_1  /usr/local/bin/python3 /var/www/cmdb-cmdb/db_sync.py
mysql -h127.0.0.1 -uroot -p${MYSQL_ROOT_PASSWORD} cmdb_admin < ./cmdb_admin.sql
