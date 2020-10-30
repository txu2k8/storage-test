#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : const.py
@Time  : 2020/10/30 17:29
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

from config.global_settings import *


# --- set/get: Global const keys/values
_global_dict = {}


def set_value(key, value):
    global _global_dict
    _global_dict[key] = value


def get_value(key, default_value=None):
    try:
        global _global_dict
        return _global_dict[key]
    except KeyError:
        return default_value


if __name__ == '__main__':
    print(VERSION)
