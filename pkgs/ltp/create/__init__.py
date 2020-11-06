#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/5 11:15
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .create_file import *
__all__ = ['CreateDataFile']


"""
./create_datafile -h
=====================
usage:
    create_file <# of 1048576 buffers to write> <name of file to create>
     ex. # create_file 10 /tmp/testfile
"""

if __name__ == '__main__':
    pass
