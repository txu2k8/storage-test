#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/12 15:49
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .fs_mark_test import *
__all__ = ['FSMark']

"""
fs_mark
==============
https://sourceforge.net/projects/fsmark/
https://openbenchmarking.org/test/pts/fs-mark
FS-Mark 3.3

The fs_mark benchmark tests synchronous write workloads. 
It can vary the number of files, directory depth, etc. 
It has detailed timings for reads, writes, unlinks and fsyncs 
that make it good for simulating mail servers and other setups.
"""


if __name__ == '__main__':
    pass
