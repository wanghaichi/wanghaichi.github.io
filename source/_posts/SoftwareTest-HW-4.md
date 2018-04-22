---
layout: article
title: 【软件测试】JAVA PATH FINDER [JPF]
date: 2017-04-08 15:07:09
tags: 软件测试作业
categories: 作业
---

软件测试小组作业之JPF

首先先说说JPF是个什么东西

官方给出的解释：
> JPF核心是用于Java™字节码的虚拟机（VM），这意味着它是一个程序，您可以让Java程序执行。它用于在这些程序中找到缺陷，因此您还需要给出属性以作为输入进行检查。 JPF通过一份报告来回复，该报告说如果属性持有和/或由JPF创建的验证工件进行进一步分析（如测试用例）。

> JPF是一个有几个扭曲的虚拟机。它在Java本身中实现，所以不要指望它像您的普通Java一样快速运行。它是在VM上运行的VM。虽然Java字节码的执行语义在http://java.sun.com/docs/books/jvms/second_edition/html/VMSpecTOC.doc.html/ Sun的Java虚拟机规范中有明确定义，但我们在JPF中几乎没有硬连线语义 - VM指令集由一组可被替换的类表示。

> 默认指令集使用下一个JPF功能：执行选项。 JPF可以识别您的程序中的执行可能不同的进程，然后系统地探索所有这些点。这意味着JPF（理论上）通过程序执行所有路径，而不仅仅是像普通的VM那样。典型的选择是不同的调度序列或随机值，但JPF可以再次介绍您自己的类型，如用户输入或statemachine事件。

