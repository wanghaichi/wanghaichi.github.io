---
layout: article
title: 编辑器带来的XSS漏洞问题解决方案
date: 2017-07-11 20:47:08
tags:
- editor
- xss
categories: 个人日记
---

接上一篇编辑器的使用，自己尝试着写了一段js代码，本以为laravel的

```
{{ $item }}
```

渲染可以完美的避免 XSS 的攻击（确实可以避免），但是由于 Editor 生成的时候，重新渲染了一遍，导致了可能出现的XSS漏洞。

![Pic](/images/2017-7-11-20-51.png)

![Pic](/images/2017-7-11-20-52.png)

可以看到，Editor已经帮助我们做了html的编码，于是我觉得不需要进行二次编码，就直接存到了数据库里，并且直接在前端进行了渲染。

Controller

```php
$res = Notification::updateById($notice_id, [
                'content'   => $content,
                'title'     => $title,
                'fileName'  => $file_name,
                'filePath'  => $file_path
            ]);
```
view

```html
<textarea id="editor" name="editor" rows="10" cols="80">
    {{ $notice['content'] }}
</textarea>
```

看起来一点问题也没有对不对！！

然而当渲染的时候缺弹出了一个框框······

![Pic](/images/2017-7-11-21-02.png)

查看代码发现变成了整个样子

![Pic](/images/2017-7-11-21-03.png)

哇，说好的前端渲染可以防止XSS呢！！！

在鹏鹏的帮助下，发现了原因，尽管我们在 editor 中输入的恶意代码经过了转义，但是Editor会在Dom加载完成后再进行一次渲染，导致第一次加载Dom时，被转义过的 html entity 被解析成了正确的字符，而Editor重新获取这些解析后的内容，再一次输出到了界面上，导致了最后的恶意代码执行。

于是我在后台处理的时候进行了一次转义

Controller

```php
$res = Notification::updateById($notice_id, [
                'content'   => htmlspecialchars($content),
                'title'     => $title,
                'fileName'  => $file_name,
                'filePath'  => $file_path
            ]);
```

这一次解决了当前的问题，恶意代码以字符形式显示了出来

![Pic](/images/2017-7-11-21-14.png)

然而，有一种东西叫做 Postman，在这里的输入可不会乖乖的向Editor一样帮你做好转义

Ok，你跟我说laravel 有 csrftoken 保护，但理论上是可以完全模拟浏览器请求的（虽然我不会）

于是我采取了这样的方法，删掉你的 Editor ，没错就是这么暴力，只在Dom树里面留下Textarea的东西

![Pic](/images/2017-7-11-21-29.png)

于是，该死的注入又出现了

![Pic](/images/2017-7-11-21-33.png)

查看代码发现转义又失效了，MMP！！！

![Pic](/images/2017-7-11-21-34.png)

其实原因也很简单，最开始成功的原因是我们假设之前的恶意代码已经被转义一次了，那么由于Editor的机制，我们只需要进行二次转义就可以了。但是，这一次恶意代码没有像我们想的那样经过了转义。

那在渲染的时候再转义一次不就好了，哼唧

于是我又修改了我的view代码，现在Controller和view看起来是这个样子的：


Controller

```php
$res = Notification::updateById($notice_id, [
                'content'   => htmlspecialchars($content),
                'title'     => $title,
                'fileName'  => $file_name,
                'filePath'  => $file_path
            ]);
```

View

```html
 {!! htmlspecialchars($notice['content']) !!}
```

这下总万事大吉了吧，结果

![Pic](/images/2017-7-11-21-42.png)

WTF？？？？？？？？？？？？

好吧，我自己作死转义了两次，恶意代码是防住了，正常代码也被干掉了。

好吧我承认其实从这里开始才是有用的东西

在第一次转义的时候避免二次转义，第二次转义正常转义，可以完美的解决这个问题

Controller
```php
$res = Notification::updateById($notice_id, [
      // 防止编辑器xss攻击，这里进行转义，同时避免二次编码
      'content'   => htmlspecialchars($content, ENT_COMPAT | ENT_HTML401, ini_get("default_charset") , false),
      'title'     => $title,
      'fileName'  => $file_name,
      'filePath'  => $file_path
]);
```

View
```html
 {!! htmlspecialchars($notice['content']) !!}
```

好了，世界安静了，去**的XSS。
