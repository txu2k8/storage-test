#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sanity.py
@Time  : 2020/11/6 8:43
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import unittest
from libs.file_ops import Consistency
from pkgs.ltp.fs_di import FSDataIntegrity
from pkgs.fstest import FSTest
from pkgs.ltp.locktests import LockTest
from pkgs.ltp.doio import DoIO
from libs.log import log
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class SanityTC(unittest.TestCase):
    """Sanity test on a mount point or path"""
    _test_path = os.path.join(args.test_path, "sanity")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_consistency(self):
        """Test the file consistency"""
        cst = Consistency()
        logger.info(cst.__doc__)
        local_path = '/tmp/consistency'
        test_path = os.path.join(self._test_path, 'consistency')
        self.assertTrue(cst.create(local_path, 500, 1))
        self.assertTrue(cst.create(test_path, 500, 1))
        self.assertTrue(cst.compare(local_path, test_path, 500))

    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        fdi = FSDataIntegrity(self._test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.sanity())

    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        fs_test = FSTest(self._test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.sanity())

    def test_locktests(self):
        """Test fcntl locking functions"""
        lct = LockTest(self._test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.sanity())

    def test_doio(self):
        """base rw test: LTP doio & iogen"""
        dio = DoIO(self._test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.iogen_doio())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
