#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : base.py
@Time  : 2020/11/12 17:30
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""
import os
import re
import unittest
from prettytable import PrettyTable
from datetime import datetime

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

logger = log.get_logger()


def to_safe_name(s):
    return str(re.sub("[^a-zA-Z0-9_]+", "_", s))


class TestProfile(object):
    """Define the test struct"""
    def __init__(self, name="", desc="", test_path="", bin_path="", command="",
                 fail_flag="Test failed"):
        self.name = name
        self.desc = desc
        self.test_path = test_path
        self.bin_path = bin_path  # chmod +x bin_path/*
        self.command = command
        self.fail_flag = fail_flag


class PkgBase(object):
    """Description for the pkg"""

    def __init__(self, top_path):
        self.top_path = top_path
        self.test_path = top_path
        self.phase_list = []

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def print_phase(self):
        if len(self.phase_list) == 0:
            return True
        step_table = PrettyTable(['No.', 'Step', 'Result', 'Elapsed', 'Comments'])
        step_table.align['Step'] = 'l'
        step_table.align['Comments'] = 'l'
        for idx, step in enumerate(self.phase_list):
            step_status = [idx + 1] + step
            step_table.add_row(step_status)
        logger.info("\n{0}".format(step_table))
        return True

    def tests_generator(self, *args, **kwargs):
        """Return TestProfile list"""
        print(self.test_path)
        tests = [TestProfile(name="Not Defined", desc="test desc", command="pwd")]
        return tests

    def test_generator(self, *args, **kwargs):
        print(self.test_path)
        return TestProfile(name="Not Defined", desc="test desc", command="pwd")

    def run(self, test):
        logger.info(test.desc)
        self.verify()
        test_name = test.name
        test_path = test.test_path
        bin_path = test.bin_path
        fail_flag = test.fail_flag
        test_log = os.path.join(self.top_path, '{0}.log'.format(test_name))
        test_cmd = "{0} | tee -a {1}".format(test.command, test_log)
        utils.mkdir_path(test_path)

        try:
            if bin_path:
                os.system('chmod +x {0}/*'.format(bin_path))
            rc, output = utils.run_cmd(test_cmd, timeout=72000)
            logger.info(output)
            if fail_flag and fail_flag in output:
                raise Exception("FAIL: Run {0} on {1}".format(test_name, test_path))
            logger.info("PASS: Run {0} on {1}".format(test_name, test_path))
        except Exception as e:
            logger.info("FAIL: Run {0} on {1}".format(test_name, test_path))
            raise e
        finally:
            pass

        return True

    def run_tests(self, tests):
        for test in tests:
            self.phase_list.append([test.name, "Start", '', test.desc])
            start_time = datetime.now()
            self.print_phase()
            try:
                ret = self.run(test)
                self.phase_list[-1][1] = "PASS" if ret else "FAIL"
            except Exception as e:
                self.phase_list[-1][1] = "FAIL"
                raise e
            finally:
                end_time = datetime.now()
                self.phase_list[-1][2] = str(end_time - start_time).split('.')[0]
                self.print_phase()
        return True


def posix_ready():
    return os.name == "posix"


def windows_ready():
    return os.name == "nt"


def filebench_ready():
    try:
        utils.run_cmd('which filebench', expected_rc=0)
    except Exception as e:
        # logger.warning(e)
        logger.warning("filebench not installed.(yum install -y filebench)")
        return False
    return True


def prove_ready():
    try:
        utils.run_cmd('prove -h', expected_rc=1)
    except Exception as e:
        # logger.warning(e)
        logger.warning("perl not installed.(yum install perl-Test-Harness)")
        return False
    return True


def fio_ready():
    try:
        utils.run_cmd("which fio", expected_rc=0)
    except Exception as e:
        # logger.warning(e)
        logger.warning("fio not installed.(apt-get install -y fio)")
    return True


def attr_ready():
    try:
        utils.run_cmd("which attr", expected_rc=0)
    except Exception as e:
        # logger.warning(e)
        logger.warning("attr not installed.(apt-get install -y attr)")
    return True


def len_path_in_limit(p, n=128):
    """if path len in limit, return True"""
    return len(p) < n


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pb = PkgBase("/mnt/test")

    def test_benchmark(self):
        self.pb.run_tests(self.pb.tests_generator())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
