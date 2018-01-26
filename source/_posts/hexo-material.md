---
layout: article
title: Hexo 更换 materail 主题，使用 Travis 持续集成
date: 2018-01-25 18:27:00
tags: 
- hexo-theme
categories: 个人日记
---

是的，我折腾了一天把博客的模版换了一下。怎么说呢，之前用的 Next 主题，很简约，看起来也很舒服，但总觉得少点什么，后来逛了逛其他人的站，感觉 Next 主题没有图，视觉上没什么冲击力，灰蒙蒙的感觉，于是采用了 material 这个主题，也很简洁，相比之下色彩丰富一些。

之前在使用 github pages 有一些不爽的地方就是地址不是自己的域名，然而宝宝是买了域名的，为什么要在 github 下弄呢，之前尝试过使用CNAME进行域名解析，但是在处理 https 的问题上比较麻烦，想着弄一套 CI流程出来。试过 hexo 的 deploy 插件，用 rsync 进行自动部署，然而未果，各种奇怪的问题弄的头痛。最近心血来潮 google 一番，发现好多人都在用Travis CI 来自动化部署，于是尝试了一下，效果很不错。

大致整理整理安装的过程吧，在阅读下面的文字之前，你需要自己安装过一次hexo，并了解hexo。

## HEXO MATERIAL 主题更换

从 github 上下载 material 主题：[https://github.com/viosey/hexo-theme-material](https://github.com/viosey/hexo-theme-material) 下载 release 或者直接克隆项目均可，将主题包移动到 hexo 项目的 theme 中并修改博客配置文件 `_config.yml`

```
theme: material
```

此时运行  `hexo s` 在本地就可以预览到 material 主题的样式了。接下来的步骤，完全可以按照官方的教程一项一项设置，不要嫌麻烦，因为很多特性默认都是没有的，需要自己去打开。

官方文档：https://material.viosey.com/docs/#/

下面记录的是一些在安装时需要注意的地方，请先阅读一遍官方文档，再接着进行。

**关于首页icon**

有一个好的 icon 可以让博客看上去美观很多，这里推荐一个网站，有很多不错的图，而且可以DIV。

https://www.canva.com/

**关于侧边栏icon**

最开始默认的侧边栏只有主页和归档，看着空唠唠的。如果你按照文档进行，应该会将标签云、分类、时间轴等等都加上，但是对应的 icon 又不能空着，可以去这里找相应的 icon

https://material.io/icons/

**关于相册**

这个功能可能是我最喜欢的了，可以将一些生活上的照片放进来，但是会有一些问题。

首先是图片大小的问题，太大的图片会让这个单叶奇卡无比，随意在上传图片之前强烈建议进行压缩，或者使用一些图片CDN加速。

然后就是相册对竖版图片支持的并不好，尽量传横板吧，期待作者的更新

**关于第三方服务**

material 主题内嵌了很多第三方支持，按照文档，去对应的第三方网站注册就行。评论的第三方支持我用的畅言，虽然想用disqus，但是考虑到国内的大墙，还是算了。



## 使用 TRAVIS CI 持续集成

这个可以说阅读了好多好多博客了，这里就不再抄一遍别人家的了

https://segmentfault.com/a/1190000009054888

这篇博客里面讲的就很详尽了，下面记录一些自己遇到的问题

**关于gem 安装travis报错**

这个一般是 ruby 版本或者依赖的问题，ubuntu 下我安装了下面几个依赖

```
- ruby-dev
- gcc
- libffi-dev
- make
```

macOS 下直接更新了 ruby 就可以了

```
brew update
brew install ruby
```

**关于服务器谜钥认证**

基本原理是将你电脑的 ssh 谜钥加密传到 travis 上去，在进行服务器连接时 travis 对谜钥进行解密，然后接下来的流程就跟使用 ssh 谜钥访问主机的方法一样了。

按照博客上面的方法，会要求将你本地的默认ssh 谜钥  `~/.ssh/id_rsa` 加密传上去，但这就会带来一个问题，一般为了安全，都会给谜钥设置一个口令，但是 CI 中没法让你输入口令。解决办法也很简单，只需要新生成一个谜钥，`ssh-keygen -f ~/.ssh/travis` 这样就会自动生成一个新的私钥和公钥，将公钥写到服务器的 `authorized_keys` 里面，上传的时候将新生成的私钥加密传到仓库即可。

在部署脚本里面，建议将解密后的秘要以默认的形式 `~/.ssh/id_rsa` 保存，虽然在 rsync 过程中可以使用 `ssh -i ~/.ssh/travis` 来制定具体使用的谜钥，但在实践部署中总是提示找不到文件，具体可以参见 [.travis.yml](https://github.com/wanghaichi/wanghaichi.github.io/blob/hexo/.travis.yml)

上面的部署脚本建议不要拿过来直接用，如果你的 hexo 中开启了其他的组件，记得在部署脚本里面安装。

最后，如果你的博客还没有备份，请一定去备份一下。你一定会发现我的 git 仓库又两个分支，CI的触发分支是 hexo 而不是 master。教程链接： [hexo 使用git备份hexo源文件](/2017/03/17/hexo-backup/)

