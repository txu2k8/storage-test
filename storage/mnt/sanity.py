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

from libs import log
from libs import utils
from libs.exceptions import NoSuchDir
from libs.customtest import CustomTestCase
from config import const

logger = log.get_logger()
args = const.get_value('args')


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

    # ==== LTP ====
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.sanity())

    def test_doio(self):
        """base rw test: LTP doio & iogen"""
        from pkgs.ltp.doio import DoIO
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.iogen_doio())

    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        from pkgs.ltp.fs_di import FSDataIntegrity
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.sanity())

    def test_locktests(self):
        """Test fcntl locking functions"""
        from pkgs.ltp.locktests import LockTest
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.sanity())

    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        from pkgs.ltp.read import ReadAll
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.sanity())

    def test_stream(self):
        """LTP file stream test"""
        from pkgs.ltp.stream import StreamTest
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.sanity())

    # ==== Tools ====
    def test_fio(self):
        """FIO: Flexible I/O tester."""
        from pkgs.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.sanity())

    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        from pkgs.fstest import FSTest
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.sanity())

    # ==== Private ====
    def test_consistency(self):
        """Test the file consistency"""
        from pkgs.fileops import Consistency
        cst = Consistency()
        logger.info(cst.__doc__)
        local_path = '/tmp/consistency'
        test_path = os.path.join(self.test_path, 'consistency')
        self.assertTrue(cst.create(local_path, 500, 1))
        self.assertTrue(cst.create(test_path, 500, 1))
        self.assertTrue(cst.compare(local_path, test_path, 500))


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
