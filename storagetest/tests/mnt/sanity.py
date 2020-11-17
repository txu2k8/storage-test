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

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtest import CustomTestCase
from storagetest.pkgs.base import posix_ready, fio_ready, attr_ready
from config import const

logger = log.get_logger()


class SanityTC(CustomTestCase):
    """Sanity test on a mount point or path"""
    _fs_path = ""

    @classmethod
    def setUpClass(cls):
        args = const.get_value('args')
        cls._fs_path = args.test_path

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
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(attr_ready(), "attr not installed!")
    @unittest.skip("Skip this test temporary ...")
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from storagetest.pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    @unittest.skip("Skip this test temporary ...")
    def test_doio(self):
        """base rw test: LTP doio & iogen"""
        from storagetest.pkgs.ltp.doio import DoIO
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.iogen_doio())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        from storagetest.pkgs.ltp.fs_di import FSDataIntegrity
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_locktests(self):
        """Test fcntl locking functions"""
        from storagetest.pkgs.ltp.locktests import LockTest
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        from storagetest.pkgs.ltp.read import ReadAll
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_stream(self):
        """LTP file stream test"""
        from storagetest.pkgs.ltp.stream import StreamTest
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.sanity())

    # ==== PTS ====
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(fio_ready(), "fio not installed!")
    def test_fio(self):
        """FIO: Flexible I/O tester."""
        from storagetest.pkgs.pts.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_postmark(self):
        """Simulate small-file testing similar to the tasks endured by web and mail servers"""
        from storagetest.pkgs.pts.postmark import PostMark
        pm = PostMark(self.test_path)
        logger.info(pm.__doc__)
        self.assertTrue(pm.sanity())

    # ==== Tools/Private ====
    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        from storagetest.pkgs.fstest import FSTest
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.sanity())

    def test_consistency(self):
        """Test the file consistency"""
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        logger.info(cst.__doc__)
        self.assertTrue(cst.sanity())

    def test_fileops(self):
        """Test the various of file operations"""
        from storagetest.pkgs.fileops import LocalFileOps
        fops = LocalFileOps(self.test_path)
        logger.info(fops.__doc__)
        self.assertTrue(fops.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
