#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/6 18:20
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .read_all import *
__all__ = ['ReadAll']

"""
https://github.com/linux-test-project/ltp/tree/master/testcases/kernel/fs/read_all

 * Perform a small read on every file in a directory tree.
 *
 * Useful for testing file systems like proc, sysfs and debugfs or anything
 * which exposes a file like API so long as it respects O_NONBLOCK. This test
 * is not concerned if a particular file in one of these file systems conforms
 * exactly to its specific documented behavior. Just whether reading from that
 * file causes a serious error such as a NULL pointer dereference.
 *
 * It is not required to run this as root, but test coverage will be much
 * higher with full privileges.
 *
 * The reads are preformed by worker processes which are given file paths by a
 * single parent process. The parent process recursively scans a given
 * directory and passes the file paths it finds to the child processes using a
 * queue structure stored in shared memory.
 *
 * This allows the file system and individual files to be accessed in
 * parallel. Passing the 'reads' parameter (-r) will encourage this. The
 * number of worker processes is based on the number of available
 * processors. However this is limited by default to 15 to avoid this becoming
 * an IPC stress test on systems with large numbers of weak cores. This can be
 * overridden with the 'w' parameters.
"""

if __name__ == '__main__':
    pass
