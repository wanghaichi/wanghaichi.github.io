---
layout: article
title: Vagrant ： Windows下开发小助手，告别双系统
date: 2017-05-17 03:29:56
tags:
- 虚拟机
- Vagrant
categories: 个人日记
---

# Vagrant ： Windows下开发小助手，告别双系统
不知道广大程序员们是怎么处理 Windows 和 Linux 的，最开始在 Windows 下面跑 Linux 的虚拟机，卡的自己怀疑人生。后来做了个双系统，自己 250 的固态表示根本不够用，而且动不动关机重启，别问我为什么，毕竟 office 割舍不了。后来一个学长点了我一下，既然想用 Linux 搞事情，用什么图形化界面，搞个服务器不就好了。然后我就搞了个腾讯云，然而，网络不好的时候真的蛋疼。最后，在宁哥大腿的指引下，尝试了一下 Vagrant 虚拟机，快的飞起，果断放弃双系统。

这里记录一些自己在搭建 Vagrant 环境时的步骤以及踩的坑。

提前准备：
- [Vagrant](https://www.vagrantup.com/)
- [VirtureBox](https://www.virtualbox.org/wiki/Downloads)

首先，我们要选择一个适合我们的 box 也就是操作系统。Vagrant 提供了许多 box 供我们使用：[Vagrant Box](https://atlas.hashicorp.com/boxes/search) 。这里，海痴选择的是 ubuntu16.04。

那么，当我们装好了 Vagrant，VirtureBox，并且下载好所需要的box以后，就可以开始搞事情了。当然，为了接下来的发展更加顺利，强烈建议装一个 Git ，毕竟 Git bash 异常的好用。

我们新建一个文件夹，命名为 ubuntu，并且将我们的 box 移到这个目录下。在这个目录打开命令行界面，添加box
```
$ vagrant box add xenial-server-cloudimg-amd64-vagrant.box
```
添加后的 box 可以使用 `vagrant box list` 来查看
更多的 vagrant 操作，可以参考这篇博客 [使用 Vagrant 打造跨平台开发环境](https://segmentfault.com/a/1190000000264347)

接下来，运行 `vagrant up` 来启动这个虚拟机。这是一个漫长的过程，如果你使用 Windows 命令行，可能会更慢。

![Picture](/images/2017-05-17-11-28.png)

细心地你如果打开 VirtureBox，会发现那里已经有一个虚拟机躺着啦

这个时候，我们的名为 ubuntu 的文件夹里面会多几个文件，其中 Vagrantfile 是 Vagrant 虚拟机的配置文件，这个先不用管，以后再说。

此时我们可以通过 ssh 的方式连接虚拟机，Windows 可以使用 PuTTy，当然，我们的 Git bash 帮我们准备好了这些。打开终端（Git bash），执行 `vagrant ssh` ，怎么样，是不是看到了一个闪闪发亮的 Linux！

![Picture](/images/2017-05-17-11-29.png)

接下来的配置大家就可以按需进行拉，和 Vagrant 就没有太大关系了。当然，有一些配置是需要注意的。

#### Vagrant 端口转发
在 Vagrantfile 配置文件中，取消以下几行的注释
```
config.vm.network "forwarded_port", guest: 3306, host: 4567
config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
config.vm.network "private_network", ip: "192.168.33.10"
```
该命令可以将虚拟机的端口与本机的端口进行对应，当然，根据需要可以进行更多的端口转发，其中第三行，可以不进行端口转发，直接通过 ip 地址访问虚拟机。

#### Vagrant 共享文件夹
```
config.vm.synced_folder "../../../data/whc_web", "/vagrant_data"
```
意图很清晰，这也是 Vagrant 虚拟机非常好用的一点，可以在主机使用 IDE 进行写码，然后在虚拟机中运行。配合下面的预执行SHELL脚本效果更佳

#### Vagrant 预执行脚本
```
  config.vm.provision "shell", inline: <<-SHELL
    rm /var/www/html -rf
    ln -s /vagrant_data /var/www/html
  SHELL
```
  在执行 `vagrant up` 指令时会执行，可根据需要自定义，不过需要注意的是需要有对应目录的权限，对于 lemp 开发环境的同学，将 /var/www/html 设置成根目录，并调整对应权限，把项目代码放着这里即可

#### 通过主机连接 Vagrant MySQL 数据库
安装 MySQL 就不多说了，安装之后需要配置一下
 MySQL 的配置文件 `my.cnf`
海痴的 `my.cnf` 实际上引用的配置文件在 `/etc/mysql/mysql.conf.d/mysqld.cnf` 修改以下行
```
# bind-address = 127.0.0.1
bind-address = 0.0.0.0
```
重启 MySQL 服务就可以了

#### 通过 PuTTy ssh 连接Vagrant
网上说的默认账号密码都是 `vagrant` 然而我的账号是 `ubuntu` 密码是空，然而 ssh 是不允许无密码访问的。所以需要先设置 ubuntu 账户的密码，才可以正常访问。

#### 设置 hexo 博客时出现的 npm install 的问题
由于 npm 安装时需要与外部建立软链，而 Windows 只有管理员才可以进行此操作，所以需要使用管理员模式打开命令行界面才可以

其余的遇到问题不断更新吧

反正我以后不用来回切换系统了啊哈哈哈哈
