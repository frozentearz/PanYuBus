#!/bin/bash

# 安装定时脚本，添加时间规则
response="cron is installed"
echo "#初始化 cron ......" >> ./panyubus.log
result=$(sed -n '2p' ./panyubus.log)
# head -1 ./panyubus.log
# 如果不相等，即 Cron 尚未初始化
if [[ $result != $response ]]; then
    chmod +x cron.sh
    ./cron.sh
fi

# 打印日志
date >> panyubus.log
echo "----------------------------------------------------" >> panyubus.log
python panyubus.py >> panyubus.log 2>&1