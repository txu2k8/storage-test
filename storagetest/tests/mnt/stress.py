#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : stress.py
@Time  : 2020/10/26 16:14
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import time
import unittest

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtest import CustomTestCase
from storagetest.pkgs.base import posix_ready, fio_ready, attr_ready, filebench_ready
from config import const

logger = log.get_logger()


class StressTC(CustomTestCase):
    """Stress test on a mount point or path"""
    _fs_path = ""

    @classmethod
    def setUpClass(cls):
        args = const.get_value('args')
        cls._fs_path = args.test_path

        logger.info("Start stress test on {}".format(cls._fs_path))
        if not os.path.isdir(cls._fs_path):
            raise NoSuchDir(cls._fs_path)
        str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        cls.test_path = os.path.join(cls._fs_path, "stress_"+str_time)
        utils.mkdir_path(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        logger.info("Stress test on {} complete!".format(cls._fs_path))

    # ==== LTP ====
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(attr_ready(), "attr not installed!")
    @unittest.skip("Skip this test temporary ...")
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from storagetest.pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.stress())

    def test_create_files(self):
        """Creates files of specified size"""
        from storagetest.pkgs.ltp.create import CreateDataFile
        cdf = CreateDataFile(self.test_path)
        logger.info(cdf.__doc__)
        self.assertTrue(cdf.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    @unittest.skip("Skip this test temporary ...")
    def test_doio(self):
        """base rw test: LTP doio & iogen; growfiles"""
        from storagetest.pkgs.ltp.doio import DoIO
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.rwtest())
        self.assertTrue(dio.growfiles())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        from storagetest.pkgs.ltp.fs_di import FSDataIntegrity
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fsstress(self):
        """filesystem stress with LTP tool fsstress"""
        from storagetest.pkgs.ltp.fsstress import FSStress
        fs_stress = FSStress(self.test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.stress()

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_locktests(self):
        """Test fcntl locking functions"""
        from storagetest.pkgs.ltp.locktests import LockTest
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        from storagetest.pkgs.ltp.read import ReadAll
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_stream(self):
        """LTP file stream test"""
        from storagetest.pkgs.ltp.stream import StreamTest
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.stress())

    # ==== PTS ====
    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_aio(self):
        """a-synchronous I/O benchmark"""
        from storagetest.pkgs.pts.aio import AioStress
        aio = AioStress(self.test_path)
        logger.info(aio.__doc__)
        self.assertTrue(aio.benchmark())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_compilebench(self):
        """Simulating disk IO common in creating, compiling, patching, stating and reading kernel trees."""
        from storagetest.pkgs.pts.compilebench import CompileBench
        cb = CompileBench(self.test_path)
        logger.info(cb.__doc__)
        self.assertTrue(cb.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(fio_ready(), "fio not installed!")
    @unittest.skip("Skip this test temporary ...")
    def test_fio(self):
        """FIO: Flexible I/O tester."""
        from storagetest.pkgs.pts.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fs_mark(self):
        """The fs_mark benchmark tests synchronous write workloads"""
        from storagetest.pkgs.pts.fs_mark import FSMark
        fm = FSMark(self.test_path)
        logger.info(fm.__doc__)
        self.assertTrue(fm.benchmark())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_iozone(self):
        """A benchmark tests for generates and measures a variety of file operations."""
        from storagetest.pkgs.pts.iozone import IOzone
        ioz = IOzone(self.test_path)
        logger.info(ioz.__doc__)
        self.assertTrue(ioz.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_postmark(self):
        """Simulate small-file testing similar to the tasks endured by web and mail servers"""
        from storagetest.pkgs.pts.postmark import PostMark
        pm = PostMark(self.test_path)
        logger.info(pm.__doc__)
        self.assertTrue(pm.stress())

    # ==== Tools/Private ====
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(filebench_ready(), "filebench not installed!")
    def test_filebench(self):
        """File System Workload test"""
        from storagetest.pkgs.filebench import FileBench
        fb = FileBench(self.test_path)
        logger.info(fb.__doc__)
        self.assertTrue(fb.stress())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        from storagetest.pkgs.fstest import FSTest
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.stress())

    def test_consistency(self):
        """Test the file consistency"""
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        logger.info(cst.__doc__)
        self.assertTrue(cst.stress())

    def test_fileops(self):
        """Test the various of file operations"""
        from storagetest.pkgs.fileops import LocalFileOps
        fops = LocalFileOps(self.test_path)
        logger.info(fops.__doc__)
        self.assertTrue(fops.stress())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(StressTC)
    unittest.TextTestRunner(verbosity=2).run(suite)