#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/10/27 10:25
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .filebench import FileBench
__all__ = ['FileBench']

"""
Filebench - A Model Based File System Workload Generator
https://github.com/filebench/filebench/wiki
===============
Filebench is a file system and tests benchmark that can generate a large
variety of workloads. Unlike typical benchmarks it is extremely flexible and
allows to specify application's I/O behavior using its extensive Workload Model
Language (WML). Users can either describe desired workloads from scratch or use
(with or without modifications) workload personalities shipped with Filebench
(e.g., mail-, web-, file-, and database-server workloads).

Filebench 是一款文件系统性能的自动化测试工具，它通过快速模拟真实应用服务器的负载来测试文件系统的性能。
它不仅可以仿真文件系统微操作（如 copyfiles, createfiles, randomread, randomwrite ），
而且可以仿真复杂的应用程序（如 varmail, fileserver, oltp, dss, webserver, webproxy ）。
Filebench 比较适合用来测试文件服务器性能，但同时也是一款负载自动生成工具，也可用于文件系统的性能。
"""

if __name__ == '__main__':
    pass
