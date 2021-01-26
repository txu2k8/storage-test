#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : smbtorture.py
@Time  : 2021/1/26 15:23
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import re
import unittest
from collections import defaultdict

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary
from storagetest.pkgs.base import PkgBase, TestProfile, to_safe_name

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class SMBTorture(PkgBase):
    """
    SMB Torture
    https://github.com/samba-team/samba
    =============
    The Samba torture suite is an extensive, general purpose CIFS test suite.
    It is not Samba specific
    """

    def __init__(self, top_path, server, user, password):
        super(SMBTorture, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "smb_torture")
        self.server = server
        self.user = user
        self.password = password

    def verify1(self):
        if os.name != "posix":
            raise PlatformError("smbtorture just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)
        rc, output = utils.run_cmd('which smbtorture')
        if not output.strip("\n") or 'no smbtorture' in output:
            logger.warning("yum install smbtorture -y")
            raise NoSuchBinary("smbtorture not installed")

    @staticmethod
    def get_default_tests():
        """Get the default test case list by command"""
        case_info = defaultdict(list)

        rc, output = utils.run_cmd("smbtorture", expected_rc=0)
        lines = output.split('Tests are:')[1].strip('\r\n').split('\n')
        # logger.info(line_list)
        pattern_suite = r'\((\S*)\):'
        suite = ""
        for line in lines:
            if not line or line == '\r' or "The default test is ALL" in line:
                continue
            match_suite = re.findall(pattern_suite, line)
            if match_suite:
                suite = match_suite[0]
            elif suite:
                case_info[suite].extend(line.strip(' \r').split(' '))
            else:
                pass
        return case_info

    def tests_generator(self):
        """
        Return smbtorture test case list
        smbtorture //server/share -Uuser%pass testcase
        """

        default_tests = self.get_default_tests()
        idx = 0
        tests = []
        for suite in default_tests.keys():
            for tc in default_tests[suite]:
                test_name = "smbtorture_{0}_{1}".format(idx + 1, to_safe_name(tc))
                cmd = "smbtorture //{0}/{1} -U{2}%{3} {4}"
                test = TestProfile(
                    name=test_name,
                    desc=tc,
                    test_path=self.test_path,
                    bin_path=bin_path,
                    command=cmd.format(self.server, self.test_path, self.user, self.password, tc))
                tests.append(test)
        return tests

    def sanity(self):
        return self.run_tests(self.tests_generator())

    def stress(self):
        return self.run_tests(self.tests_generator())

    def benchmark(self):
        return self.run_tests(self.tests_generator())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.smb_torture = SMBTorture("/mnt/test")

    def test_benchmark(self):
        self.smb_torture.sanity()


if __name__ == '__main__':
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

