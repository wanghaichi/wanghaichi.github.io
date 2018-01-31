---
layout: article
title: 【软件测试】Selenium Web 测试
date: 2017-03-26 17:08:07
tags: 软件测试上机实验
categories: 上机实验
---

Selenium 用于WEB程序测试，可以录制下来点击过程的脚本，并自动进行测试。

- [使用selenium-ide 进行脚本录制](#ide)
- [使用java编写selenium程序，实现自动验证](#selenium-java)

---
<h2 id='ide'>使用selenium-ide 进行脚本录制</h2>
在开始实验之前，需要安装所需要的软件。首先想要使用selenium-ide，需要是用firefox浏览器。
[firefox下载链接](https://www.mozilla.org/zh-CN/firefox/new/)
[selenium-ide下载链接](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)
将下载后的selenium插件拖到firefox里即可自动安装。
成功安装后，在firefox中可以打开selenium插件:
选择开发者工具中的selenium-ide
![Pictures](/images/2017-3-26-21-22.png)
打开后长这个样子
![Pictures](/images/2017-3-26-21-27.png)
在1的位置输入想要测试的网址，接着点击2位置的按钮开始录制。去浏览器访问对应的网站，完成表单提交操作，回到selenium-ide会看到录制下来的case，最后点击4,会将当前所有的case执行一遍。

---

<h2 id='selenium-java'>使用java编写selenium程序，实现自动验证</h2>
新建一个java项目，然后导入下列jar包

- [selenium-server-standalone-3.3.1.jar](http://selenium-release.storage.googleapis.com/3.3/selenium-server-standalone-3.3.1.jar)
- [selenium-java-3.3.1.zip](http://selenium-release.storage.googleapis.com/3.3/selenium-java-3.3.1.zip)

导入成功后需要下载firefox的驱动：
[geckodriver-v0.15.0-linux64.tar.gz](https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz)

以上就是全部的准备工作了
新建一个项目，在main方法中写如下代码:
```java
import java.io.*;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import com.csvreader.*;

public class Main {

    public static void main(String[] args){


        //定义测试的根目录
        String baseUrl = "http://121.193.130.195:8080";
        // 创建webdriver对象
        System.setProperty("webdriver.gecko.driver", "geckodriver");
        WebDriver driver = new FirefoxDriver();
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);

        try{
            //读取csv文件
            File inFile = new File("inputgit.csv");
            BufferedReader reader = new BufferedReader(new FileReader(inFile));
            CsvReader csvreader = new CsvReader(reader,',');
            //每次读取一行
            while(csvreader.readRecord()){
                String str = csvreader.getRawRecord();
                String[] strList = str.split(",");

                //使用webdriver模拟登录，并获取信息
                driver.get(baseUrl + "/");
                driver.findElement(By.id("name")).clear();
                driver.findElement(By.id("name")).sendKeys(strList[0]);
                driver.findElement(By.id("pwd")).clear();
                driver.findElement(By.id("pwd")).sendKeys(strList[0].substring(4));
                driver.findElement(By.id("submit")).click();
                String temp = strList[0];
                strList[0] = strList[1];
                strList[1] = temp;
                //获取特定验证信息
                String[] targetGitUrl = driver.findElement(By.id("resultString")).getAttribute("innerHTML").trim().split(",");
                boolean flag = true;
                for(int i = 0; i < 3; i ++){
                    if(!strList[i].equals(targetGitUrl[i])){
                        flag = false;
                        break;
                    }
                }
                //验证失败
                if(!flag){
                    System.out.println("Error: \n" + strList[0] + " " + strList[1] + " " + strList[2]);
                    System.out.println(targetGitUrl[0] + " " + targetGitUrl[1] + " " + targetGitUrl[2]);
                }
            }
            driver.quit();
        } catch (IOException e){
            e.printStackTrace();
        }
    }
}
```
运行即可
完整的项目在github上：[selenium-web-test](https://github.com/wanghaichi/selenium-web-test)

---
挽尊
