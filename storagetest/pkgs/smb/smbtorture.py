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
from prettytable import PrettyTable

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

    def __init__(self, top_path, server, user, password, case_filter='', expect_failures=None):
        super(SMBTorture, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "smb_torture")
        self.server = server
        self.user = user
        self.password = password
        self.case_filter = case_filter
        self.expect_failures = expect_failures

    def verify(self):
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
                if not str(tc).startswith(self.case_filter):
                    continue
                test_name = "smbtorture_{0}_{1}".format(idx + 1, to_safe_name(tc))
                cmd = "smbtorture //{0}/{1} -U{2}%{3} {4}"
                test = TestProfile(
                    name=test_name,
                    desc=tc,
                    test_path=self.test_path,
                    bin_path='',
                    command=cmd.format(self.server, self.test_path, self.user, self.password, tc))
                tests.append(test)
        return tests

    @staticmethod
    def result_analyze(test, result, expect_failure_list=None):
        """
        Compare result with the expect_failure_list
        :param test:
        :param result:
        :param expect_failure_list:
        :return: True | False
        """
        if expect_failure_list is None:
            expect_failure_list = []
        actual_failure_list = []
        # find all failures in result
        pattern_success = re.compile(r'(success):\s+(.+)')
        pattern_failure = re.compile(r'(failure):\s+(.+\b)\s+(\[\s\S+.+\s\S)')
        pattern_skip = re.compile(r'(skip):\s+(.+\b)\s+(\[\s\S+.+\s\S)')
        success_info = pattern_success.findall(result)
        failure_info = pattern_failure.findall(result)
        skip_info = pattern_skip.findall(result)

        for success in success_info:
            logger.info("%s: %s" % (success[0], success[1]))

        for failure in failure_info:
            if failure[1] in expect_failure_list:
                logger.warning("%s: %s %s" % (failure[0], failure[1], failure[2]))
            else:
                logger.error("%s: %s %s" % (failure[0], failure[1], failure[2]))
                actual_failure_list.append(failure[1])

        for skip in skip_info:
            logger.warning("%s: %s %s" % (skip[0], skip[1], skip[2]))

        diff_acturl_expect = utils.get_list_difference(actual_failure_list, expect_failure_list)
        pass_flag = False if diff_acturl_expect else True

        expect_failure_len = len(expect_failure_list)
        actual_failure_len = len(actual_failure_list)
        diff_failure_len = len(diff_acturl_expect)
        column_len = max(expect_failure_len, actual_failure_len,
                         diff_failure_len)
        table = PrettyTable()
        table.add_column('Test', [test] * column_len)
        table.add_column('Expect_Failure', expect_failure_list + [''] * (
                column_len - expect_failure_len))
        table.add_column('Actual_Failure', actual_failure_list + [''] * (
                column_len - actual_failure_len))
        table.add_column('Diff_Acturl_Expect', diff_acturl_expect + [''] * (
                column_len - diff_failure_len))
        if pass_flag:
            logger.info('PASS: %s \n%s' % (test, table.get_string(align="l")))
        else:
            logger.error('FAIL: %s \n%s' % (test, table.get_string(align="l")))

        return pass_flag

    def run(self, test):
        logger.info(test.desc)
        self.verify()
        test_name = test.name
        test_path = test.test_path
        binary_path = test.bin_path
        fail_flag = test.fail_flag
        test_log = os.path.join(self.top_path, '{0}.log'.format(test_name))
        test_cmd = "{0} | tee -a {1}".format(test.command, test_log)
        utils.mkdir_path(test_path)

        try:
            if binary_path:
                os.system('chmod +x {0}/*'.format(binary_path))
            rc, output = utils.run_cmd(test_cmd, timeout=72000)
            logger.info(output)
            if fail_flag and fail_flag in output:
                raise Exception("FAIL: Run {0} on {1}".format(test_name, test_path))
            pass_flag = self.result_analyze(test, output, self.expect_failures)
            if pass_flag:
                logger.info("PASS: Run {0} on {1}".format(test_name, test_path))
            else:
                logger.info("FAIL: Run {0} on {1}".format(test_name, test_path))
                return pass_flag
        except Exception as e:
            logger.info("FAIL: Run {0} on {1}".format(test_name, test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        return self.run_tests(self.tests_generator())

    def stress(self):
        return self.run_tests(self.tests_generator())

    def benchmark(self):
        return self.run_tests(self.tests_generator())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.smb_torture = SMBTorture("/mnt/test", '', '', '')

    def test_benchmark(self):
        self.smb_torture.sanity()


if __name__ == '__main__':
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

