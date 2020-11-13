#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/12 18:27
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .compile_bench import *
__all__ = ['CompileBench']

"""
compilebench
==============
https://oss.oracle.com/~mason/compilebench/
https://openbenchmarking.org/test/pts/compilebench

Compilebench tries to age a filesystem by simulating some of the disk IO 
common in creating, compiling, patching, stating and reading kernel trees. 
It indirectly measures how well filesystems can maintain directory locality 
as the disk fills up and directories age. 
This current test is setup to use the makej mode with 10 initial directories

Quick and dirty usage: (note the -d option changed in 0.6)
1. Untar compilebench
2. run commands:
    ./compilebench -D some_working_dir -i 10 -r 30
    ./compilebench -D some_working_dir -i 10 --makej
    ./copmilebench -D some_working_dir -i 10 --makej -d /dev/xxx -t trace_file
    ./compilebench --help for more
"""


if __name__ == '__main__':
    pass
