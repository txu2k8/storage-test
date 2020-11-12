#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/12 17:17
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""
from .aio_stress import *
__all__ = ['AioStress']

"""
aio_stress
==============
http://fsbench.filesystems.org/bench/aio-stress.c
https://openbenchmarking.org/test/pts/aio-stress
AIO-Stress 0.21

AIO-Stress is an a-synchronous I/O benchmark created by SuSE.
Current this profile uses a 2048MB test file and a 64KB record size.
"""
