---
layout: article
title: Ubuntu16.04 配置JAVA环境、搭建tomcat环境、安装php-java-bridge工具
date: 2017-01-17 23:34:00
tags: java
categories: 个人日记
---

- [下载安装jdk](#jdk)
- [配置JAVA环境变量](#javahome)
- [搭建tomcat环境](#tomcat)
- [安装php-java-bridge工具](#java-bridge)
---
<h2 id='jdk'>下载安装jdk</h2>
首先去Oracle官网下载jdk安装包：[下载地址](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)根据系统版本选择要下载的安装包，海痴选择的是 [jdk-8u111-linux-x64.tar.gz](http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.tar.gz)下载后解压
```
$ tar -xzvf jdk-8u111-linux-x64.tar.gz
```
在/opt下创建java目录，并将解压后的文件夹移动到java目录下
```
$ sudo mkdir /opt/java
$ sudo mv jdk1.8.0_111 /opt/java
```
---
<h2 id='javahome'>配置JAVA环境变量</h2>
修改 /etc/profile 文件，在文件尾添加如下内容
```
$ sudo vim /etc/profile
export JAVA_HOME=/opt/java/jdk1.8.0_111
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
```
使其生效，注意使用zsh的童鞋，需要在 .zshrc 上也加上上述的配置
```
$ sudo source /etc/profile
```
测试是否成功
```
$ java -version
java version "1.8.0_111"
Java(TM) SE Runtime Environment (build 1.8.0_111-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.111-b14, mixed mode)
```
---
<h2 id='tomcat'>搭建tomcat环境</h2>
去官网下载tomcat [下载链接](http://tomcat.apache.org/download-90.cgi)
海痴用的是 [apache-tomcat-9.0.0.M15.tar.gz](http://apache.fayea.com/tomcat/tomcat-9/v9.0.0.M15/bin/apache-tomcat-9.0.0.M15.tar.gz)解压，将解压后的文件夹移动到 /opt 下
```
$ tar -xzvf apache-tomcat-9.0.0.M15.tar.gz
$ sudo mv tomcat /opt
```
修改 /opt/tomcat/bin/startup.sh ，添加以下内容（与上文配置java环境的时候一致）。注意要在最后一行之前添加
```
$ sudo vim /opt/tomcat/bin/startup.sh
export JAVA_HOME=/opt/java/jdk1.8.0_111
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
export TOMCAT_HOME=/opt/tomcat
```
启动即可
```
$ sudo /opt/tomcat/bin/startup.sh      
Using CATALINA_BASE:   /opt/tomcat
Using CATALINA_HOME:   /opt/tomcat
Using CATALINA_TMPDIR: /opt/tomcat/temp
Using JRE_HOME:        /opt/java/jdk1.8.0_111/jre
Using CLASSPATH:       /opt/tomcat/bin/bootstrap.jar:/opt/tomcat/bin/tomcat-juli.jar
Tomcat started.
```
访问 https://localhost:8080 将显示tomcat的欢迎界面。如果失败了请查看环境变量时候配置正确，8080端口是否被占用。
检查端口占用情况，如果被占用关掉相应进程即可
```
$ netstat -apn | grep <端口号>
```
---
<h2 id='java-bridge'>安装php-java-bridge工具</h2>
去官网下载安装包 [下载链接](http://php-java-bridge.sourceforge.net/pjb/download.php)
海痴下载的是：[JavaBridgeTemplate621.war](http://sourceforge.net/projects/php-java-bridge/files/Binary%20package/php-java-bridge_6.2.1/JavaBridgeTemplate621.war/download)将下载的文件放到tomcat的webapps目录下，并重新启动tomcat
```
$ sudo cp  JavaBridgeTemplate621.war /opt/tomcat/webapps/
$ sudo /opt/tomcat/bin/startup.sh
```
此时在webapps目录下会有名为JavaBridgeTemplate621的文件夹，将此文件夹移到apache目录下即可使用
具体使用方法
首先关闭tomcat服务器，然后运行JavaBridge.jar文件
```
$ java -jar JavaBridge/WEB-INF/lib/JavaBridge.jar SERVLET:8080 &
Jan 17 17:20:20 JavaBridge INFO : VM                  : 1.8.0_111@http://java.oracle.com/
Jan 17 17:20:20 JavaBridge INFO : JavaBridge version             : 6.2.1    
Jan 17 17:20:20 JavaBridge INFO : logFile             :
Jan 17 17:20:20 JavaBridge INFO : default logLevel    : 3
Jan 17 17:20:20 JavaBridge INFO : socket              : SERVLET:8080
Jan 17 17:20:20 JavaBridge INFO : java.ext.dirs       : /opt/java/jdk1.8.0_111/jre/lib/ext:/usr/java/packages/lib/ext
Jan 17 17:20:20 JavaBridge INFO : php.java.bridge.base: /home/hardy
Jan 17 17:20:20 JavaBridge INFO : thread pool size    : 20
Jan 17 17:20:20 JavaBridge INFO : JavaBridgeRunner started on port INET:8080
```
新建 test.php 文件，输入以下内容
```
<?php
  require_once("JavaBridge/java/Java.inc");
  $system = java("java.lang.System");
  echo "Java version=".$system->getProperty("java.version");
?>
```
测试成功！（注意 test.php 与 JavaBridge文件夹的位置）
如果提示没有权限打开文件，奖JavaBridge文件夹内的文件修改成755权限即可
```
$ chmod 755 -R JavaBridge
```
具体JavaBridge的用法边学边写吧
