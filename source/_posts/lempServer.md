---
layout: article
title: Centos 7 Nginx + php + mysql Web服务器搭建
date: 2017-01-21 23:34:00
tags:
- Nginx
- web server
- Lemp
categories: 个人日记
---

- [安装Nginx](#nginx)
- [安装php5](#php5)
- [安装php7](#php7)
- [安装mysql](#mysql)
---
<h2 id='nginx'>搭建nginx服务</h2>
在所有工作之前，先更新一下yum咯
```
$ yum install yum
$ yum -y update
```
然后使用yum安装nginx
```
# 如果没有nginx包尝试使用下面的命令添加
$ yum install epel-release
$ yum install nginx
# 启动
$ systemctl start nginx
# 开机自启
$ systemctl enable nginx
```
然后就可以在浏览器输入`http://127.0.0.1`，会看到nginx的欢迎界面，如果是远程服务器请输入以下命令查看ip
```
$ ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
# 或者
$ curl http://icanhazip.com
```
---
<h2 id='php5'>安装php5</h2>
使用yum安装，十分简单。
```
$ yum install php php-mysql php-fpm
```
安装完成后，修改 `/etc/php.ini` 文件，找到 `cgi.fix_pathinfo=0` 这一行，取消注释并修改成0
然后修改 `/etc/php-fpm.d/www.conf` 文件，需要修改一下几个地方
```
listen = /var/run/php-fpm/php-fpm.sock
listen.owner = nobody
listen.group = nobody
user = nginx
group = nginx
```
然后启动就可以啦
```
$ systemctl start php-fpm
$ systemctl enable php-fpm
```
---
<h2 id='php7'>安装php7</h2>

php7的安装就需要编译安装了
首先下载php7
```
$ wget -O php7.tar.gz http://cn2.php.net/get/php-7.0.4.tar.gz/from/this/mirror
$ tar -xvf php7.tar.gz
$ cd php-7.0.4
```
在编译之前需要安装php7需要的依赖：
```
yum install libxml2 libxml2-devel openssl openssl-devel bzip2 bzip2-devel libcurl libcurl-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel gmp gmp-devel libmcrypt libmcrypt-devel readline readline-devel libxslt libxslt-devel
```
然后编译，当然需要提前安装c族 ``$ yum install gcc`
```
./configure \
--prefix=/usr/local/php \
--with-config-file-path=/etc \
--enable-fpm \
--with-fpm-user=nginx  \
--with-fpm-group=nginx \
--enable-inline-optimization \
--disable-debug \
--disable-rpath \
--enable-shared  \
--enable-soap \
--with-libxml-dir \
--with-xmlrpc \
--with-openssl \
--with-mcrypt \
--with-mhash \
--with-pcre-regex \
--with-sqlite3 \
--with-zlib \
--enable-bcmath \
--with-iconv \
--with-bz2 \
--enable-calendar \
--with-curl \
--with-cdb \
--enable-dom \
--enable-exif \
--enable-fileinfo \
--enable-filter \
--with-pcre-dir \
--enable-ftp \
--with-gd \
--with-openssl-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib-dir  \
--with-freetype-dir \
--enable-gd-native-ttf \
--enable-gd-jis-conv \
--with-gettext \
--with-gmp \
--with-mhash \
--enable-json \
--enable-mbstring \
--enable-mbregex \
--enable-mbregex-backtrack \
--with-libmbfl \
--with-onig \
--enable-pdo \
--with-mysqli=mysqlnd \
--with-pdo-mysql=mysqlnd \
--with-zlib-dir \
--with-pdo-sqlite \
--with-readline \
--enable-session \
--enable-shmop \
--enable-simplexml \
--enable-sockets  \
--enable-sysvmsg \
--enable-sysvsem \
--enable-sysvshm \
--enable-wddx \
--with-libxml-dir \
--with-xsl \
--enable-zip \
--enable-mysqlnd-compression-support \
--with-pear \
--enable-opcache
```
接下来需要
```
$ make && make install
```
修改环境变量，在 `/etc/profile` 文件中最后加上以下内容
```
PATH=$PATH:/usr/local/php/bin
export PATH
```
保存后使其生效
```
$ source /etc/profile
```
$ source /etc/profile安装成功后需要配置fpm
```
$ cp php.ini-production /etc/php.ini
$ cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
$ cp /usr/local/php/etc/php-fpm.d/www.conf.default /usr/local/php/etc/php-fpm.d/www.conf
$ cp sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
$ chmod +x /etc/init.d/php-fpm
```
然后就是各种秘制配置了
这里要注意上面的配置的路径
首先修改 `/usr/local/php/etc/php-fpm.d/www.conf`
```
listen = 127.0.0.1:9000
listen.owner = nobody
listen.group = nobody
user = nginx
group = nginx
```
然后修改 `php.ini` 文件
查看刚刚配置的命令，可以看到`php.ini`文件位置是： `/etc/php.ini` 找到 `cgi.fix_pathinfo` 并修改为0
```
cgi.fix_pathinfo=0
```
然后重新启动php-fpm
```
$ /etc/init.d/php-fpm restart
```
接下来需要配置nginx对php文件的解析
注意这里对于php5和php7的配置是稍有不同的
修改 `/etc/nginx/conf.d/default.conf` 文件，海痴的Centos有毒，修改的是 `/etc/nginx/nginx.conf` 文件，作如下修改
```
server {
    listen       80;
    server_name  server_domain_name_or_IP;
    # note that these lines are originally from the "location /" block
    root   /usr/share/nginx/html;
    index index.php index.html index.htm;
    location / {
        try_files $uri $uri/ =404;
    }
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
    location ~ \.php$ {
        try_files $uri =404;
        #php5:
        #fastcgi_pass unix:/var/run/php-fpm/php-fpm.sock;
        #php7:
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```
然后重新启动nginx服务就可以了
```
$ systemctl restart nginx
```
此时可以去nginx的工作目录下，边写phpinfo文件进行测试
---
<h2 id='mysql'>安装mysql(mariadb)</h2>
简单粗暴2333333
```
$ yum install mariadb-server mariadb
$ systemctl start mariadb
$ mysql_secure_installation
```
然后就按照提示进行就可以咯，给root设置一个密码，其他的没什么特别需要就一直点下去就可以了。
然后，就没有然后了。
