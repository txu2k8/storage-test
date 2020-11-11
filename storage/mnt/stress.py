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

from libs import log
from libs import utils
from libs.exceptions import NoSuchDir
from libs.customtest import CustomTestCase
from config import const

logger = log.get_logger()
args = const.get_value('args')


class StressTC(CustomTestCase):
    """Stress test on a mount point or path"""
    _fs_path = args.test_path

    @classmethod
    def setUpClass(cls):
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
    def test_acl(self):
        """Test ACL and Extend Attribute on Linux system"""
        from pkgs.ltp.acl import AclXattr
        acl = AclXattr(self.test_path)
        logger.info(acl.__doc__)
        self.assertTrue(acl.stress())

    def test_create_files(self):
        """Creates files of specified size"""
        from pkgs.ltp.create import CreateDataFile
        cdf = CreateDataFile(self.test_path)
        logger.info(cdf.__doc__)
        self.assertTrue(cdf.stress())

    def test_doio(self):
        """base rw test: LTP doio & iogen; growfiles"""
        from pkgs.ltp.doio import DoIO
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.rwtest())
        self.assertTrue(dio.growfiles())

    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        from pkgs.ltp.fs_di import FSDataIntegrity
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.stress())

    def test_fsstress(self):
        """filesystem stress with LTP tool fsstress"""
        from pkgs.ltp.fsstress import FSStress
        fs_stress = FSStress(self.test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.stress()

    def test_locktests(self):
        """Test fcntl locking functions"""
        from pkgs.ltp.locktests import LockTest
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.stress())

    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        from pkgs.ltp.read import ReadAll
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.stress())

    def test_stream(self):
        """LTP file stream test"""
        from pkgs.ltp.stream import StreamTest
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.stress())

    # ==== Tools ====
    def test_filebench(self):
        """File System Workload test"""
        from pkgs.filebench import FileBench
        fb = FileBench(self.test_path)
        logger.info(fb.__doc__)
        self.assertTrue(fb.stress())

    def test_fio(self):
        """FIO: Flexible I/O tester."""
        from pkgs.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.stress())

    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        from pkgs.fstest import FSTest
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.stress())

    def test_postmark(self):
        """Mail server workload"""
        from pkgs.postmark import PostMark
        pm = PostMark(self.test_path)
        logger.info(pm.__doc__)
        self.assertTrue(pm.stress())

    # ==== Private ====
    def test_consistency(self):
        """Test the file consistency"""
        from pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        logger.info(cst.__doc__)
        self.assertTrue(cst.stress())

    def test_fileops(self):
        """Test the various of file operations"""
        from pkgs.fileops import LocalFileOps
        fops = LocalFileOps(self.test_path)
        logger.info(fops.__doc__)
        self.assertTrue(fops.stress())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(StressTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
