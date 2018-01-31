---
layout: article
title: hexo 使用git备份hexo源文件
date: 2017-03-17 15:29:17
tags:
- hexo
categories: 个人日记
---
这是个悲伤的故事，海痴的linux出了点毛病，然后就想着重装一遍。掐指一算，自家的代码在git上面都保存了，直接重装！
然后吧，hexo你大爷，你没事就不能把博客原文备份一下么？又不占你的空间！那么费劲么！
是的，海痴的博客都没了，别问我为什么还能看着，宝宝复制粘贴都快吐了，弄到凌晨两点多才恢复了。
这件事情告诉我们，没事闲的别重装系统。

---
具体的思路就是在我们的博客仓库中新建一个分支，用来保存源码，master分支用来提交hexo自动生成的文件。以海痴的博客为例。打开wanghaichi.github.io工作目录，我们可以喜闻乐见的发现没有.git文件夹。那么接下来的事情就简单了
打开工作目录，执行以下操作
```
$ git init
$ vi .gitignore
.DS_Store
Thumbs.db
db.json  
*.log
.deploy*/
node_modules/
.npmignore
public/
$ git branch -b hexo
$ git add .
$ git commit -m "backup"
$ git remote add origin git@github.com:wanghaichi/wanghaichi.github.io.git
$ git push origin hexo
```
如果没设置ssh权限可能需要设置一下，然后去github仓库里面切换以下分支，你的可爱的博客就都在里面啦。
以后每次写完博客，先执行一遍
```
$ git add .
$ git commit -m "backup"
$ git push origin hexo
```
再发布，就不用担心自家博客丢失啦

---
妈妈再也不用担心复制博客到零点啦
