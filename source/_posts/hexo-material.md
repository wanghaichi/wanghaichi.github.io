---
layout: article
title: Hexo 更换 materail 主题，使用 Travis 持续集成
date: 2018-01-25 18:27:00
tags: 
- hexo-theme
categories: 个人日记
---

是的，我折腾了一天把博客的模版换了一下。怎么说呢，之前用的Next主题，很简约，看起来也很舒服，但总觉得少点什么，后来逛了逛其他人的站，感觉Next主题没有图，视觉上没什么冲击力，灰蒙蒙的感觉，于是采用了 material 这个主题，也很简洁，相比之下色彩丰富一些。

之前在使用 github pages 有一些不爽的地方就是地址不是自己的域名，然而宝宝是买了域名的，为什么要在 github 下弄呢，之前尝试过使用CNAME进行域名解析，但是在处理 https 的问题上比较麻烦，想着弄一套 CI流程出来。试过 hexo 的 deploy 插件，用 rsync 进行自动部署，然而未果，各种奇怪的问题弄的头痛。最近心血来潮 google 一番，发现好多人都在用Travis CI 来自动化部署，于是尝试了一下，效果很不错。

大致整理整理安装的过程吧，在阅读下面的文字之前，你需要自己安装过一次hexo，并了解hexo。

## HEXO MATERIAL 主题更换

从 github 上下载 material 主题：[https://github.com/viosey/hexo-theme-material](https://github.com/viosey/hexo-theme-material) 下载 release 或者直接克隆项目均可，将主题包移动到 hexo 项目的 theme 中并修改博客配置文件 `_config.yml`

```
theme: material
```

此时运行  `hexo s` 在本地就可以预览到 material 主题的样式了。接下来的步骤，完全可以按照官方的教程一项一项设置，不要嫌麻烦，因为很多特性默认都是没有的，需要自己去打开。

官方文档：https://material.viosey.com/docs/#/

下面记录的是一些在安装时需要注意的地方，请先阅读一遍官方文档，再接着进行