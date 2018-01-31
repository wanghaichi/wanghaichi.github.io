---
layout: article
title: 在CentOS7上搭建ftp服务器
date: 2017-01-17 23:34:00
tags: ftp
categories: 个人日记
---

在ninge的帮助下，终于搞出了ftp服务器，记下来以后用

- [ftp服务器搭建](#ftp)
- [sftp服务器搭建](#sftp)
- [用户权限设置](#useradd)
- [啰嗦几句](#other)

---
<h2 id='ftp'>ftp服务器搭建</h2>
首先安装sftp服务
```
[root@hardy ~]# yum install vsftpd
```
修改配置文件，在修改配置文件之前记得备份
```
[root@hardy ~]# cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.bak
[root@hardy ~]# vim /etc/vsftpd/vsftpd.conf
```
vsftpd服务有许多配置，这里不一一赘述，将一些常用的写出来
```
#匿名用户是否可以登录
anonymous_enable=YES
#允许系统用户名登录
local_enable=YES
#允许使用任何可以修改文件系统的FTP的指令，禁用这项则用户无法修改
write_enable=YES
#本地用户新建文件的掩码
local_umask=022
#开启日志功能
xferlog_enable=YES
#日志文件位置
xferlog_file=/var/log/vsftpd.log
#这三项设置chroot，用来限制用户只能访问家目录，这三项一会详说。
chroot_local_user=YES
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list
```
修改以下配置
```
anonymous_enable=NO
chroot_local_user=YES
#以下需要手动添加
allow_writeable_chroot=YES
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40100
```
启动vsftpd服务，并设置开机启动
```
[root@hardy ~]# systemctl restart vsftpd.service
[root@hardy ~]# systemctl enable vsftpd.service
```
Centos7以后使用firewall防火墙，因此需要设置开放端口，如果没有防火墙请忽略，使用iptables也可以，开放20和21端口即可
```
[root@hardy ~]# firewall-cmd --permanent --add-service=ftp
[root@hardy ~]# firewall-cmd --reload
[root@hardy ~]# setsebool -P ftp_home_dir on
```
添加个用户，并设置无法登录
```
[root@hardy ~]# useradd -m ftptest -s /sbin/nologin
[root@hardy ~]# passwd ftptest
```
然后就可以使用浏览器或者ftp连接工具连接了，会进入默认的/home/ftptest文件夹

---
<h2 id='sftp'>ftp服务器搭建</h2>
一般的服务器都会有ssh服务的，要是没有的话安装一下
```
[root@hardy ~]# yum -y install openssh-server
```
为了方便管理ftp用户，需要建立一个ftp用户组
```
[root@hardy ~]# groupadd ftpusers
```
打开ssh配置文件 /etc/ssh/sshd_config 并作如下修改
```
#Subsystem      sftp    /usr/libexec/openssh/sftp-server
Subsystem       sftp    internal-sftp
Match group ftpusers
ChrootDirectory %h
X11Forwarding   no
AllowTcpForwarding no
ForceCommand internal-sftp
```
重启ssh服务
```
[root@hardy ~]# systemctl restart sshd
```
至此，sftp服务搭建完毕。不过刚刚创建的用户是不能访问的，由于还没有设置用户组。
为了更加方便的管理ftp用户，需要对相关用户设置相应的权限。

---
<h2 id='useradd'>用户权限设置</h2>
为刚刚创建的用户添加用户组
```
[root@hardy ~]# usermod -g ftpusers ftptest
```
chroot要求该用户的家目录的所有者是root，并且不具有写权限
```
[root@hardy ~]# chown root /home/ftptest
[root@hardy ~]# chmod 750 /home/ftptest
```
这样用户通过ftptest登入后无法上传或者下载，建立文件夹www，设置所有者及用户组
```
[root@hardy ~]# mkdir /home/hardy/www
[root@hardy ~]# chown hardy:ftpusers /home/hardy/www
```
这样就可以在www文件夹下进行上传和下载了

---
<h2 id='other'>啰嗦几句</h2>
我们往往需要设置两个ftp账号，一个能够上传下载，另一个只能下载而不能上传。
只需要修改相应的权限即可
只能下载的用户不具有写权限就可以了

---
参考文章：[Setup FTP server on centos 7(VSFTP)](http://www.krizna.com/centos/setup-ftp-server-centos-7-vsftp/)
