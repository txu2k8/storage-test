#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : loadgen.py
@Time  : 2020/11/6 8:42
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import time
import random
import unittest

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtest import CustomTestCase
from storagetest.pkgs.base import posix_ready, fio_ready
from config import const

logger = log.get_logger()


class LoadGenTC(CustomTestCase):
    """Generate data on a mount point or path"""
    _fs_path = ""
    _dir_n = 0
    _file_n = 0
    _file_size_range = ""

    @classmethod
    def setUpClass(cls):
        args = const.get_value('args')
        cls._fs_path = args.test_path
        cls._dir_n = args.dir_number
        cls._file_n = args.file_number
        cls._file_size_range = args.file_size_range

        logger.info("Start generate data on {}".format(cls._fs_path))
        if not os.path.isdir(cls._fs_path):
            raise NoSuchDir(cls._fs_path)
        str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        cls.test_path = os.path.join(cls._fs_path, "load_"+str_time)
        utils.mkdir_path(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        logger.info("Generate data on {} complete!".format(cls._fs_path))

    def test_empty_files(self):
        """Generate empty files by Consistency"""
        logger.info(self.test_empty_files.__doc__)
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        cst.verify()
        test_top_path = os.path.join(self.test_path, 'empty_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            self.assertTrue(cst.create(test_path, self._file_n, 0))

    def test_small_files(self):
        """Generate small files by Consistency"""
        logger.info(self.test_small_files.__doc__)
        from storagetest.pkgs.fileops import Consistency
        cst = Consistency(self.test_path)
        cst.verify()
        test_top_path = os.path.join(self.test_path, 'small_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            f_size_min, f_size_max = utils.to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cst.create(test_path, self._file_n, f_size))

    def test_large_files(self):
        """Generate large files by LocalFileOps"""
        logger.info(self.test_large_files.__doc__)
        from storagetest.pkgs.fileops import LocalFileOps
        fops = LocalFileOps(self.test_path)
        test_top_path = os.path.join(self.test_path, 'large_files')
        for x in range(0, self._dir_n):
            dir_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            utils.mkdir_path(dir_path)
            for n in range(0, self._file_n):
                file_path = os.path.join(dir_path, 'file-{0}.dat'.format(x))
                f_size_min, f_size_max = utils.to_int_list(self._file_size_range)
                self.assertTrue(fops.create_large_size_file(file_path, f_size_max))

    @unittest.skipUnless(posix_ready(), "Not supported platform!")
    def test_create_files(self):
        """Creates files of specified size"""
        logger.info(self.test_create_files.__doc__)
        from storagetest.pkgs.ltp.create import CreateDataFile
        cdf = CreateDataFile(self.test_path)
        cdf.verify()
        test_top_path = os.path.join(self.test_path, 'create_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, "dir_{}".format(x))
            f_size_min, f_size_max = utils.to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cdf.run(test_path, self._file_n, f_size))

    @unittest.skipUnless(posix_ready(), "Not supported platform")
    @unittest.skipUnless(fio_ready(), "fio not installed!")
    def test_seq_files(self):
        """Generate sequential files of specified size by fio"""
        logger.info(self.test_empty_files.__doc__)
        from storagetest.pkgs.pts.fio import FIO
        for x in range(0, self._dir_n):
            f_size_min, f_size_max = utils.to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            fio = FIO(os.path.join(self.test_path, 'seq_files_dir_{0}'.format(x)))
            self.assertTrue(fio.seq_write(self._file_n, str(f_size)))

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