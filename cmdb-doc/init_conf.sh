#!/bin/bash

# replace aws-cmdb-gw config


function add_env()
{
   . ./aws-cmdb-admin.env
   . ./aws-cmdb-redis.env
   . ./aws-cmdb-mysql.env
}

function create_compose_env()
{
   cat aws-cmdb-redis.env > .env
}

function check_env()
{
    [ "${DEFAULT_REDIS_PASSWORD}x" == "x" ] && echo -e "\033[31m No env for DEFAULT_REDIS_PASSWORD  be find. exit.\033[0m" && exit 1
    [ "${ADMIN_TOKEN_SECRET}x" == "x" ] && echo -e "\033[31m No env for ADMIN_TOKEN_SECRET be find. exit.\033[0m" && exit 1
    [ "${ADMIN_SECRET_KEY}x" == "x" ] && echo -e "\033[31m No env for ADMIN_SECRET_KEY be find. exit.\033[0m" && exit 1
}

function create_gw_config()
{
    cd aws-cmdb-gw
    mkdir -p conf lua
 
    cp -r template/conf/* conf
    sed -e "s/REDIS_PASSWORD/${DEFAULT_REDIS_PASSWORD}/g" -e "s/ADMIN_TOKEN_SECRET/${ADMIN_TOKEN_SECRET}/g" -e "s/ADMIN_SECRET_KEY/${ADMIN_SECRET_KEY}/g" template/lua/configs.lua > lua/configs.lua
}

function show()
{
    echo -e "Success!!!!!!!!!!"
}

function main()
{
  add_env
  create_compose_env
  check_env
  create_gw_config
  show
}

#

main
