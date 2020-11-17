#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/11/6 17:40
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .stream_test import *
__all__ = ['StreamTest']


"""
stream: 文件流写入测试
https://github.com/linux-test-project/ltp/tree/master/testcases/kernel/fs/stream
=========

stream01 -h
  -h      Show this help screen
  -i n    Execute test n times
  -I x    Execute test for x seconds

stream01: 
>KEYS:  < freopen()
>WHAT:  < 1) check that freopen substitutes the named file in place of stream.
>HOW:   < 1) open a stream, write something to it, perform freopen and
        <    write some more. Check that second write to stream went to
        <    the file specified by freopen.

stream02: 
>KEYS:  < fseek() mknod() fopen()

stream03: 
>KEYS:  < fseek() ftell()
>WHAT:  < 1) Ensure ftell reports the correct current byte offset.
>HOW:   < 1) Open a file, write to it, reposition the file pointer and check it.

stream04: 
>KEYS:  < fwrite() fread()
>WHAT:  < 1) Ensure fwrite appends data to stream.
        < 2) Ensure fread and fwrite return values are valid.
>HOW:   < 1) Open a file, write to it, and then check it.
        < 2) Fwrite a know quanity, check return value.
        <    Fread a know quanity, check return value.
     
stream05:    
>KEYS:  < ferror() feof() clearerr() fileno()
>WHAT:  < 1) check that ferror returns zero
        < 2) check fileno returns valid file descriptor
        < 3) check that feof returns zero (nonzero) appropriately
        < 4) check that clearerr resets EOF indicator.
>HOW:   < 1) open a stream and immediately execute ferror
        < 2) use the file des returned from fileno to read a file
        <    written with stream - compare actual vs expected.
        < 3) open stream and ensure feof returns zero, read to end of
        <    file and ensure feof returns non-zero.
        < 4) after 3) above use clearerr and then use feof to ensure
        <    clearerr worked
"""

if __name__ == '__main__':
    pass
