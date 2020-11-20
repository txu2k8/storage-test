#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : benchmark.py
@Time  : 2020/11/12 11:10
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import unittest
from datetime import datetime

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtestcase import CustomTestCase
from storagetest.pkgs.base import posix_ready, fio_ready

logger = log.get_logger()


class BenchMarkTC(CustomTestCase):
    """BenchMark test on a mount point or path"""

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()
        fs_path = self.args[0].test_path
        if not os.path.isdir(fs_path):
            raise NoSuchDir(fs_path)
        self.test_path = os.path.join(fs_path, "benchmark_{0}_{1}".format(self.str_time, self.tc_loop[self.id()]))
        utils.mkdir_path(self.test_path)

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
        self.assertTrue(cb.benchmark())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_dbench(self):
        """A load tester for various protocols such as iSCSI, NFS, SCSI, SMB."""
        from storagetest.pkgs.pts.dbench import Dbench
        db = Dbench(self.test_path)
        logger.info(db.__doc__)
        self.assertTrue(db.benchmark())

    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(fio_ready(), "fio not installed!")
    def test_fio(self):
        """Flexible I/O tester"""
        from storagetest.pkgs.pts.fio import FIO
        fio = FIO(self.test_path)
        logger.info(fio.__doc__)
        self.assertTrue(fio.google_benchmark())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fs_mark(self):
        """A benchmark tests for synchronous write workloads"""
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
        self.assertTrue(ioz.benchmark())

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_postmark(self):
        """Simulate small-file testing similar to the tasks endured by web and mail servers"""
        from storagetest.pkgs.pts.postmark import PostMark
        pm = PostMark(self.test_path)
        logger.info(pm.__doc__)
        self.assertTrue(pm.benchmark())

    # ==== Private ====
    def test_consistency(self):
        """File consistency test"""
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        logger.info(cst.__doc__)
        self.assertTrue(cst.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(BenchMarkTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
