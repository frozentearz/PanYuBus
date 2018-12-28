#!/bin/bash

# 安装定时脚本，添加时间规则
response="cron is installed"
echo "#初始化 cron ......" >> ./panyubus.log
result=$(sed -n '2p' ./panyubus.log)
# head -1 ./panyubus.log
# 如果不相等，即 Cron 尚未初始化
if [[ $result != $response ]]; then
    echo "Cron 尚未初始化，正在尝试初始化....."
    echo "cron is installed" >> panyubus.log
    result=$(lsb_release -a | tr 'A-Z' 'a-z')

    # RedHat 系列
    redhat="redhat"
    centos="centos"
    fedora="fedora"
    # Debian 系列
    ubuntu="ubuntu"
    debian="debian"

    echo "开始检测系统发行版本......"
    if [[ $result =~ $ubuntu || $result =~ $debian ]]; then
        echo "检测完成，您的系统为："
        echo $result
        echo "开始安装相应发行版本 Cron"
        apt-get install cron >> panyubus.log 2>&1
        service cron start
    elif [[ $result =~ $redhat || $result =~ $centos || $result =~ $fedora ]]; then
        echo "检测完成，您的系统为："
        echo $result
        echo "开始安装相应发行版本 Cron"
        yum install vixie-cron crontabs >> panyubus.log 2>&1
        chkconfig --level 345 crond on
        service crond start
    fi
    pip install requests >> panyubus.log 2>&1
fi

# 打印日志
echo " " >> panyubus.log
date >> panyubus.log
echo "----------------------------------------------------" >> panyubus.log
python3 panyubus.py
# python3 panyubus.py >> panyubus.log 2>&1
