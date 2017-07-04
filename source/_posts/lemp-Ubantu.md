layout: article
title: Unbuntu16.04 Nginx + php + mysql Web服务器搭建
date: 2017-03-10 23:34:00
tags:
- Nginx
- web server
- Lemp
categories: 个人日记
---
# Unbuntu16.04 Nginx + php + mysql Web服务器搭建
下决心不再用lamp的集成包了，自己搞一个出来。
- [Nginx](#nginx)
- [php](#php)
- [mysql](#mysql)
---
<h2 id='nginx'>Nginx</h2>
首先安装使用 apt 安装nginx
$ sudo apt install nginx
然而由于之前安装过nginx，卸载还不干净，导致配置文件读取失败，出现错误：
```
Job for nginx.service failed because the control process exited with error code. See "systemctl status nginx.service" and "journalctl -xe" for details.
invoke-rc.d: initscript nginx, action "start" failed.
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: failed (Result: exit-code) since 四 2017-03-09 00:06:13 CST; 7ms ago
  Process: 4540 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=1/FAILURE)
3月 09 00:06:13 hardy-Inspiron-5547 systemd[1]: Starting A high performance....
3月 09 00:06:13 hardy-Inspiron-5547 nginx[4540]: nginx: [emerg] open() "/etc...
3月 09 00:06:13 hardy-Inspiron-5547 nginx[4540]: nginx: configuration file /...
3月 09 00:06:13 hardy-Inspiron-5547 systemd[1]: nginx.service: Control proc...1
3月 09 00:06:13 hardy-Inspiron-5547 systemd[1]: Failed to start A high perf....
3月 09 00:06:13 hardy-Inspiron-5547 systemd[1]: nginx.service: Unit entered....
3月 09 00:06:13 hardy-Inspiron-5547 systemd[1]: nginx.service: Failed with ....
Hint: Some lines were ellipsized, use -l to show in full.
dpkg: 处理软件包 nginx-core (--configure)时出错：
 子进程 已安装 post-installation 脚本 返回错误状态 1
dpkg: 依赖关系问题使得 nginx 的配置工作不能继续：
 nginx 依赖于 nginx-core (>= 1.10.0-0ubuntu0.16.04.4) | nginx-full (>= 1.10.0-0ubuntu0.16.04.4) | nginx-light (>= 1.10.0-0ubuntu0.16.04.4) | nginx-extras (>= 1.10.0-0ubuntu0.16.04.4)；然而：
  软件包 nginx-core 尚未配置。
  未安装软件包 nginx-full。
  未安装软件包 nginx-light。
  未安装软件包 nginx-extras。
 nginx 依赖于 nginx-core (<< 1.10.0-0ubuntu0.16.04.4.1~) | nginx-full (<< 1.10.0-0ubuntu0.16.04.4.1~) | nginx-light (<< 1.10.0-0ubuntu0.16.04.4.1~) | nginx-extras (<< 1.10.0-0ubuntu0.16.04.4.1~)；然而：
  软件包 nginx-core 尚未配置。
  未安装软件包 nginx-full。
  未安装软件包 nginx-light。
  未安装软件包 nginx-extras。
dpkg: 处理软件包 nginx (--configure)时出错：
 依赖关系问题 - 仍未被配置
在处理时有错误发生：
 nginx-core
 nginx
E: Sub-process /usr/bin/dpkg returned an error code (1)
```
在报错信息中可以看到配置文件读取失败，当然这个错误也有可能是因为apache占用了80端口
```
# 如果是apache占用端口的话
$ systemctl stop apache2
# 如果是东西没删干净的话，我的问题是这个
$ sudo apt-get purge nginx nginx-common nginx-full
```
解决之后启动nginx服务，并设置开机启动
```
# 输入完，在本地打 127.0.0.1 已经可以访问了，然而在设置开机启动的时候又炸了
$ systemctl start nginx
$ systemctl enable nginx
```
然而自家系统又报错了：
```
Synchronizing state of nginx.service with SysV init with /lib/systemd/systemd-sysv-install...
Executing /lib/systemd/systemd-sysv-install enable nginx
sh: 0: getcwd() failed: No such file or directory
insserv: pushd() can not change to directory /etc/init.d: No such file or directory
update-rc.d: error: insserv rejected the script header
```
结果原因是因为我当前的工作目录已经被删除了，所以……
成功后，访问 127.0.0.1 会看到nginx的欢迎界面
![pictures](/images/welcomeToNginx.png)
---
<h2 id='php'>编译安装PHP7</h2>
首先下载php7的源码：[链接](http://php.net/get/php-7.0.9.tar.gz/from/a/mirror)然后安装需要的依赖
```
$ sudo apt-get update
$ sudo apt-get install libxml2-dev
# 安装gcc
$ sudo apt-get install build-essential
$ sudo apt-get install openssl
$ sudo apt-get install libssl-dev
$ sudo apt-get install make
$ sudo apt-get install curl
$ sudo apt-get install libcurl4-gnutls-dev
$ sudo apt-get install libjpeg-dev
$ sudo apt-get install libpng-dev
$ sudo apt-get install libmcrypt-dev
$ sudo apt-get install libreadline6 libreadline6-dev
```
解压下载好的php文件
```
$ sudo tar -zxf /tmp/php-7.0.9.tar.gz
$ cd php-7.0.9
```
编译安装（这里需要好一会儿时间）
```
$ sudo ./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php/etc --enable-fpm --with-fpm-user=www --with-fpm-group=www --with-mysqli --with-pdo-mysql --with-iconv-dir --with-freetype-dir --with-jpeg-dir --with-png-dir --with-zlib --with-libxml-dir=/usr --enable-xml --disable-rpath --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --with-curl --enable-mbregex --enable-mbstring --with-mcrypt --enable-ftp --with-gd --enable-gd-native-ttf --with-openssl --with-mhash --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-soap --without-pear --with-gettext --disable-fileinfo --enable-maintainer-zts
$ sudo make && sudo make install
```
安装结束后，需要配置一下php的配置文件
```
$ cd /usr/local/php/etc
$ sudo cp php-fpm.conf.default php-fpm.conf
$ cd /usr/local/php/etc/php-fpm.d
$ sudo cp www.conf.default www.conf
# 打开www.conf文件可以看到 user 和 group 默认设置为 www
# 如果www用户不存在，那么先添加www用户
$ sudo groupadd www
$ sudo useradd -g www -s /bin/nologin www
```
在 `/etc/profile` 文件末尾加上：
```
PATH=$PATH:/usr/local/php/bin
export
# 输入
$ source /etc/profile
```
验证php安装情况并启动
```
$ php -v
$ sudo /usr/local/php/sbin/php-fpm
```
配置nginx配置与php配置
```
# 我们可以发现/usr/local/php/etc 下面是没有php.ini文件的，这个文件可以在你的源码目录下找到，有个 php.ini.development 的文件
$ sudo cp php.ini.development /usr/local/php/etc/php.ini
# 打开ini文件，作如下修改
cgi.fix_pathinfo=0
# 修改nginx配置文件 /etc/nginx/sites-available/default
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html index.php;
	server_name server_domain_or_IP;
	location / {
		try_files $uri $uri/ =404;
	}
	location ~ \.php$ {
		include snippets/fastcgi-php.conf;
		fastcgi_pass 127.0.0.1:9000;
	}
	location ~ /\.ht {
		deny all;
	}
}
```
重新启动 nginx 并测试
```
$ sudo systemctl reload nginx
$ sudo vi /var/www/html/test.php
<?php
    echo phpinfo();
?>
```
![picture](/images/phpinfo.png)
---
<h2 id='mysql'>安装MYSQL</h2>
通过 apt 安装mysql，根据提示自定义mysql
```
$ sudo apt-get install mysql-server
```
---
至此，lemp的环境就搭建完了，下一篇文章海痴会搞一搞 vhost
