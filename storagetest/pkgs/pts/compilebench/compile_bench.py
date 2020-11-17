#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : compile_bench.py
@Time  : 2020/11/13 9:19
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


class CompileBench(PkgBase):
    """
    CompileBench
    https://oss.oracle.com/~mason/compilebench/
    =============
    Compilebench tries to age a filesystem by simulating some of the disk IO
    common in creating, compiling, patching, stating and reading kernel trees.
    It indirectly measures how well filesystems can maintain directory locality
    as the disk fills up and directories age.
    """

    def __init__(self, top_path):
        super(CompileBench, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "compile_bench")

    def tests_generator(self):
        """
        Return CompileBench test case list
        """
        cb_bin = os.path.join(bin_path, 'compilebench')
        cmd_list = [
            ("Initial Create/Compile/Read Compiled Tree", "{0} -D {1} -i 10 --makej -s {2}"),
        ]

        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            test_name = "compile_bench_{0}_{1}".format(idx + 1, to_safe_name(desc))
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(cb_bin, self.test_path, bin_path))
            tests.append(test)
        return tests

    def benchmark_profile(self):
        """
        Return a benchmark test
            Initial Create
            Compile
            Read Compiled Tree
        """
        cb_bin = os.path.join(bin_path, 'compilebench')
        desc = "benchmark"
        test_name = "compilebench_{0}".format(to_safe_name(desc))
        test = TestProfile(
            name=test_name,
            desc=desc,
            test_path=self.test_path,
            bin_path=bin_path,
            command="{0} -D {1} -i 10 --makej".format(cb_bin, self.test_path))

        return test

    def stress_profile(self):
        """
        Return a stress test
            intial create
            create
            patch
            compile
            clean
            read tree
            read compiled tree
            delete tree
            delete compiled tree
            stat tree
            stat compiled tree
        """
        cb_bin = os.path.join(bin_path, 'compilebench')
        desc = "stress"
        test_name = "compilebench_{0}".format(to_safe_name(desc))
        test = TestProfile(
            name=test_name,
            desc=desc,
            test_path=self.test_path,
            bin_path=bin_path,
            command="{0} -D {1} -i 10".format(cb_bin, self.test_path))

        return test

    def benchmark(self):
        """
        A shorter run that simulates the files created by running make -j in a kernel tree,
        and then readingand deleting the kernel trees.
        """
        logger.info(self.benchmark.__doc__)
        return self.run(self.benchmark_profile())

    def stress(self):
        """
        A full tests include:
            intial create
            create
            patch
            compile
            clean
            read tree
            read compiled tree
            delete tree
            delete compiled tree
            stat tree
            stat compiled tree"""
        logger.info(self.stress.__doc__)
        return self.run(self.stress_profile())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.cb = CompileBench("/mnt/test")

    def test_benchmark(self):
        self.cb.benchmark()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
