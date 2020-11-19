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
DBENCH
==============
https://dbench.samba.org/web/index.html
https://openbenchmarking.org/test/pts/dbench-1.0.0


DBENCH is a tool to generate I/O workloads to either a filesystem or to 
a networked CIFS or NFS server. It can even talk to an iSCSI target. 
DBENCH can be used to stress a filesystem or a server to see which workload 
it becomes saturated and can also be used for preditcion analysis to determine 
"How many concurrent clients/applications performing this workload can my server 
handle before response starts to lag?"

DBENCH provides a similar benchmarking and client emulation that is implemented 
in SMBTORTURE using the BENCH-NBENCH test for CIFS, but DBENCH can play these 
loadfiles onto a local filesystem instead of to a CIFS server. 
Using a different type of loadfiles DBENCH can also generate and measure latency for NFS.

Features include:
1. Reading SMBTORTURE BENCH-NBENCH loadfiles and emulating this workload as posix 
    calls to a local filesystem
2. NFS style loadfiles which allows DBENCH to mimic the i/o pattern of a real 
    application doing real i/o to a real server.
3. iSCSI support and iSCSI style loadfiles.

Loadfiles
At the heart of DBENCH is the concept of a "loadfile". A loadfile is a sequence of operations 
to be performed once statement at a time. This could be operations such as "Open file XYZ", 
"Read 5 bytes from offset ABC", "Close the file", etc etc.

By carefully crafting a loadfile it is possible to describe an I/O pattern that almost exactly 
matches what a particular application performs. While cumbersome to produce, such a loadfile 
it does allow you to describe exactly how/what an application performs and "replay" this 
sequence of operations any time you want.

Each line in the DBENCH loadfile contain a timestamp for the operation. 
This is used by DBENCH to try to keep the same rate of operations as the original application. 
This is very useful since this allows to perform accurate scalability predictions based on the 
exact application we are interested in. and not an artificial benchmark which may or may not 
be relevant to our particular applications workload pattern.
"""
