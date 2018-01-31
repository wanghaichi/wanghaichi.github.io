---
layout: article
title: laravel的学习日常-初识
date: 2017-03-20 00:24:17
tags:
- laravel
categories: 个人日记
---

记录记录自己踩过的坑

---
按照官方文档，乖乖的用composer进行安装：
```
$ composer global require "laravel/installer"
```
然后，就给我报了噼里啪啦一堆错误
```

  [Composer\Downloader\TransportException]                                     
  The "https://packagist.org/packages.json" file could not be downloaded: fai  
  led to open stream: Connection timed out                                     

```
EXM？我还啥也没干呢啊 = =。
然后吧，我就把这个错误扔到了google上，注意了注意了，划重点了！搜出来解决方案的没有一个可以用的！然后我发现只是单纯的被墙了而已。
WHAT THE FUCK !!!
解决办法也挺简单，把composer的源切成国内镜像就好了
```
$ composer config -g repo.packagist composer https://packagist.phpcomposer.com
```
具体的可以参见 [Packagist / Composer 中国全量镜像](https://pkg.phpcomposer.com/) 这里。
接下来就可以愉快的使用laravel了
```
$ composer global require "laravel/installer"
```
使用laravel新建一个项目，然后就可以看到牛逼闪闪的lavavel的目录结构：
```
$ laravel new myProject
```
![pictures](/images/2017-3-20-15-16.png)
