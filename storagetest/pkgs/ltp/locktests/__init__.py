#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/2 16:12
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .lock_test import *
__all__ = ['LockTest']

"""
locktest
http://nfsv4.bullopensource.org/tools/tests/locktest.php
https://github.com/linux-test-project/ltp/tree/master/testcases/network/nfsv4/locks
==============
locktest用于fcntl锁功能的压力测试。运行时，主进程先在指定文件区域设置字节范围的记录锁，
然后多个从进程尝试在该文件区域执行read, write, 加新锁操作。
这些操作结果是可预期的（矩阵如下），如果操作结果与预期一致则测试通过，否则测试失败。
EXPECTED RESULTS
================
Here is the table of expected results, depending on :
 - Slave test operations (READ, WRITE, SET A WRITE LOCK ... )
 - Master Operation (SET A READ/A WRITE LOCK )
 - Slave types (Processes, threads)
 - Locking profile (POSIX locking, Mandatory locking)
=====================================================================================================
                                    |                       Master  process/thread                  |
====================================|===============================================================|
Slave type   |   Test operation     |    advisory         locking    |   mandatory        locking   |
____________________________________|________________________________|______________________________|
             |                      |    read lock       write lock  |   read lock       write lock |
____________________________________|________________________________|______________________________|
thread       |   set a read lock    |     Allowed         Allowed    |    Allowed         Allowed   |
             |   set a write lock   |     Allowed         Allowed    |    Allowed         Allowed   |
             |   read               |     Allowed         Allowed    |    Allowed         Allowed   |
             |   write              |     Allowed         Allowed    |    Allowed         Allowed   |
====================================+================================+==============================|
process      |   set a read lock    |     Allowed         Denied     |    Allowed         Denied    |
             |   set a write lock   |     Denied          Denied     |    Denied          Denied    |
             |   read               |     Allowed         Allowed    |    Denied          Allowed   |
             |   write              |     Allowed         Allowed    |    Denied          Denied    |
=====================================================================================================
"""

if __name__ == '__main__':
    pass
