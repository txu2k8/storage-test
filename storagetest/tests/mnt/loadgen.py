#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : loadgen.py
@Time  : 2020/11/6 8:42
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import random
import unittest
from datetime import datetime

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtestcase import CustomTestCase
from storagetest.pkgs.base import posix_ready, fio_ready

logger = log.get_logger()


class LoadGenTC(CustomTestCase):
    """Generate data on a mount point or path"""

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()
        fs_path = self.args[0].test_path
        self.dir_n = self.args[0].dir_number
        self.file_n = self.args[0].file_number
        self.file_size_range = self.args[0].file_size_range
        if not os.path.isdir(fs_path):
            raise NoSuchDir(fs_path)
        self.test_path = os.path.join(fs_path, "load_{0}_{1}".format(self.str_time, self.tc_loop[self.id()]))
        utils.mkdir_path(self.test_path)

    def test_empty_files(self):
        """Generate empty files by Consistency"""
        logger.info(self.test_empty_files.__doc__)
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        cst.verify()
        test_top_path = os.path.join(self.test_path, 'empty_files')
        for x in range(0, self.dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            self.assertTrue(cst.create(test_path, self.file_n, 0))

    def test_small_files(self):
        """Generate small files by Consistency"""
        logger.info(self.test_small_files.__doc__)
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        cst.verify()
        test_top_path = os.path.join(self.test_path, 'small_files')
        for x in range(0, self.dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            f_size_min, f_size_max = utils.to_int_list(self.file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cst.create(test_path, self.file_n, f_size))

    def test_large_files(self):
        """Generate large files by LocalFileOps"""
        logger.info(self.test_large_files.__doc__)
        from storagetest.pkgs.fileops import LocalFileOps
        fops = LocalFileOps(self.test_path)
        test_top_path = os.path.join(self.test_path, 'large_files')
        for x in range(0, self.dir_n):
            dir_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            utils.mkdir_path(dir_path)
            for n in range(0, self.file_n):
                file_path = os.path.join(dir_path, 'file-{0}.dat'.format(x))
                f_size_min, f_size_max = utils.to_int_list(self.file_size_range)
                self.assertTrue(fops.create_large_size_file(file_path, f_size_max))

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_create_files(self):
        """Creates files of specified size"""
        logger.info(self.test_create_files.__doc__)
        from storagetest.pkgs.ltp.create import CreateDataFile
        cdf = CreateDataFile(self.test_path)
        cdf.verify()
        test_top_path = os.path.join(self.test_path, 'create_files')
        for x in range(0, self.dir_n):
            test_path = os.path.join(test_top_path, "dir_{}".format(x))
            f_size_min, f_size_max = utils.to_int_list(self.file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cdf.run(test_path, self.file_n, f_size))

    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(fio_ready(), "fio not installed!")
    def test_seq_files(self):
        """Generate sequential files of specified size by fio"""
        logger.info(self.test_empty_files.__doc__)
        from storagetest.pkgs.pts.fio import FIO
        for x in range(0, self.dir_n):
            f_size_min, f_size_max = utils.to_int_list(self.file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            fio = FIO(os.path.join(self.test_path, 'seq_files_dir_{0}'.format(x)))
            self.assertTrue(fio.seq_write(self.file_n, str(f_size)))

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_fsstress(self):
        """Generate sub dirs/files by fsstress"""
        logger.info(self.test_fsstress.__doc__)
        from storagetest.pkgs.ltp.fsstress import FSStress
        fs_stress = FSStress(self.test_path)
        fs_stress.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(LoadGenTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
