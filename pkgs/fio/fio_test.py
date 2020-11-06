#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fio_test.py
@Time  : 2020/11/6 15:56
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import random
from concurrent.futures import ThreadPoolExecutor

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir

logger = log.get_logger()


class FIO(object):
    """
    FIO: Flexible I/O tester
    https://fio.readthedocs.io/en/latest/fio_doc.html
    ==========

    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def write(self):
        pass


if __name__ == '__main__':
    pass
