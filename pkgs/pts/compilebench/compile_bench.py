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

from libs.log import log
from pkgs import PkgBase, TestProfile, to_safe_name

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
            ("Initial Create", "python {0} -D {1} -i 10 --makej INITIAL_CREATE"),
            ("Compile", "python {0} -D {1} -i 10 --makej COMPILE"),
            ("Read Compiled Tree", "python {0} -D {1} -i 10 --makej READ_COMPILED_TREE"),
        ]

        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            test_name = "compile_bench_{0}_{1}".format(idx + 1, to_safe_name(desc))
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(cb_bin, self.test_path))
            tests.append(test)
        return tests

    def stress_profile(self):
        """Return a stress test"""
        cb_bin = os.path.join(bin_path, 'compilebench')
        desc = "stress"
        test_name = "compilebench_{0}".format(to_safe_name(desc))
        test = TestProfile(
            name=test_name,
            desc=desc,
            test_path=self.test_path,
            bin_path=bin_path,
            command="python {0} -D {1} -i 10 --makej".format(cb_bin, self.test_path))

        return test

    def benchmark(self):
        return self.run_tests(self.tests_generator())

    def stress(self):
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
