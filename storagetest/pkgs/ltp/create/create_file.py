#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : create_file.py
@Time  : 2020/11/6 9:38
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import random
import unittest
from concurrent.futures import ThreadPoolExecutor

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

logger = log.get_logger()


class CreateDataFile(object):
    """Creates a file of specified size."""
    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def run(self, test_path, f_num, f_size):
        """
        create_file <# of 1048576 buffers to write> <name of file to create>
        ex. # create_file 10 /tmp/testfile
        f_size: MB
        """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        bin_path = os.path.join(cur_dir, 'bin')
        cdf_bin = os.path.join(bin_path, 'create_datafile')

        try:
            os.system('chmod +x {0}/*'.format(bin_path))
            pool = ThreadPoolExecutor(max_workers=8)
            futures = []
            for x in range(0, f_num):
                f_name = os.path.join(test_path, "file_{}".format(x))
                test_cmd = "{0} {1} {2}".format(cdf_bin, f_size, f_name)
                futures.append(pool.submit(utils.run_cmd, test_cmd, expected_rc='ignore'))
            pool.shutdown()
            future_result = [future.result()[0] for future in futures]
            result = False if -1 in future_result else True
            assert result
            logger.info("PASS: create {0} datafile on {1}".format(f_num, test_path))
        except Exception as e:
            logger.info("FAIL: create datafile on {}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        """1dir*200files*(1MB)*"""
        self.verify()
        test_path = os.path.join(self.top_path, "create_file")
        assert self.run(test_path, 200, 1)
        return True

    def stress(self, dir_n=100):
        """100dirs*100files*(1~100MB)*"""
        self.verify()
        test_top_path = os.path.join(self.top_path, 'create_files')
        for x in range(0, dir_n):
            test_path = os.path.join(test_top_path, "dir_{}".format(x))
            utils.mkdir_path(test_path)
            assert self.run(test_path, 100, random.randint(1, 100))
        return True


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.cd = CreateDataFile("/mnt/test")

    def test_01(self):
        self.cd.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
