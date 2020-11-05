#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fs_di.py
@Time  : 2020/11/5 10:13
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


class FSDataIntegrity(object):
    """
    FileSystem Data Integrity Test
    ============
    1. Creates a data file of specified or random size and copies
        the file to a random directory depth on a specified filesystem
        The two files are compared and checked for differences.
        If the files differ, then the test fails. By default, this
        test creates a 30Mb file and runs for ten loops.
    2. Creates a datafile of size half of the partition size. Creates
        two fragmented files on the specified partition and copies datafile
        to them. Then compares both the fragmented files with datafile. If
        files differ, then test fails.
    """
    pass


if __name__ == '__main__':
    pass
