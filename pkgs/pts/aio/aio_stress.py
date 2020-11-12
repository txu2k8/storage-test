#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : aio_stress.py
@Time  : 2020/11/12 17:23
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest

from libs import utils
from libs.log import log
from pkgs import PkgBase, TestProfile

logger = log.get_logger()


class AioStress(PkgBase):
    """
    aio_stress
    https://sourceforge.net/projects/fsmark/
    =============
    AIO-Stress is an a-synchronous I/O benchmark created by SuSE.
    Current this profile uses a 2048MB test file and a 64KB record size.
    """

    def __init__(self, top_path):
        super(AioStress, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "aio_stress")

    def tests_generator(self):
        """
        Return fs_mark test case list FYI:
        https://openbenchmarking.org/test/pts/fs-mark
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        fm_bin = os.path.join(cur_dir, 'bin/fs_mark')
        cmd_list = [
            ("1000 Files, 1MB Size", "{0} -d {1} -s 1048576 -n 1000"),
            ("1000 Files, 1MB Size, No Sync/FSync", "{0} -d {1} -s 1048576 -n 1000 -S 0"),
            ("5000 Files, 1MB Size, 4 Threads", "{0} -d {1} -s 1048576 -n 5000 -t 4"),
            ("4000 Files, 32 Sub Dirs, 1MB Size", "{0} -d {1} -s 1048576 -n 4000 -D 32"),
        ]

        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            test_name = "fs_mark_{0}_{1}".format(idx + 1, utils.to_safe_name(desc))
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=fm_bin,
                command=cmd.format(fm_bin, self.test_path))
            tests.append(test)
        return tests

    def benchmark(self):
        return self.run_tests(self.tests_generator())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.aio = AioStress("/mnt/test")

    def test_benchmark(self):
        self.aio.benchmark()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

