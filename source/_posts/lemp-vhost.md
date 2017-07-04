layout: article
title: Nginx 本地虚拟主机搭建
date: 2017-03-13 23:34:02
tags:
- Nginx
- Vhost
categories: 个人日志
---
# Nginx 本地虚拟主机搭建
之前每次都死在这里，这把终于搞明白了。
弄个虚拟主机的目的是将多个项目都可以跑在虚拟域名的根目录下，在本地调试结构也比较清晰。

---
首先备份一份 default 配置文件
```
$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
```
接下来以example.com域名为例
```
$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/example.com.conf
```
修改新的配置文件的内容
```

server {
	listen 80;
	listen [::]:80;
	server_name example.com;
	root /var/www/example.com;
	index index.html index.php;
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
这里你需要有对应的工作目录，将配置文件链接到 `sites-enabled` 中使其生效
下面这里要注意了，一定要写绝对路径。
```
$ sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
$ sudo systemctl reload nginx
```
在hosts文件中加上映射
```
$ vi /etc/hosts
127.0.0.1 example.com
$ sudo /etc/init.d/networking restart
```
去浏览器访问 example.com 就可以看到对应的网页了

---
之前每次貌似都是在做链接那里死了，因为只要用相对路径，链接不上，也不知道为什么。
挽尊