个人觉得JPF是一个针对JAVA程序寻找可执行路径的工具。看了一下官方的例子，觉得JPF可以在JAVA程序执行时自动检测所有的可执行路径，找到可能出现问题的路径。不同于传统的基于用例的Testing，JPF采用的是Model Checking，尽管基于用例的测试在用例足够多的时候有着很不错的测试效果，但是很难保证测试到所有的可行路径。JPF官方给出了基于测试用例的Testing 与 Model Testing 的差别：[testing_vs_model_checking](http://babelfish.arc.nasa.gov/trac/jpf/wiki/intro/testing_vs_model_checking)

那么说说JPF安装的方式，JPF安装需要使用一个类似于git的管理工具：Mercurial，同时需要JUNIT，与Apache ant。
安装之前我们需要先下载Mercuial 和 ant
```
$ sudo apt install Mercurial
$ sudo apt install ant
```
由于我使用的IDE是 idea ,自带了JUNIT的包，没有的需要去下载一下。
需要将JUNIT包的目录加入到环境变量中
```
$ sudo vi /etc/provile
export JUNIT_HOME=/home/hardy/app/idea-IU-163.13906.18/lib
export CLASSPATH=.:$CLASSPATH:$JUNIT_HOME/junit-4.12.jar
$ source /etc/provile
```
使用Mercuial下载jpf-core的仓库
```
$ hg clone http://babelfish.arc.nasa.gov/hg/jpf/jpf-core
$ cd jpf-core
$ ant test
```
成功后会提示安装成功
```
BUILD SUCCESSFUL
Total time: 3 minutes 53 seconds
```

新建一个JAVA类，测试jpf
```java
# Racer.java
public class Racer implements Runnable {
    int d = 42;
    public void run () {
        doSomething(1000);                   // (1)
        d = 0;                               // (2)
    }
    public static void main (String[] args){
        Racer racer = new Racer();
        Thread t = new Thread(racer);
        t.start();

        doSomething(1000);                   // (3)
        int c = 420 / racer.d;               // (4)
        System.out.println(c);
    }
    static void doSomething (int n) {
        // not very interesting..
        try { Thread.sleep(n); } catch (InterruptedException ix) {}
    }
}
```
在同一目录下建立Racer.jpf，写入jpf的配置信息
```
# Racer.jpf
target = Racer

listener=gov.nasa.jpf.listener.PreciseRaceDetector

report.console.property_violation=error,trace
​```
上述配置能够输出jpf的工作栈
此程序正常的输出应为10
然而由于我们不知道线程的调度关系，因而忽略了可能导致的除0的问题
```
$ ~/jpf-core/bin/jpf Racer.jpf
# output

JavaPathfinder core system v8.0 (rev 32) - (C) 2005-2014 United States Government. All rights reserved.


====================================================== system under test
Racer.main()

====================================================== search started: 17-4-10 下午4:21
10
10

====================================================== error 1
gov.nasa.jpf.listener.PreciseRaceDetector
race for field Racer@15b.d
  main at Racer.main(Racer.java:35)
		"int c = 420 / racer.d;               // (4)"  READ:  getfield Racer.d
  Thread-1 at Racer.run(Racer.java:26)
		"d = 0;                               // (2)"  WRITE: putfield Racer.d


====================================================== trace #1
------------------------------------------------------ transition #0 thread: 0
gov.nasa.jpf.vm.choice.ThreadChoiceFromSet {id:"ROOT" ,1/1,isCascaded:false}
      [3157 insn w/o sources]
  Racer.java:30                  : Racer racer = new Racer();
  Racer.java:19                  : public class Racer implements Runnable {
      [1 insn w/o sources]
  Racer.java:21                  : int d = 42;
  Racer.java:30                  : Racer racer = new Racer();
  Racer.java:31                  : Thread t = new Thread(racer);
      [145 insn w/o sources]
  Racer.java:31                  : Thread t = new Thread(racer);
  Racer.java:32                  : t.start();
      [1 insn w/o sources]
------------------------------------------------------ transition #1 thread: 0
gov.nasa.jpf.vm.choice.ThreadChoiceFromSet {id:"START" ,1/2,isCascaded:false}
      [2 insn w/o sources]
  Racer.java:34                  : doSomething(1000);                   // (3)
  Racer.java:41                  : try { Thread.sleep(n); } catch (InterruptedException ix) {}
      [4 insn w/o sources]
------------------------------------------------------ transition #2 thread: 1
gov.nasa.jpf.vm.choice.ThreadChoiceFromSet {id:"SLEEP" ,2/2,isCascaded:false}
      [1 insn w/o sources]
  Racer.java:1                   : /*
  Racer.java:25                  : doSomething(1001);                   // (1)
  Racer.java:41                  : try { Thread.sleep(n); } catch (InterruptedException ix) {}
      [4 insn w/o sources]
------------------------------------------------------ transition #3 thread: 1
gov.nasa.jpf.vm.choice.ThreadChoiceFromSet {id:"SLEEP" ,2/2,isCascaded:false}
      [3 insn w/o sources]
  Racer.java:41                  : try { Thread.sleep(n); } catch (InterruptedException ix) {}
  Racer.java:42                  : }
  Racer.java:26                  : d = 0;                               // (2)
------------------------------------------------------ transition #4 thread: 0
gov.nasa.jpf.vm.choice.ThreadChoiceFromSet {id:"SHARED_OBJECT" ,1/2,isCascaded:false}
      [3 insn w/o sources]
  Racer.java:41                  : try { Thread.sleep(n); } catch (InterruptedException ix) {}
  Racer.java:42                  : }
  Racer.java:35                  : int c = 420 / racer.d;               // (4)
------------------------------------------------------ transition #5 thread: 0
gov.nasa.jpf.vm.choice.ThreadChoiceFromSet {id:"SHARED_OBJECT" ,1/2,isCascaded:false}
  Racer.java:35                  : int c = 420 / racer.d;               // (4)

====================================================== results
error #1: gov.nasa.jpf.listener.PreciseRaceDetector "race for field Racer@15b.d   main at Racer.main(Ra..."

====================================================== statistics
elapsed time:       00:00:00
states:             new=9,visited=1,backtracked=4,end=2
search:             maxDepth=6,constraints=0
choice generators:  thread=8 (signal=0,lock=1,sharedRef=2,threadApi=3,reschedule=2), data=0
heap:               new=362,released=33,maxLive=357,gcCycles=7
instructions:       3424
max memory:         119MB
loaded code:        classes=62,methods=1477

====================================================== search finished: 17-4-10 下午4:21

```

可以看到jpf帮我们运行了所有可能的路径，同时找到了可能发生的错误
通过线程的角度来考虑，可以用官网给出的这个调度图来说明：
![pictures](/images/interleavings.png)
对于一个多线程的java程序，jpf会组合出所有的可能的线程调度，并顺序遍历每一种执行顺序，知道找到可能存在的缺陷