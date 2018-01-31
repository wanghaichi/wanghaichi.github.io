---
layout: article
title: 【软件测试】记录几个曾经遇到的坑
date: 2017-02-26 23:34:01
tags: 软件测试作业
categories: 作业
---

- [php中过滤函数的编码问题](#htmlspecialchars)
- [mysql不经过滤直接拼接的问题](#mysql)
---
<h2 id='htmlspecialchars'>php中过滤函数的编码问题</h2>
问题发生的背景是整理服务器，将一部分php5的代码迁移到php7的服务器上。
> If omitted, the default value of the encoding varies depending on the PHP version in use. In 5.6 and later, the default_charset configuration option is used as the default value. PHP 5.4 and 5.5 will use UTF-8 as the default. Earlier versions of PHP use ISO-8859-1.

这是官方的文档，能看到在php5.6之前与之后
```
string htmlspecialchars ( string $string [, int $flags = ENT_COMPAT | ENT_HTML401 [, string $encoding = ini_get("default_charset") [, bool $double_encode = true ]]] )
```
这个函数的默认编码变了，使得当在php5.6之后的版本，该函数无法对编码格式为gbk的进行过滤。需要显示定义 `string $encoding = ini_get("default_charset")`这个参数。

---
<h2 id='mysql'>mysql不经过滤直接拼接的问题</h2>
这个则是蠢得不行不行的bug，懂点的人都知道mysql如果直接拼接字符串会导致各种注入问题。
比如：
```
$id = $_GET['id'];//获取id
$where = " where id ='" . $id . "'";
$result = getByWhere('specialnews', $where);
```
只要人家输入个 `"AND 1 = 1"` 之类的，就血崩。
然后使用mysqli函数族中的 `real_escape_string()` 过滤一下就好了

---
最后，挽尊。
