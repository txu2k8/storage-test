#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : filebench_test.py
@Time  : 2020/11/19 9:38
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from parameterized import parameterized, param

from storagetest.libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary
from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.pkgs.filebench import FileBench

logger = log.get_logger()


def custom_name_func():
    def custom_naming_func(testcase_func, param_num, param):
        return '{0}_{1}_{2}'.format(testcase_func.__name__, param_num, parameterized.to_safe_name(param.args[0]))
        # return testcase_func.__name__ + '_' + parameterized.to_safe_name(param.args[0])

    return custom_naming_func


class FilebenchTestCase(unittest.TestCase):
    _test_path = "/tmp"
    # Verify
    if os.name != "posix":
        raise PlatformError("fs_test just support for linux machine!")
    if not os.path.isdir(_test_path):
        raise NoSuchDir(_test_path)
    rc, output = utils.run_cmd('which filebench')
    if not output.strip("\n") or 'no filebench' in output:
        logger.warning("yum install filebench -y")
        raise NoSuchBinary("filebench not installed")

    def setUp(self):
        logger.info("Filebench Test Start ...")

    def tearDown(self):
        logger.info("Filebench Test Complete!")

    fb_parameterized = []
    fb_test = FileBench(_test_path)
    logger.info(fb_test.__doc__)
    for test in fb_test.tests_generator():
        p = param(test.name, test)
        fb_parameterized.append(p)

    @parameterized.expand(fb_parameterized, name_func=custom_name_func())
    def test_filebench(self, _, test):
        self.fb_test.run(test)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(FilebenchTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
