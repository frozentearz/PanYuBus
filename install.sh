#!/bin/bash

echo "#初始化程序 ......"
result=$(lsb_release -a | tr 'A-Z' 'a-z')

# RedHat 系列
redhat="redhat"
centos="centos"
fedora="fedora"

# Debian 系列
ubuntu="ubuntu"
debian="debian"

echo "正在检测系统发行版本......"
if [[ $result =~ $ubuntu || $result =~ $debian ]]; then
    echo "检测完成，您的系统为："
    echo $result
    echo "开始安装相应发行版本 Cron"
    apt-get install cron -y >> panyubus.log 2>&1
    service cron start
    echo "正在添加计划任务..."
    echo "30 6 * * 1,2,3,4,5 python3 main.py >> panyubus.log 2>&1" >> /etc/crontab
    service cron restart
    echo "Cron 计划任务添加完成......\n正在安装 Python3"
    apt-get install python3 >> panyubus.log 2>&1
    apt-get install pip3 >> panyubus.log 2>&1
    echo "正在安装 Python 依赖库......"
    pip3 install requests itchat requests_toolbelt
    echo "所有依赖安装完成！"
elif [[ $result =~ $redhat || $result =~ $centos || $result =~ $fedora ]]; then
    echo "检测完成，您的系统为："
    echo $result
    echo "开始安装相应发行版本 Cron"
    yum install vixie-cron crontabs >> panyubus.log 2>&1
    chkconfig --level 345 crond on
    service crond start
    echo "正在添加计划任务..."
    echo "30 6 * * 1,2,3,4,5 python3 main.py >> panyubus.log 2>&1" >> /etc/crontab
    echo "Cron 计划任务添加完成......\n正在安装 Python3"
    yum install python3 -y >> panyubus.log 2>&1
    yum install pip3  >> panyubus.log 2>&1
    echo "正在安装 Python 依赖库......"
    pip3 install requests itchat requests_toolbelt
    echo "所有依赖安装完成！"
else 
    echo "找不到相关发行版本！"
fi