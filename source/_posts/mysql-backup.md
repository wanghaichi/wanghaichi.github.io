---
layout: article
title: Mysql 增量备份，全部备份实现方法以及自动化脚本
date: 2017-10-20 00:41:45
tags: mysql
img: /images/2018-01-31-11-26-data.jpg
---

## 前情摘要

自己作死干了一件特别蠢的事情（具体略）

然后开始研究如何进行增量备份

## 增量备份

### 原理

mysql 有个 binlog 的功能，会记录所有的用户的操作，可以依靠这个，配合全备份，将数据库回滚到某一个特殊的时刻。hhh

简单来说，比如我们每周做一次全备份，每天做一次增量备份，当数据库发生问题的时候，我们就可以先将数据库回滚到上一周我们的全备份的时间，然后再通过每天的增量备份（其实就是模拟所有的数据库操作，全部执行一遍），将数据恢复到我们想要的时间点。

### 配置

mysql 的 binlog 功能需要在配置文件中打开，在 my.cnf 或者 mysqld.cnf 中添加以下几行：

```shell
server-id               = 1

# binlog存放路径
log_bin                 = /var/log/mysql/mysql-bin.log

# binlog记录的格式，有row、statement、mixed三种选项
binlog-format           = row

# binlog写缓冲区设置大小，由于是内存，写速度非常快，可以有效提高binlog的写效率，如果数据库中经常出现大事务，可以酌情提高该参数。
binlog_cache_size       = 32m

# 最大缓存区大小
max_binlog_cache_size   = 512m

# binlog文件最大的大小
max_binlog_size         = 1000m

# 需要备份的数据库名，如果备份多个数据库，重复设置这个选项即可
binlog-do-db=game     
binlog-do-db=platform

# 不需要备份的数据库，如果备份多个数据库，重复设置这个选项即可
binlog-ignore-db=
```

重启mysql服务，在对应的文件夹下(这里是`/var/log/mysql`)会看到 `mysql-bin.000001` 和 `mysql-bin.index` 两个文件，第一个就是我们需要的 binlog 文件，里面会记录我们的操作，第二个负责记录 binlog 的名称，可以用来判断当前最新的 binlog 是哪一个

### 一些相关的操作

开启了binlog之后，就可以进行一些尝试了，可以先去数据库做一些修改操作。（因为binlog的格式选择的是row，所以select语句是不会被记录的）

```mysql
mysql> UPDATE ....
mysql> DELETE ....
// 查看当前log的备份情况
mysql> show master logs;
// 查看最新的备份文件的情况
mysql> show master status;
// 将当前的log写入磁盘，并创建新的binlog文件
mysql> flush log;
```

binlog 文件可以使用 mysqlbinlog 命令查看

```mysql
// 查看binlogfile即可看到这份log中记录的数据库操作
mysqlbinlog mysql-bin.000011 > /tmp/binlogfile
// 获取指定位置范围的记录
mysqlbinlog --start-position=1285 --stop-position=1681 mysql-bin.000011 > /tmp/binlogfile
// 获取指定时间范围内的记录，常用
mysqlbinlog --start-date="2012-10-15 16:30:00" --stop-date="2012-10-15 17:00:00"
```

## 全备份

全备份没什么好说的，mysqldump一条命令就可以了
```
mysqldump -uroot -ppwd --quick --all-databases --flush-logs --delete-master-logs --single-transaction > $dumpFile
```
注意里面的一些参数，尤其是flush-logs和single-transaction两个参数，建议开启

## 自动化脚本

全备份
```shell
#!/bin/bash

# 全备份路径
backDir=/var/log/mysql/backup/weekly

# 日志文件
logFile=/var/log/mysql/backup/bak-all.log

# 获取当前时间，用于命名
nowDate=`date +%Y%m%d`
beginTime=`date +"%Y%m%d %H:%M:%S"`

# 进入备份文件夹
cd $backDir
dumpFile=$nowDate.sql
dumpFileTgz=$nowDate.sql.tgz

# mysqldump 导出所有数据库
echo dumping...
mysqldump -uroot -ppwd --quick --all-databases --flush-logs --delete-master-logs --single-transaction > $dumpFile
echo compressing...

# 压缩文件
tar czvf $dumpFileTgz $dumpFile
rm $dumpFile
endTime=`date +"%Y%m%d %H:%M:%S"`
echo begin:$beginTime end:$endTime $dumpFileTgz succ >> $logFile

# 清楚之前的增量备份
cd $backDir/../daily
rm -f *
```

增量备份脚本

```
#!/bin/bash

# 增量备份存放路径
backDir=/var/log/mysql/backup/daily
# binlog存放路径
binDir=/var/log/mysql/
# 日志文件
logFile=/var/log/mysql/backup/bak-daily.log
# binlog.index 文件路径
binIndex=/var/log/mysql/mysql-bin.index
# 将当前所有的日志写到磁盘，会新建一个00000*的binlog文件
mysqladmin -uroot -phhxxttxs flush-logs
# 获取当前有几条binlog文件（需要保证是从1开始的）
count=`wc -l $binIndex | awk '{print $1}'`

nextNum=0

for file in  `cat $binIndex`
do
    # 获取文件名，去除文件夹名
    base=`basename $file`
    # 遍历每个binlog文件，如果是最新的不做操作，否则备份
    nextNum=`expr $nextNum + 1`
    if [ $nextNum -eq $count ]
    then
    	echo $base skip!  >> $logFile
    else
        dest=$backDir/$base
        # file already exist
        if(test -e $dest)
        then
            echo  $base exist! >> $logFile
       	else
            cp $binDir/$base $backDir
            echo $base copyed >> $logFile
        fi
    fi
done

echo `date +"%Y%m%d %H:%M:%S"` Backup succ! >> $logFile
```

做一下定时就好了

## 具体恢复操作

当发现数据丢失时

1. 确认丢失数据的开始时间
2. 找到距离这个时间最近的全量备份
3. mysql -uuser -p < all.sql
4. 依次运行从全备份到丢失时间之间的增量备份
5. mysqlbinlog mysql-bin.000123 --start-date="" --end-date="" > /tmp/tmpfile
6. mysql -uuser -p < /tmp/tmpfile

通过以上，就可以将数据还原到需要的还原点。
记得定期查看备份的log文件，以防出现问题，全备份需要定时清理