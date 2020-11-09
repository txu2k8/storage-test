#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/5 10:25
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .acl_test import *
__all__ = ['AclXattr']

"""
https://github.com/linux-test-project/ltp/tree/master/testcases/kernel/fs/acl

USAGE       : ./tacl_xattr.sh
DESCRIPTION : A script that will test ACL and Extend Attribute on Linux system.
REQUIREMENTS:
           1) Kernel with loop device support
           2) A spare (scratch) disk partition of 100MB or larger.
           3) Kernel with ACL and Extend Attribute function support
"""

if __name__ == '__main__':
    pass
