---
layout: article
title: hexo 设置相册、主页并使用七牛云加速图片加载
date: 2018-02-07 15:23:00
tags: 
- hexo
categories: 个人日记
img: /images/2018-02-07-15-28-heart.jpg
---

据换完博客主题之后也有一段时间了，但总觉得哪里不对的样子，别人家都是主页和博客分开的，或者把博客放在主页的子目录下，而自己的却只有一个博客，反正自己也有域名，为什么不整个单独的主页出来呢。

这篇文章记录了海痴是如何在 google 上扒模版，如何利用 travis 来将博客的内容同步到主页上，又如何与某涛互相比较，解决图片加载慢的问题。

我们可以看看最终的效果：https://www.liebes.top

在一切开始之前，海痴已经准备好了用 hexo 搭建起来的博客，一个自己的域名，以及使用 travis 将博客部署到自己的服务器的脚本。可以参见上一篇博客：[Hexo 更换 materail 主题，使用 Travis 持续集成](https://blog.liebes.top/2018/01/25/hexo-material/)

## 一份靠谱的主页模板

关于如何找到一份高端上档次的主题模板，大家可以各显神通，当然，最快的还是 google 上搜一下：“主页 模板 bootstrap”，请一定加上 bootstrap 这个关键字，因为经过实践，这样搜出的结果最靠谱。

准备好之后，就可以将模板文件放在博客的根目录下，随便起个名字，就像这样：

```
├── _config.yml
├── db.json
├── liebes.top <- 这个是模板文件
├── liebes.top.py <- 这个是之后会用到的脚本文件
├── node_modules
├── package-lock.json
├── package.json
├── public
├── pyyaml
├── scaffolds
├── source
├── themes
└── travis.enc
```

根据你的需要来修改你的主页模板。

## 动态获取博客内容，嵌入主页中

如果你希望你的主页上显示一些你的个人动态，你就要动一番手脚了。

一个简单的办法，就是使用 php 做个后台支持，这并不难。

海痴希望将自己最近写的博客显示在主页上，同时显示一些相册里面的照片。一个简单的思路，就是读取博客目录中的静态文件，提取内容，找出时间相近的部分，使用脚本文件对 html 进行替换。

于是我的 `index.html` 文件就变成了这个样子：

```Html
<section class="swag text-center">
  <div class="container">
    <div class="row">
      <div class="col-md-8 col-md-offset-2">
        <h1>我共写了 {count} 篇博客<span>记录生活，记录点滴</span></h1>
        <a href="#portfolio" class="down-arrow-btn"><i class="fa fa-chevron-down"></i></a>
      </div>
    </div>
  </div>
</section>
<section class="portfolio text-center section-padding" id="portfolio">
  <div class="container">
    <div class="row">
      <div id="servicesSlider" class="hidden-sm hidden-xs">
        <ul class="slides">
          {articles}
        </ul>
      </div>
        <div id="servicesSlider2" class="hidden-md hidden-lg">
            <ul class="slides">
                {articles2} <- 这个是适配小屏幕的
            </ul>
        </div>
    </div>
  </div>
</section>
```

我将需要替换的部分用 `{var}` 来标记，为之后的脚本文件作准备。

由于最近在弄机器学习相关的东西，python 使用的比较多，就顺手用 python 写的脚本。

```python
import os
import re
import yaml

imgCdnPath = "http://p3q6bdexg.bkt.clouddn.com"
imgRule_ori = "?imageMogr2/thumbnail/600x/blur/1x0/quality/75"
imgRule_webp = "?imageMogr2/thumbnail/600x/format/webp/blur/1x0/quality/75|imageslim"
imgPath = "https://blog.liebes.top"
useCdn = True

def convert_md(filePath):
	file = open(filePath, 'r')
	content = file.read()
	pattern = re.compile(r'---([\s\S]*)---\n([\s\S]*)')
	content = re.search(pattern, content)
	prefix = content.group(1)
	main = content.group(2)
	pattern = re.compile(r'[-`#\s]')
	# print(prefix)
	main = re.sub(pattern, "", main)
	mLen = min(len(main), 250)
	main = main.decode('utf-8')[0:mLen].encode('utf-8')

	pattern = re.compile(r'title:( *)(.*?)( *)\n')
	title = re.search(pattern, prefix).group(2)
	pattern = re.compile(r'date:( *)(.*?)( *)\n')
	date = re.search(pattern, prefix).group(2)
	pattern = re.compile(r'img:( *)(.*?)( *)\n')
	img = ""
	try: 
		img = (imgPath, imgCdnPath)[useCdn] + re.search(pattern, prefix).group(2) + ("", imgRule_ori)[useCdn]
	except:
		img = "img/portfolio-01.jpg"
	webSite = "https://blog.liebes.top"
	url = date[0:10]
	url = url.replace("-", "/")
	basename = os.path.basename(filePath)
	basename = os.path.splitext(basename)[0]

	return {
		'title': title,
		'date' : date,
		'main' : main,
		'url'  : webSite + "/" + url + "/" + basename,
		'src'  : img
	}

def change_html(html_path, mdList, totalCount):

	html = ""
	html2 = ""
	s = ""
	template = ""

	with open(os.getcwd() + "/source/_data/li-article.html", "r") as file:
		template = file.read()

	for idx, item in enumerate(mdList):
		tem = template
		tem = tem.replace("{title}", item['title'])
		tem = tem.replace("{url}", item['url'])
		tem = tem.replace("{content}", item['main'])
		tem = tem.replace("{src}", item['src'])
		s = s + tem
		html2 = html2 + "<li>" + tem + "</li>"
		if idx % 3 == 2:
			s = "<li>" + s + "</li>"
			html = html + s
			s = ""
	content = ""
	with open(html_path, 'r') as file:
		content = file.read()
	content = content.replace("{articles}", html)
	content = content.replace("{count}", str(totalCount))
	content = content.replace("{articles2}", html2)
	with open(html_path, 'w') as file:
		file.write(content)

def convert_links(filePath):
	links = {}
	template = ""
	html = ""
	html2 = ""
	with open(filePath + "/links.yaml", 'r') as file:
		links = yaml.load(file)
	
	with open(filePath + "/li-links.html", "r") as file:
		template = file.read()

	s = ""
	for idx, k in enumerate(links):
		tem = template
		tem = tem.replace("{link}", links[k]["link"])
		tem = tem.replace("{pic}", links[k]["avatar"])
		tem = tem.replace("{desc}", links[k]["descr"])
		tem = tem.replace("{name}", k)
		html2 = html2 + "<li>" + tem + "</li>"
		s = s + tem
		if idx % 3 == 2:
			s = "<li>" + s + "</li>"
			html = html + s
			s = ""
	if s != "":
		s = "<li>" + s + "</li>"
		html = html + s
		s = ""

	content = ""
	with open(os.getcwd() + "/liebes.top/index.html", "r") as file:
		content = file.read()

	content = content.replace("{links}", html.encode("utf-8"))
	content = content.replace("{links2}", html2.encode("utf-8"))

	with open(os.getcwd() + "/liebes.top/index.html", "w") as file:
		file.write(content)

def convert_gallery(filePath):
	links = {}
	template = ""
	html = ""
	html2 = ""
	with open(filePath + "/gallery.yaml", 'r') as file:
		links = yaml.load(file)
	
	with open(filePath + "/li-gallery.html", "r") as file:
		template = file.read()

	s = ""
	for idx, k in enumerate(links):
		tem = template
		tem = tem.replace("{src}", "%s"%(links[k]["full_link"]))
		#tem = tem.replace("{src}", "%s%s%s"%((imgPath, imgCdnPath)[useCdn], links[k]["full_link"], ("", imgRule_ori)[useCdn]))
		s = s + tem
		html2 = html2 + "<li>" + tem + "</li>"
		if idx % 2 == 1:
			s = "<div class=\"col-md-4 wp4\">" + s + "</div>"
			html = html + s
			s = ""
		if idx == 5:
			break
	if s != "":
		s = "<div class=\"col-md-4 wp4\">" + s + "</div>"
		html = html + s
		s = ""
	html = "<li>" + html + "</li>"
	content = ""
	with open(os.getcwd() + "/liebes.top/index.html", "r") as file:
		content = file.read()

	content = content.replace("{gallery}", html.encode("utf-8"))
	content = content.replace("{gallery2}", html2.encode("utf-8"))
	with open(os.getcwd() + "/liebes.top/index.html", "w") as file:
		file.write(content)

baseDir = os.getcwd()
mds = os.listdir(baseDir + "/source/_posts")
totalCount = len(mds)

mdList = []
for md in mds:
	md = baseDir + "/source/_posts" + "/" + md
	turple = convert_md(md)
	mdList.append(turple)
	
mdList = sorted(mdList, key = lambda item: item['date'], reverse=True)
mdList = mdList[0:6]

change_html(baseDir + "/liebes.top/index.html", mdList, totalCount)
convert_links(baseDir + "/source/_data")
convert_gallery(baseDir + "/source/_data")
```

这份 python 文件引用了 pyyaml 这个依赖包，所以需要先安装一下。

```
 - git clone https://github.com/yaml/pyyaml.git
 - cd pyyaml
 - sudo python setup.py install
```

具体的做法就是使用正则读取出文章最开始的数据信息，比如时间、标题等等，然后去对 html 做替换。不详说，有问题可以在评论区提问。

## Travis 脚本修改

本着程序员一切从简的心态，当把项目提交到 github 上之后，就应该完成一切的部署操作，于是适当修改Travis 脚本

 ```
before_install:
  - git clone https://github.com/yaml/pyyaml.git
  - cd pyyaml
  - sudo python setup.py install
  - cd ..
  ...
script:
  - python liebes.top.py
  - rsync -az -vv --delete -e 'ssh' liebes.top/ root@www.liebes.top:/var/www/www
  ...
 ```

当然，这需要你在服务器上提前配置好 nginx 

## 图片加载加速

在我美滋滋的弄完所有的工作之后，下一个问题困扰了我：网站加载慢。如果你也是使用的阿里云最低配的服务器，你也一定会遇到这个问题。图片加载慢带来的连锁反应就是 js 的执行会等待 DOM 加载完毕，于是刚打开网站的时候就会有一种网站烂掉的错觉。

七牛云可以提供免费的对象存储服务，有免费的 10G 可以使用。

https://portal.qiniu.com 七牛云网址

实名认证后可以创建对象存储资源，创建好之后在 `内容管理 -> 上传文件` 上传你的文件，之后就可以使用外链进行访问了。

请一定继续将图片传到你的 git 仓库中，因为如果某一天加速服务取消了，你的图片就不见了。

这样折腾完，基本上页面加载速度会在 5s 内搞定



最后吐槽一句，写完 python 写其他语言，出现的错误基本都是没写分号 ：）