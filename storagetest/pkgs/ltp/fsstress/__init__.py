#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : __init__.py.py
@Time  : 2020/10/27 9:40
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from .fs_stress import *
__all__ = ['FSStress']


"""
FYI: https://www2.cs.duke.edu/ari/fstress/
Fstress is a synthetic, flexible, self-scaling NFS file service benchmark 
whose primary goal is flexibility. 
Fstress exports control over several dimensions in both data set and workload, 
enabling a wide range of tests for fundamental evaluation of file service 
scalability, sizing, configuration, and other factors. 
Fstress includes several important "canned" workloads.
"""

if __name__ == '__main__':
    pass
