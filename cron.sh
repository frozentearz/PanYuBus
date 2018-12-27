#!/bin/bash

######################################
######################################
####                              ####
####      Cron 自动安装脚本        ####
####                              ####
######################################
######################################

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