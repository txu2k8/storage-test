#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/13 13:52
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .iozone_test import *
__all__ = ["IOzone"]

"""
IOzone Filesystem Benchmark
============================
http://www.iozone.org/
https://openbenchmarking.org/test/pts/iozone

IOzone is a filesystem benchmark tool. 
The benchmark generates and measures a variety of file operations. 
Iozone is useful for performing a broad filesystem analysis of a vendor’s computer platform. 
The benchmark tests file I/O performance for the following operations:
    Read, write, re-read, re-write, read backwards, 
    read strided, fread, fwrite, random read, pread,
    mmap, aio_read, aio_write
    
-i #  Test to run 
    0=write/rewrite, 1=read/re-read, 2=random-read/write
    3=Read-backwards, 4=Re-write-record, 5=stride-read, 6=fwrite/re-fwrite
    7=fread/Re-fread, 8=random_mix, 9=pwrite/Re-pwrite, 10=pread/Re-pread
    11=pwritev/Re-pwritev, 12=preadv/Re-preadv
"""


if __name__ == '__main__':
    pass
