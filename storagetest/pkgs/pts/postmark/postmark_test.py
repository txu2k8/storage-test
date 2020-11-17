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

from storagetest.libs.log import log
from storagetest.pkgs.base import TestProfile, PkgBase, to_safe_name

# --- Global Value
logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class PostMark(PkgBase):
    """
    PostMark
    Simulate small-file testing similar to the tasks endured by web and mail servers
    FYI: http://openbenchmarking.org/test/pts/postmark
    """

    def __init__(self, top_path):
        super(PostMark, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "postmark")

    def test_generator(self, test_profile):
        """Return a spec PostMark test"""
        pm_bin = os.path.join(bin_path, 'postmark')
        test_profile_name = os.path.basename(test_profile)
        desc = "{}: Simulate small-file testing".format(test_profile_name.split(".")[0])
        test_name = "postmark_{0}".format(to_safe_name(desc))
        test = TestProfile(
            name=test_name,
            desc=desc,
            test_path=self.test_path,
            bin_path=bin_path,
            command="cd {0}; {1} {2}".format(self.test_path, pm_bin, test_profile))

        return test

    def sanity(self):
        """
        PostMark For Disk Transaction Sanity Test(default profile)
        """
        test_profile = os.path.join(cur_dir, 'test_profiles/sanity.pmrc')
        return self.run(self.test_generator(test_profile))

    def stress(self):
        """
        PostMark For Disk Transaction Stress Test
        """
        test_profile = os.path.join(cur_dir, 'test_profiles/stress.pmrc')
        return self.run(self.test_generator(test_profile))

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
        test_profile = os.path.join(cur_dir, 'test_profiles/benchmark.pmrc')
        return self.run(self.test_generator(test_profile))


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pm = PostMark("/mnt/test")

    def test_01(self):
        self.pm.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
