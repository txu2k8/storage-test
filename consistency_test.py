#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : consistency_test.py
@Time  : 2020/10/26 15:14
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from pkgs.fileops.file_ops import Consistency


if __name__ == '__main__':
    cst = Consistency()
    print(cst.__doc__)
    cst.test()
