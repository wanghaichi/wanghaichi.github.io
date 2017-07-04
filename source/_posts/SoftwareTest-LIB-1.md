layout: article
title: 【软件测试】JUNIT使用及覆盖测试
date: 2017-03-10 23:34:01
tags: 软件测试上机实验
categories: 上机实验
---
# 【软件测试】JUNIT使用及覆盖测试
软件测试第一次上机，测试了一下JUnit的使用和覆盖测试，虽然实验要求是用eclipse，但我还是被idea的美色所臣服。
- [Junit 安装与使用](#junit)
- [覆盖测试](#cover)
---
<h2 id='junit'>Junit 安装与使用</h2>
首先去官网下载Junit的jar包和其依赖
> [junit-4.12.jar](http://search.maven.org/#search|gav|1|g:"junit" AND a:"junit")

> [hamcrest-core-1.3.jar](http://search.maven.org/#search|ga|1|g%3Aorg.hamcrest)

打开Idea，新建一个项目，并在项目中与src目录平级创建test和lib文件夹，并将下载的jar包放在lib文件夹中
![pictures](/images/2017-3-10-11-55.png)
在idea中导入junit：`File>Project Structure>Modules` 点击 ‘+’ 引入刚刚下载的jar包，点击 Apply
![pictures](/images/2017-3-10-12-00.png)
将test文件夹设置为测试文件夹
在test文件夹右键 > Mark Directory as > Test Resources Root
回到Main.java 编写testTriangle方法
```
//判断一个三角形的形状：等边，等腰，普通
public static String testTriangle(int a, int b, int c){
    if(a < 0 || b < 0 || c < 0)
        return "illegal input";
    else if (a + b <= c || a + c <= b || b + c <= a)
        return "illegal input";
    else if (a == b && b == c)
        return "equilateral";
    else if (a == b || b == c)
        return "isosceles";
    else
        return "scalene";
}
```
Ctrl + Shift + T 或者 Navigate > Test 选择 Creat New Test 成功后会在test目录下生成test类
修改testTriangle方法
```
@Test
    public void testTriangle() throws Exception {
        a = 1;
        b = 2;
        c = 3;
        assertEquals("illegal input", Main.testTriangle(a, b, c));
        a = 2;
        b = 5;
        c = 5;
        assertEquals("isosceles", Main.testTriangle(a, b, c));
        a = 5;
        b = 5;
        c = 5;
        assertEquals("equilateral", Main.testTriangle(a, b, c));
        a = 5;
        b = 6;
        c = 7;
        assertEquals("scalene", Main.testTriangle(a, b, c));
    }
```
Ctrl + Shift + F10 运行测试，得到运行结果
![pictures](/images/2017-3-10-17-57.png)
---
<h2 id='cover'>覆盖测试</h2>
作业要求的是使用Eclemma，然而Eclemma是Eclipse的插件，idea继承了覆盖测试
Run > Run ‘Main’ with Coverage
![pictures](/images/2017-3-10-18-03.png)
---
就这些啦，挽尊。
