layout: article
title: 网络安全学习-1
date: 2017-05-10 14:32:43
categories: 安全
tags:
- 网络安全
- XSS
---

# 网络安全学习之浏览器安全

最近在看《白帽子讲WEB安全》这本书，按着章节记录一下实践和学习的过程。

### 同源策略
> 简单来说，同源策略限制了来自不同源的“document”或脚本，对当前“document”读取或设置某些属性

同源的网站指起host地址是一致的

比如以下几个地址
1. http://store.company.com/dir2/index.html
2. http://store.company.com/dir1/index.html
3. https://store.company.com/dir1/index.html
4. http://store.company.com:8080/dir2/index.html
5. http://news.company.com/dir1/index.html

其中1,2是同源的，而其他几个则不是。

对于一个网页中加载的javascript资源而言，其域是当前打开的页面

比如在a.com中引用了b.com中的文件
```
<script src="http://b.com/b.js"></script>
```
其中b.js的源是a.com而非b.com

### XSS简介

跨站脚本攻击，全称是 Cross Site Script。XSS攻击通常指黑客通过“Html 注入”篡改了网页，插入恶意的脚本，从而在浏览网页时，控制用户浏览器的一种攻击。

#### 反射型XSS

反射型XSS只是简单地把用户输入的数据“反射”给浏览器，也就是说，黑客需要诱使用户点击一个恶意链接，才能攻击成功。反射型XSS也叫做“非持久型CSS”（Non-persistent XSS）

#### 储存型XSS

储存型XSS会把用户输入的数据“储存”在服务器端。这种XSS具有很强的稳定性。

#### DOM Based XSS

DOM Based XSS 从本质上来说也是反射型XSS。单独划分出来是因为DOM Based XSS的形成原因比较特别。通过修改页面的DOM节点形成的XSS，称之为DOM Based XSS。
