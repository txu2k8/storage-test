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
from pkgs import posix_ready, fio_ready, attr_ready
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
    @unittest.skipUnless(posix_ready() and attr_ready(), "Not supported platform or attr not installed!")
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_doio(self):
        """base rw test: LTP doio & iogen"""
        from pkgs.ltp.doio import DoIO
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.iogen_doio())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        from pkgs.ltp.fs_di import FSDataIntegrity
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_locktests(self):
        """Test fcntl locking functions"""
        from pkgs.ltp.locktests import LockTest
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        from pkgs.ltp.read import ReadAll
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_stream(self):
        """LTP file stream test"""
        from pkgs.ltp.stream import StreamTest
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.sanity())

    # ==== Tools ====
    @unittest.skipUnless(posix_ready() and fio_ready(), "Not supported platform or fio not installed!")
    def test_fio(self):
        """FIO: Flexible I/O tester."""
        from pkgs.pts.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        from pkgs.fstest import FSTest
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_postmark(self):
        """Simulate small-file testing similar to the tasks endured by web and mail servers"""
        from pkgs.pts.postmark import PostMark
        pm = PostMark(self.test_path)
        logger.info(pm.__doc__)
        self.assertTrue(pm.sanity())

    # ==== Private ====
    def test_consistency(self):
        """Test the file consistency"""
        from pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        logger.info(cst.__doc__)
        self.assertTrue(cst.sanity())

    def test_fileops(self):
        """Test the various of file operations"""
        from pkgs.fileops import LocalFileOps
        fops = LocalFileOps(self.test_path)
        logger.info(fops.__doc__)
        self.assertTrue(fops.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
