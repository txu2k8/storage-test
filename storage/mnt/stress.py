#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : stress.py
@Time  : 2020/10/26 16:14
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from libs.file_ops import Consistency
from pkgs.ltp.fs_di import FSDataIntegrity
from pkgs.ltp.fsstress import FSStress
from pkgs.fstest import FSTest
from pkgs.filebench import FileBench
from pkgs.ltp.locktests import LockTest
from pkgs.ltp.doio import DoIO
from pkgs.ltp.stream import StreamTest
from pkgs.ltp.read import ReadAll
from pkgs.ltp.create import CreateDataFile
from libs.log import log
from libs.exceptions import NoSuchDir
from libs.customtest import CustomTestCase
from libs import utils
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class StressTC(CustomTestCase):
    """Stress test on a mount point or path"""
    _fs_path = args.test_path

    @classmethod
    def setUpClass(cls):
        logger.info("Start stress test on {}".format(cls._fs_path))
        if not os.path.isdir(cls._fs_path):
            raise NoSuchDir(cls._fs_path)
        cls.test_path = os.path.join(cls._fs_path, "stress")
        utils.mkdir_path(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        logger.info("Stress test on {} complete!".format(cls._fs_path))

    def test_consistency(self):
        """Test the file consistency"""
        cst = Consistency()
        logger.info(cst.__doc__)
        local_path = '/tmp/consistency'
        self.assertTrue(cst.create(local_path, 1000, 1))
        test_top_path = os.path.join(self.test_path, 'consistency')
        for x in range(0, 100):
            test_path = os.path.join(test_top_path, 'dir{0}'.format(x))
            self.assertTrue(cst.create(test_path, 1000, 1))
            self.assertTrue(cst.compare(local_path, test_path, 1000))

    def test_create_files(self):
        """Creates files of specified size"""
        cdf = CreateDataFile(self.test_path)
        logger.info(cdf.__doc__)
        self.assertTrue(cdf.stress())

    def test_fs_di(self):
        """Test FileSystem Data Integrity"""
        fdi = FSDataIntegrity(self.test_path)
        logger.info(fdi.__doc__)
        self.assertTrue(fdi.stress())

    def test_fstest(self):
        """Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink"""
        fs_test = FSTest(self.test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.stress())

    def test_fsstress(self):
        """filesystem stress with LTP tool fsstress"""
        fs_stress = FSStress(self.test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.stress()

    def test_filebench(self):
        """File System Workload test"""
        fb = FileBench(self.test_path)
        logger.info(fb.__doc__)
        self.assertTrue(fb.stress())

    def test_locktests(self):
        """Test fcntl locking functions"""
        lct = LockTest(self.test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.stress())

    def test_doio(self):
        """base rw test: LTP doio & iogen; growfiles"""
        dio = DoIO(self.test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.rwtest())
        self.assertTrue(dio.growfiles())

    def test_stream(self):
        """LTP file stream test"""
        stream = StreamTest(self.test_path)
        logger.info(stream.__doc__)
        self.assertTrue(stream.stress())

    def test_readall(self):
        """Perform a small read on every file in a directory tree."""
        readall = ReadAll(self.test_path)
        logger.info(readall.__doc__)
        self.assertTrue(readall.stress())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(StressTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
