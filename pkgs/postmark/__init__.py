#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/10/27 10:27
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .postmark_test import *
__all__ = ['PostMark']

"""
PostMark
==============
http://openbenchmarking.org/test/pts/postmark
pts/postmark-1.1.2
postmark_1.51

Mail server workload
Postmark主要用于测试文件系统在邮件系统或电子商务系统中性能，这类应用的特点是：需要频繁、大量地存取小文件
原理：构建一个测试文件池，通过文件最大，最小大小，数量等参数进行配置，然后进行事务的初始化，
对每一个事务中读取/附加,创建/删除等所占的比例进行设置来模拟真是应用场景，事务操作完成后，
Postmark对文件池进行删除，结束测试，输出结果。

Postmark是用随机数来产生所操作文件的序号，从而使测试更加贴近于现实应用。
输出结果中比较重要的输出数据包括测试总时间、每秒钟平均完成的事务数、在事务处理中平均每秒创建和删除的文件数，
以及读和写的平均传输速度。
"""

if __name__ == '__main__':
    pass
