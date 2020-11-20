#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/12 16:57
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .dbench_test import Dbench
__all__ = ['Dbench']

"""
dbench  -- TODO
========
http://samba.org/ftp/tridge/dbench/
https://openbenchmarking.org/test/pts/dbench
Dbench 4.0

Dbench is a benchmark designed by the Samba project as a free 
alternative to netbench, but dbench contains only file-system 
calls for testing the disk performance.
"""


if __name__ == '__main__':
    pass
