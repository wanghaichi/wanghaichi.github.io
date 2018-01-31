---
layout: article
title: 机器学习之 darknet YOLO 训练 VOC 数据集
date: 2018-01-30 13:27:00
tags: 
- machine learning
- darknet
categories: 个人日记
img: /images/2018-01-31-11-15-darknet.jpg
---

最近被安排到中汽研实习（就算是实习吧），做了一些基于深度学习的图像识别工作，其实说起来自己对深度学习也没什么太深入的了解，都是现学现卖，跑人家的例子。不过还是在这边记录一下，以后回首可以稍稍感慨一下年轻时的无知。

关于机器学习，基础知识是看*周志华的西瓜书（清华大学出版社的机器学习）*来学习的，不过大致是囫囵吞枣，没有静下心来安安稳稳地钻研（时间也不允许）。

之后看了网易云课堂中[**吴恩达的机器学习教程**](https://mooc.study.163.com/course/2001281002#/info)，受益匪浅，推荐刚入门的同学去看看，讲的很好。

在吴恩达的视频中，大致了解了卷积神经网络和深度学习大致的套路，其实说到底就是各种卷积层（convolution layer），池化层（pooling layer），全连接层（fool connected layer）不断组合。

感觉机器学习想要深入了解，可能需要看很多相关的论文，之后的学习路程就记录在之后的博客中好了。

先说说甲方的需求：需要在行车过程中动态识别出前方交通标志，如果是限速标识，需要识别中里面的数字。

最近只做了第一部分，也就是交通标志的识别。对卷积神经网络有过了解的话能感觉出来这就是一个分类问题，好在公司已经标好了数据，并且是按照 VOC 格式标记的，接下来就是使用现成的网络训练就可以了。

我用的是 YOLO 在darknet 网站上有 v1 和 v2 两个版本。

https://pjreddie.com/darknet/yolo/

以上是 YOLO darknet 版本的官网，上面的说明非常详细，也非常人性化，即使没有 GPU 也可以使用，可以简单的按照上面的教程进行安装。

注意，`darknet` 默认是不开启 `GPU` 的，当然这对没有 `GPU` 的人（比如我…）是很友好的，但这并不影响 `CPU` 训练网络慢的要死的事实。如果想要开启对 `GPU` 的支持，在 `Makefile` 最上面开启对 `GPU` 和 `CUDNN` 的支持就可以了

```
GPU=0 // 开启GPU，使用 nvidia-smi 来查看本机 GPU 使用情况
CUDNN=0 // 开启CUDA，请确保事先安装好了CUDA，可以运行 nvcc -V 来查看
OPENCV=0 // 开启后可以直接查看预测后的图片
OPENMP=0
DEBUG=0
```

如果顺利，此时你已经可以使用 darknet 预先训练好的 YOLO 模型检测出了样例中的物体。接下来我们要尝试使用自己的数据训练。

关于 VOC 数据集的训练在官网的教程上面也有提到。

```
./darknet detector train cfg/voc.data cfg/yolo-voc.cfg darknet19_448.conv.23
```

一切准备工作就绪后，上面的工作会开始训练，不过你大概会失败，因为有一些坑官网并没有提到。

首先在 voc.data 里面

```
classes= 20
train  = <your work directory>/darknet/train.txt
valid  = <your work directory>/darknet/2007_test.txt
names = data/voc.names
backup = backup
```

这里的 backup 是在训练工程中权重文件储存的位置，需要提前创建好这个文件夹

还需要编辑一下 cfg/yolo-voc.cfg 这个文件，将前几行的 test 次改成 train

```
[net]
# Testing //注释到测试的部分，将训练部分取消注释
#batch=1
#subdivisions=1
# Training
batch=64
subdivisions=8
height=416
width=416
channels=3
momentum=0.9
decay=0.0005
angle=0
saturation = 1.5
exposure = 1.5
hue=.1
```

然后应该就不会有问题了，这里建议大家用 GPU 服务器去训练，不要头铁用 CPU 去尝试，不然你会等到天荒地老。

训练结束后的权重文件在 backup 文件夹中会有保存，按照官网的例子运行就可以了

---


然后说说自己的数据集怎么训练，公司给的数据集是按照 VOC 的格式标注的，虽然有一点不一样，不过总体上已经解决很多问题了，在转换 VOC 数据集的时候，官方提供了一个脚本 `voc_label.py` 我们修改这个文件即可。

**强烈建议大家复制一份配置文件出来，不要直接在原文件修改**

首先我们来看看在训练 VOC 的数据集中，darknet 都用到了什么。

在 cfg/voc.data 中

```
classes= 20
train  = <your work directory>/darknet/train.txt
valid  = <your work directory>/darknet/2007_test.txt
names = data/voc.names
backup = backup
```

classes 参数需要改成你的数据集中具体的分类数目，下面用来训练和测试的图片列表都是有上述的脚本自动生成的，voc.names 里面保存了所有分类。打开 `train.txt` 可以看到里面保存的是用来训练的图片的绝对路径，但是，真正的标注信息却没有体现，也就是 `VOCdevkit/VOC2007/labels` 下面的标签文件。本来百思不得其解，后来发现是在源码中写死的，在`src/data.c` 中有。

```c
find_replace(path, "images", "labels", labelpath);
find_replace(labelpath, "JPEGImages", "labels", labelpath);
```

**也就是说他会根据 `train.txt` 中图片的路径，替换 `JPEGImages` 为`labels` 作为标签路径，因此在生成标签的时候一定要让标签目录与图片目录同级。**

如果你根据你的数据正确修改了 `voc_label.py` 这个脚本文件，那么你的准备工作应该已经接近尾声了。（训练数据和测试数据按照 10 : 1 的比率划分）

最后修改一些网络中的参数就可以了。

`cfg/voc.data` 里面的 `classes` 改成你的分类数量，`voc.names` 里面存好具体分类的名称，然后修改 `cfg/yolo-voc.2.0.cfg` 

```

[convolutional]
...
filters=5*(N+5)
...
classes=N
...
```

修改上面两个参数即可，其他参数可以按需修改。

之后按照同样的操作训练即可

简单说一下训练的时候的输出

```
Region Avg IOU: 0.432582, Class: 0.452631, Obj: 0.143766, No Obj: 0.005994, Avg Recall: 0.391304,  count: 23
623: 14.499426, 14.887394 avg, 0.001000 rate, 1.074940 seconds, 39872 images
```

 在训练的时候会有这些信息在控制台打出，简单说下这些东西的含义

`Region Avg IOU` 交并比，即检测出的框框和标注的框框相交程度，期望趋近于 1

`Avg Recall` 平均召回率，即检测出物体的个数除以标注的所有物体个数，期望趋近于 1

`count` 标注的物体个数

最后一行的格式：

<迭代次数> : < train loss >, < avg train loss >, <学习率> ...

反正我主要关心召回率和损失

据说一个模型训练要很长时间，如果你不小心退出了，没关系，`backup/yolo2.backup` 这个文件是实时备份的，所以只需要从这个备份点重新开始就可以了

```
./darknet detector train cfg/catarc.data cfg/yolo2.0-catarc.cfg backup/yolo2.backup -gpus 0,1
```



参考博客

- [【YOLO】详解：YOLO-darknet训练自己的数据](http://blog.csdn.net/jinlong_xu/article/details/75577007)
- [darknet YOLOv2安装及数据集训练](http://blog.csdn.net/dcrmg/article/details/78496002)
- [【Darknet】【yolo v2】训练自己数据集的一些心得----VOC格式](http://blog.csdn.net/renhanchi/article/details/71077830)