#导入环境变量文件，最开始准备的环境变量文件
source /opt/cmdb/env.sh

#修改配置
#后端数据库名称,建议不要修改，初始化data.sql已经指定了数据库名字，若需改请一块修改
CMDB_DB_DBNAME='cmdb_cmdb'

#任务系统的域名
sed -i "s#cookie_secret = .*#cookie_secret = '${cookie_secret}'#g" settings.py

#mysql配置
sed -i "s#DEFAULT_DB_DBHOST = .*#DEFAULT_DB_DBHOST = os.getenv('DEFAULT_DB_DBHOST', '${DEFAULT_DB_DBHOST}')#g" settings.py
sed -i "s#DEFAULT_DB_DBPORT = .*#DEFAULT_DB_DBPORT = os.getenv('DEFAULT_DB_DBPORT', '${DEFAULT_DB_DBPORT}')#g" settings.py
sed -i "s#DEFAULT_DB_DBUSER = .*#DEFAULT_DB_DBUSER = os.getenv('DEFAULT_DB_DBUSER', '${DEFAULT_DB_DBUSER}')#g" settings.py
sed -i "s#DEFAULT_DB_DBPWD = .*#DEFAULT_DB_DBPWD = os.getenv('DEFAULT_DB_DBPWD', '${DEFAULT_DB_DBPWD}')#g" settings.py
sed -i "s#DEFAULT_DB_DBNAME = .*#DEFAULT_DB_DBNAME = os.getenv('DEFAULT_DB_DBNAME', '${CMDB_DB_DBNAME}')#g" settings.py

#只读MySQL配置
sed -i "s#READONLY_DB_DBHOST = .*#READONLY_DB_DBHOST = os.getenv('READONLY_DB_DBHOST', '${READONLY_DB_DBHOST}')#g" settings.py
sed -i "s#READONLY_DB_DBPORT = .*#READONLY_DB_DBPORT = os.getenv('READONLY_DB_DBPORT', '${READONLY_DB_DBPORT}')#g" settings.py
sed -i "s#READONLY_DB_DBUSER = .*#READONLY_DB_DBUSER = os.getenv('READONLY_DB_DBUSER', '${READONLY_DB_DBUSER}')#g" settings.py
sed -i "s#READONLY_DB_DBPWD = .*#READONLY_DB_DBPWD = os.getenv('READONLY_DB_DBPWD', '${READONLY_DB_DBPWD}')#g" settings.py
sed -i "s#READONLY_DB_DBNAME = .*#READONLY_DB_DBNAME = os.getenv('READONLY_DB_DBNAME', '${CMDB_DB_DBNAME}')#g" settings.py

#redis配置
sed -i "s#DEFAULT_REDIS_HOST = .*#DEFAULT_REDIS_HOST = os.getenv('DEFAULT_REDIS_HOST', '${DEFAULT_REDIS_HOST}')#g" settings.py
sed -i "s#DEFAULT_REDIS_PORT = .*#DEFAULT_REDIS_PORT = os.getenv('DEFAULT_REDIS_PORT', '${DEFAULT_REDIS_PORT}')#g" settings.py
sed -i "s#DEFAULT_REDIS_PASSWORD = .*#DEFAULT_REDIS_PASSWORD = os.getenv('DEFAULT_REDIS_PASSWORD', '${DEFAULT_REDIS_PASSWORD}')#g" settings.py

#这里如果配置cmdb-task的数据库地址，则将数据同步到作业配置

TASK_DB_DBNAME='cmdb_task'
sed -i "s#CMDB_TASK_DB_HOST = .*#CMDB_TASK_DB_HOST = os.getenv('CMDB_TASK_DB_HOST', '${DEFAULT_DB_DBHOST}')#g" settings.py
sed -i "s#CMDB_TASK_DB_PORT = .*#CMDB_TASK_DB_PORT = os.getenv('CMDB_TASK_DB_PORT', '${DEFAULT_DB_DBPORT}')#g" settings.py
sed -i "s#CMDB_TASK_DB_USER = .*#CMDB_TASK_DB_USER = os.getenv('CMDB_TASK_DB_USER', '${DEFAULT_DB_DBUSER}')#g" settings.py
sed -i "s#CMDB_TASK_DB_PWD = .*#CMDB_TASK_DB_PWD = os.getenv('CMDB_TASK_DB_PWD', '${DEFAULT_DB_DBPWD}')#g" settings.py
sed -i "s#CMDB_TASK_DB_DBNAME = .*#CMDB_TASK_DB_DBNAME = os.getenv('CMDB_TASK_DB_DBNAME', '${TASK_DB_DBNAME}')#g" settings.py
