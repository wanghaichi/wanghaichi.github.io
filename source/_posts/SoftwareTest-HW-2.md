layout: article
title: 【软件测试】作业2 设计测试用例
date: 2017-02-26 23:34:02
tags: 软件测试作业
categories: 作业
---
#【软件测试】作业2 设计测试用例
软件测试课程作业，按照要求设计相关的测试用例
- [问题描述](#problem)
- [问题解答](#answer)
---
<h2 id='problem'>问题描述</h2>
> Below are two faulty programs. Each includes a test case that results in failure. Answer the following questions about each program.
> ```
// program 1
public int findLast (int[] x, int y) {
//Effects: If x==null throw NullPointerException
// else return the index of the last element
// in x that equals y.
// If no such element exists, return -1
  for (int i=x.length-1; i > 0; i--){
    if (x[i] == y){
      return i;
    }
  }
  return -1;
}
// test: x=[2, 3, 5]; y = 2
// Expected = 0
```
> ```
// program 2
public static int lastZero (int[] x) {
// Effects: if x==null throw NullPointerException
// else return the index of the LAST 0 in x.
// Return -1 if 0 does not occur in x
  for (int i = 0; i < x.length; i++){
    if (x[i] == 0){
      return i;
    }
  }
  return -1;
}
// test: x=[0, 1, 0]
// Expected = 2
```

#### Questions
- Identify the fault.
- If possible, identify a test case that does not execute the fault. (Reachability)
- If possible, identify a test case that executes the fault, but does not result in an error state.
- If possible identify a test case that results in an error, but
not a failure.
---
<h2 id='answer'>问题解答</h2>
- program 1
  - 程序1中循环体内，变量`i`应从`x.length`遍历到`0`，也就是说，`for (int i=x.length-1; i > 0; i--)` 这一行应当改为`for (int i=x.length-1; i >= 0; i--)`
  - test: `x = [1, 2, 3]; y = 3;` 程序会返回`2`，且程序会在第一次循环时结束，不会执行到 fault 处
  - test: `x = [1, 2, 3]; y = 1;` 由于程序没有查询位置`0`，因此会返回`-1`，程序循环了两次，执行到了fault处，但没有导致错误状态
  - test: `x = [1, 2, 3]; y = 6;` 由于`x`中没有`y`，因此会返回`-1`，是正确结果，但确实在第三次迭代时发生了错误
- program 2
  - 程序2中循环体内，变量i应当从后向前遍历，应将`for (int i = 0; i < x.length; i++)`这一行改为`for (int i = x.length - 1; i >= 0; i--)`
  - test: `x = [0];` 程序会返回`0`，由于x只有一个元素，从前向后与从后向前没有差别，因此没有执行 fault
  - test: `x = [0, 1, 0];` 程序会返回错误结果`0`，但并没有导致错误状态
  - test: `x = [1, 0, 1];` 程序返回了正确结果`1`，但在第一次与第二次迭代时发生了错误。
  ---
  应当明确三个词语 `fault` `error` `failure` 之间的差别，然而海痴并不是很懂，欢迎大神在下面指出错误，并帮忙分析一下这三个“错误”差别在哪里
