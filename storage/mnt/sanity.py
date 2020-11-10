#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sanity.py
@Time  : 2020/11/6 8:43
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import time
import unittest
from libs.file_ops import Consistency
from pkgs.ltp.fs_di import FSDataIntegrity
from pkgs.fstest import FSTest
from pkgs.ltp.locktests import LockTest
from pkgs.ltp.doio import DoIO
from pkgs.ltp.stream import StreamTest
from pkgs.ltp.read import ReadAll
from pkgs.ltp.acl import AclXattr
from libs.log import log
from libs import utils
from libs.exceptions import NoSuchDir
from libs.customtest import CustomTestCase
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class SanityTC(CustomTestCase):
    """Sanity test on a mount point or path"""
    _fs_path = args.test_path

    @classmethod
    def setUpClass(cls):
        logger.info("Start sanity test on {}".format(cls._fs_path))
        if not os.path.isdir(cls._fs_path):
            raise NoSuchDir(cls._fs_path)
        str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        cls.test_path = os.path.join(cls._fs_path, "sanity_"+str_time)
        utils.mkdir_path(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        logger.info("Sanity test on {} complete!".format(cls._fs_path))

    def test_consistency(self):
        """Test the file consistency"""
        cst = Consistency()
        logger.info(cst.__doc__)
        local_path = '/tmp/consistency'
        test_path = os.path.join(self.test_path, 'consistency')
        self.assertTrue(cst.create(local_path, 500, 1))
        self.assertTrue(cst.create(test_path, 500, 1))
        self.assertTrue(cst.compare(local_path, test_path, 500))

    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.sanity())

    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.sanity())

    def test_locktests(self):
        """Test fcntl locking functions"""
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.sanity())

    def test_doio(self):
        """base rw test: LTP doio & iogen"""
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.iogen_doio())

    def test_stream(self):
        """LTP file stream test"""
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.sanity())

    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.sanity())

    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
