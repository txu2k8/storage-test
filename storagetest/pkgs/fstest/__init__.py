#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/2 15:19
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .fs_test import *
__all__ = ['FSTest']

"""
https://github.com/zfsonlinux/fstest
==============
fstest是一套简化版的文件系统POSIX兼容性测试套件，它可以工作在FreeBSD, Solaris, Linux上,
用于测试UFS, ZFS, ext3, XFS, NTFS-3G等文件系统。
fstest目前有3601个回归测试用例，测试的系统调用覆盖chmod, chown, link, mkdir, mkfifo, 
open, rename, rmdir, symlink, truncate, unlink。
"""

if __name__ == '__main__':
    pass
