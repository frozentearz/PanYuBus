#!/bin/bash

# 安装定时脚本，添加时间规则
response="cron is installed"
echo "#初始化 cron ......" >> ./panyubus.log
result=$(sed -n '2p' ./panyubus.log)
# head -1 ./panyubus.log
# 如果不相等，即 Cron 尚未初始化
if [[ $result != $response ]]; then
    echo "Cron 尚未初始化，正在尝试初始化....."
    chmod +x cron.sh
    ./cron.sh
fi

# 打印日志
echo " " >> panyubus.log
date >> panyubus.log
echo "----------------------------------------------------" >> panyubus.log
python panyubus.py >> panyubus.log 2>&1