#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : lock_test.py
@Time  : 2020/11/2 16:15
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import unittest

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class LockTest(object):
    """
    lock test: Tries to stress the fcntl locking functions.
    https://github.com/linux-test-project/ltp/tree/master/testcases/network/nfsv4/locks
    EXPECTED RESULTS
    ================
    Here is the table of expected results, depending on :
     - Slave test operations (READ, WRITE, SET A WRITE LOCK ... )
     - Master Operation (SET A READ/A WRITE LOCK )
     - Slave types (Processes, threads)
     - Locking profile (POSIX locking, Mandatory locking)
    =====================================================================================================
                                        |                       Master  process/thread                  |
    ====================================|===============================================================|
    Slave type   |   Test operation     |    advisory         locking    |   mandatory        locking   |
    ____________________________________|________________________________|______________________________|
                 |                      |    read lock       write lock  |   read lock       write lock |
    ____________________________________|________________________________|______________________________|
    thread       |   set a read lock    |     Allowed         Allowed    |    Allowed         Allowed   |
                 |   set a write lock   |     Allowed         Allowed    |    Allowed         Allowed   |
                 |   read               |     Allowed         Allowed    |    Allowed         Allowed   |
                 |   write              |     Allowed         Allowed    |    Allowed         Allowed   |
    ====================================+================================+==============================|
    process      |   set a read lock    |     Allowed         Denied     |    Allowed         Denied    |
                 |   set a write lock   |     Denied          Denied     |    Denied          Denied    |
                 |   read               |     Allowed         Allowed    |    Denied          Allowed   |
                 |   write              |     Allowed         Allowed    |    Denied          Denied    |
    =====================================================================================================
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("fs_test just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def run(self, test_path):
        """
        RUN LOCAL:
        ./locktests -n <number of concurent process> -f <test file> [-T]
        eg:
        ./locktests -n 50 -f /file/system/to/test
        """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        locktest_bin = os.path.join(cur_dir, 'bin/locktests')
        test_log = os.path.join(self.top_path, 'locktests.log')
        locktest_cmd = '{0} -n 50 -f {1}/locktest.dat | tee -a {2}'.format(
            locktest_bin, test_path, test_log)

        try:
            os.system('chmod +x {0}*'.format(locktest_bin))
            rc, output = utils.run_cmd(locktest_cmd)
            logger.info(output)
            logger.info("Complete: Run locktests on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run locktests on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "locktests")
        return self.run(test_path)

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "locktests")
        return self.run(test_path)


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.lct = LockTest("/mnt/test")

    def test_01(self):
        self.lct.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
