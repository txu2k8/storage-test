#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : benchmark.py
@Time  : 2020/11/12 11:10
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import time
import unittest

from libs import log
from libs import utils
from libs.exceptions import NoSuchDir
from libs.customtest import CustomTestCase
from config import const

logger = log.get_logger()
args = const.get_value('args')


class BenchMarkTC(CustomTestCase):
    """BenchMark test on a mount point or path"""
    _fs_path = args.test_path

    @classmethod
    def setUpClass(cls):
        logger.info("Start BenchMark test on {}".format(cls._fs_path))
        if not os.path.isdir(cls._fs_path):
            raise NoSuchDir(cls._fs_path)
        str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        cls.test_path = os.path.join(cls._fs_path, "benchmark_"+str_time)
        utils.mkdir_path(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        logger.info("BenchMark test on {} complete!".format(cls._fs_path))

    # ==== LTP ====
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.sanity())

    # ==== PTS ====
    def test_fio(self):
        """FIO: Flexible I/O tester."""
        from pkgs.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.sanity())

    def test_postmark(self):
        """Simulate small-file testing similar to the tasks endured by web and mail servers"""
        from pkgs.pts.postmark import PostMark
        pm = PostMark(self.test_path)
        logger.info(pm.__doc__)
        self.assertTrue(pm.benchmark())

    def test_fs_mark(self):
        """The fs_mark benchmark tests synchronous write workloads"""
        from pkgs.pts.fs_mark import FSMark
        fm = FSMark(self.test_path)
        logger.info(fm.__doc__)
        self.assertTrue(fm.benchmark())

    # ==== Private ====
    def test_consistency(self):
        """Test the file consistency"""
        from pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        logger.info(cst.__doc__)
        self.assertTrue(cst.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(BenchMarkTC)
    unittest.TextTestRunner(verbosity=2).run(suite)