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
from datetime import datetime

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtestcase import CustomTestCase
from storagetest.pkgs.base import posix_ready, fio_ready, attr_ready, prove_ready

logger = log.get_logger()


class SanityTC(CustomTestCase):
    """Sanity test on a mount point or path"""

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()
        self.fs_path = self.args[0].test_path
        if not os.path.isdir(self.fs_path):
            raise NoSuchDir(self.fs_path)
        self.test_path = os.path.join(self.fs_path, "sanity_{0}_{1}".format(self.str_time, self.tc_loop[self.id()]))
        utils.mkdir_path(self.test_path)

    # ==== LTP ====
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(attr_ready(), "attr not installed!")
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from storagetest.pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.sanity())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
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
        readall = ReadAll(self.fs_path)
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
    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_dbench(self):
        """A load tester for various protocols such as iSCSI, NFS, SCSI, SMB."""
        from storagetest.pkgs.pts.dbench import Dbench
        db = Dbench(self.test_path)
        logger.info(db.__doc__)
        self.assertTrue(db.sanity())

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
    @unittest.skipUnless(prove_ready(), "perl not installed!")
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
