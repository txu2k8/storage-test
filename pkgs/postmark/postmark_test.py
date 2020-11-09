#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : postmark_test.py
@Time  : 2020/11/2 17:52
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from concurrent.futures import ThreadPoolExecutor

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class PostMark(object):
    """
    PostMark: A Mail server workload
    http://openbenchmarking.org/test/pts/postmark
    TODO
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
        cd /path/to/file/system/you/want/to/test/
        prove -r /path/to/fstest/
        """
        logger.info(self.run.__doc__)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        fstest_bin = os.path.join(cur_dir, 'fstest')
        test_log = os.path.join(self.top_path, 'fstest.log')

        fstest_cmd = 'cd {0}; prove -r {1} | tee -a {2}'.format(
            test_path, fstest_bin, test_log)

        try:
            os.system('chmod +x {0}*'.format(fstest_bin))
            rc, output = utils.run_cmd(fstest_cmd)
            logger.info('\n'.format(output.strip('\n')))
            logger.info("Complete: Run fstest on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run fstest on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fstest", "sanity")
        utils.mkdir_path(test_path)
        return self.run(test_path)

    def stress(self):
        self.verify()
        stress_path = os.path.join(self.top_path, "fstest", "stress")
        pool = ThreadPoolExecutor(max_workers=4)
        futures = []
        for x in range(1, 50):
            test_path = os.path.join(stress_path, str(x))
            utils.mkdir_path(test_path)
            futures.append(pool.submit(self.run, test_path))
        pool.shutdown()
        future_result = [future.result() for future in futures]
        result = False if False in future_result else True
        return result


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pm = PostMark("/mnt/test")

    def test_01(self):
        self.pm.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
