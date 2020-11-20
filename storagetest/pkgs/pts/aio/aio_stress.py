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

from storagetest.libs.log import log
from storagetest.pkgs.base import PkgBase, TestProfile, to_safe_name

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class AioStress(PkgBase):
    """
    aio_stress
    https://openbenchmarking.org/test/pts/aio-stress
    =============
    An a-synchronous I/O benchmark created by SuSE.
    Current this profile uses a 2048MB test file and a 64KB record size.
    """

    def __init__(self, top_path):
        super(AioStress, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "aio_stress")

    def tests_generator(self):
        """
        Return aio_stress test case list
        """
        aio_bin = os.path.join(bin_path, 'aio_stress')
        cmd_list = [
            ("Write", "cd {0}; {1} -s 2g -r 64k -t 3 -o 0"),
            ("Read", "cd {0}; {1} -s 2g -r 64k -t 3 -o 1"),
            ("Random Write", "cd {0}; {1} -s 2g -r 64k -t 3 -o 2"),
            ("Random Read", "cd {0}; {1} -s 2g -r 64k -t 3 -o 3"),
        ]

        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            test_name = "aio_stress_{0}_{1}".format(idx + 1, to_safe_name(desc))
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(self.test_path, aio_bin))
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
