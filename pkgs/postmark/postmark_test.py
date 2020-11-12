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
cur_dir = os.path.dirname(os.path.realpath(__file__))


class PostMark(object):
    """
    PostMark
    Simulate small-file testing similar to the tasks endured by web and mail servers
    FYI: http://openbenchmarking.org/test/pts/postmark
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("PostMark just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def run(self, test_path, test_profile):
        """
        Run postmark command
        Args:
            test_path: A path for test(pm> set location)
            test_profile: A specified test profile, *.pmrc, if None,use default

        Returns:
            True or raise Exception
        """
        logger.info(self.run.__doc__)
        if not os.path.exists(test_profile):
            raise Exception("{} not exist".format(test_profile))
        utils.mkdir_path(test_path)
        postmark_bin = os.path.join(cur_dir, 'bin/postmark')
        test_log = os.path.join(self.top_path, 'postmark.log')

        pm_cmd = 'cd {0}; {1} {2} | tee -a {3}'.format(test_path, postmark_bin, test_profile, test_log)

        try:
            os.system('rm -rf %s/{0..10000}' % test_path)
            os.system('chmod +x {0}*'.format(postmark_bin))
            rc, output = utils.run_cmd(pm_cmd, timeout=72000)
            logger.info(output)
            logger.info("Complete: Run postmark on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run postmark on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        """
        PostMark For Disk Transaction Sanity Test(default profile)
        """
        self.verify()
        test_path = os.path.join(self.top_path, "postmark")
        test_profile = os.path.join(cur_dir, 'test_profiles/sanity.pmrc')
        return self.run(test_path, test_profile)

    def stress(self):
        """
        PostMark For Disk Transaction Stress Test
        """
        self.verify()
        test_path = os.path.join(self.top_path, "postmark")
        test_profile = os.path.join(cur_dir, 'test_profiles/stress.pmrc')
        return self.run(test_path, test_profile)

    def benchmark(self):
        """
        PostMark For Disk Transaction Performance Test
        Description:
            This is a test of NetApp's PostMark benchmark designed to
            simulate small-file testing similar to the tasks endured
            by web and mail servers.
            This test profile will set PostMark to perform 25,000 transactions
            with 500 files simultaneously with the file sizes ranging between
            5 and 512 kilobytes.
        Returns: True

        """
        logger.info(self.benchmark.__doc__)
        self.verify()
        test_path = os.path.join(self.top_path, "postmark")
        test_profile = os.path.join(cur_dir, 'test_profiles/benchmark.pmrc')
        return self.run(test_path, test_profile)


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pm = PostMark("/mnt/test")

    def test_01(self):
        self.pm.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
