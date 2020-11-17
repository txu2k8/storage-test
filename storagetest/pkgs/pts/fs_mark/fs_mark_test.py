#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fs_mark_test.py
@Time  : 2020/11/12 16:09
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest

from storagetest.libs.log import log
from storagetest.pkgs.base import PkgBase, TestProfile, to_safe_name

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class FSMark(PkgBase):
    """
    fs_mark
    https://sourceforge.net/projects/fsmark/
    =============
    The fs_mark benchmark tests synchronous write workloads.
    It can vary the number of files, directory depth, etc.
    It has detailed timings for reads, writes, unlinks and fsyncs
    that make it good for simulating mail servers and other setups.
    """

    def __init__(self, top_path):
        super(FSMark, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "fs_mark")

    def tests_generator(self):
        """
        Return fs_mark test case list
        """
        fm_bin = os.path.join(bin_path, 'fs_mark')
        cmd_list = [
            ("1000 Files, 1MB Size", "{0} -d {1} -s 1048576 -n 1000"),
            ("1000 Files, 1MB Size, No Sync/FSync", "{0} -d {1} -s 1048576 -n 1000 -S 0"),
            ("5000 Files, 1MB Size, 4 Threads", "{0} -d {1} -s 1048576 -n 5000 -t 4"),
            ("4000 Files, 32 Sub Dirs, 1MB Size", "{0} -d {1} -s 1048576 -n 4000 -D 32"),
        ]

        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            test_name = "fs_mark_{0}_{1}".format(idx + 1, to_safe_name(desc))
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(fm_bin, self.test_path))
            tests.append(test)
        return tests

    def benchmark(self):
        return self.run_tests(self.tests_generator())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fm = FSMark("/mnt/test")

    def test_benchmark(self):
        self.fm.benchmark()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
