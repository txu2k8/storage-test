#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fs_di.py
@Time  : 2020/11/5 10:13
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

logger = log.get_logger()


class FSDataIntegrity(object):
    """
    Test FileSystem Data Integrity
    ============
    1. Creates a data file of specified or random size and copies
        the file to a random directory depth on a specified filesystem
        The two files are compared and checked for differences.
        If the files differ, then the test fails. By default, this
        test creates a 30Mb file and runs for ten loops.
    2. Creates a datafile of size half of the partition size. Creates
        two fragmented files on the specified partition and copies datafile
        to them. Then compares both the fragmented files with datafile. If
        files differ, then test fails.
    """
    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def run(self, test_path, f_size, p_size, loops=1):
        """
        usage: ./fs_di -d TMPDIR [-h] [-l # of LOOPS ] [-s SIZE in Mb][-S partition SIZE in Mb]
        -d TMPDIR       Directory where temporary files will be created.
        -h              Help. Prints all available options.
        -l # of LOOPS   The number of times to run the test. Default=10.
        -s SIZE in Mb   The size of the data file to create. Default=30Mb. A "0" means random sizes from 10-500Mb.
        -S SIZE in Mb   Size of usable partition (in MBs) on which the testing is carried out (needs to be passed
                        for fragmented file test)
        -v              Verbose output.
        example: ./fs_di -d /mnt/cifsmount -l 20 -s 100 -S 200
        example: ./fs_di -d /mnt/cifsmount -l 20 -s 100

        """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        bin_path = os.path.join(cur_dir, 'bin')
        fs_di_bin = os.path.join(bin_path, 'fs_di')

        test_log = os.path.join(self.top_path, 'fs_data_integrity.log')
        test_cmd = "{0} -d {1} -l {2} -s {3} -S {4} | tee -a {5}".format(
            fs_di_bin, test_path, loops, f_size, p_size, test_log)

        try:
            os.system('chmod +x {0}/*'.format(bin_path))
            rc, output = utils.run_cmd(test_cmd)
            logger.info('\n'.format(output.strip('\n')))
            if "Test failed" in output:
                raise Exception("FAIL: Run fs_data_integrity on {}".format(test_path))
            logger.info("PASS: Run fs_data_integrity on {}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run fs_data_integrity on {}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fs_data_integrity")
        assert self.run(test_path, 10, 20, 1)
        return True

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fs_data_integrity")
        assert self.run(test_path, 100, 200, 20)
        return True


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fsdi = FSDataIntegrity("/mnt/test")

    def test_01(self):
        self.fsdi.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
