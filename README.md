# PanYuBus  
监控广州番禺地区的部分公交车位置，以及提供相关的生活服务

1. 每天早上7点启动程序，运行 itchat，并通过邮件发送登录二维码到本机  
2. 本机授权登录，itchat 发送通知给我，告诉我下一趟 番68 在哪，估计还有多久达到

**PS:** 第一次安装请删除 *panyubus.log* 文件！！！  
**PSS:** 请尽量使用 Python3 ！

crontab:
#### 每个工作日早上 6:30 分启动程序  
```
    30 6 * * 1,2,3,4,5 ~/start.sh
```

#### 相关文档：  
>[Crontab 简单实现树莓派语音闹钟](https://zhuanlan.zhihu.com/p/34195493)  
http://h5.thecampus.cc/api/v1/search?name=1

ps:
12/28
bus_comming.si = 783482