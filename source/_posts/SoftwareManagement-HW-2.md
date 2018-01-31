---
layout: article
title: Jenkins 安装与使用
date: 2017-04-14 15:55:26
tags: 软件项目管理作业
categories: 作业
---

Jenkins旨在编程的持续继承，测试部署自动化，官方给的简介如下：
> Jenkins is a self-contained, open source automation server which can be used to automate all sorts of tasks such as building, testing, and deploying software. Jenkins can be installed through native system packages, Docker, or even run standalone by any machine with the Java Runtime Environment installed.

首先下载 Jenkins 的war包
[jenkins.war](http://mirrors.jenkins.io/war-stable/latest/jenkins.war)
运行命令
```
$ java -jar jenkins.war
```
该命令会在本地的8080端口运行jenkins
访问 `localhost:8080` 会看到jenkins 的欢迎界面，按照步骤依次进行设置。
在安装插件的界面，选择默认即可，jenkins会帮你安装一些常见的插件，比如git，pipeline等
设置结束后会看到如下界面
![pictures](/images/2017-4-24-14-7.png)
点击左上角新建按钮，即可新建一个项目，这里我们选择新建一个maven项目。在github project选项上选择我们的github地址
![pictures](/images/2017-04-24-14-26.png)
在源码管理设置上选择git，并设置默认编译的分支为主分支
![pictures](/images/2017-04-24-14-28.png)
在构建触发器设置上，选择Poll SCM 并在日程表里面输入`* * * * *`表示每一分钟就会执行依次构建
![pictures](/images/2017-04-24-14-30.png)
在构建的位置，选择新增一个shell 并输入`mvn test`
![pictures](/images/2017-04-24-14-34.png)
点击保存后即可
此后每一次将代码更新到github之后，jenkins会自动进行检测，同时在每次构建时会自动进行测试。在Consloe Output中可以看到测试结果
![pictures](/images/2017-04-24-14-42.png)
![pictures](/images/2017-04-24-14-43.png)
