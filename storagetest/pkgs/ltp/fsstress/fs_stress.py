#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fs_stress.py
@Time  : 2020/10/30 14:58
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from concurrent.futures import ThreadPoolExecutor

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class FSStress(object):
    """Functions for fs stress with binary ltp-fsstress"""

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("fs_test just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def run(self, test_path, nops=100, nproc=10, loops=1):
        """
        -d dir      specifies the base directory for operations
        -n nops     specifies the no. of operations per process (default 1)
        -p nproc    specifies the no. of processes (default 1)
        -l loops    specifies the no. of times the testrun should loop
        -c          specifies not to remove files(cleanup) after execution
        -r          specifies random name padding
        """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        fsstress_bin = os.path.join(cur_dir, 'bin/fsstress')
        test_log = os.path.join(self.top_path, 'fsstress.log')
        fsstress_cmd = "{0} -d {1} -l {2} -n {3} -p {4} -v -w -r -c | tee -a {5}".format(
            fsstress_bin, test_path, str(loops), str(nops),  str(nproc), test_log)

        try:
            os.system('chmod +x {0}*'.format(fsstress_bin))
            rc, output = utils.run_cmd(fsstress_cmd)
            logger.info(output)
            logger.info("PASS: Run fsstress on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run fsstress on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fsstress")
        return self.run(test_path, nops=10, nproc=4, loops=1)

    def stress(self):
        self.verify()
        stress_path = os.path.join(self.top_path, "fsstress")
        pool = ThreadPoolExecutor(max_workers=8)
        futures = []
        for x in range(1, 5):
            test_path = os.path.join(stress_path, "dir_".format(x))
            utils.mkdir_path(test_path)
            futures.append(pool.submit(self.run, test_path, nops=1000, nproc=50, loops=3))
        pool.shutdown()
        future_result = [future.result() for future in futures]
        result = False if False in future_result else True
        return result


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fs_stress = FSStress("/mnt/test")

    def test_01(self):
        self.fs_stress.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
