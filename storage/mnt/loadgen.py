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
from pkgs.ltp.create import CreateDataFile
from pkgs.ltp.fsstress import FSStress
from pkgs.fio import FIO
from libs.file_ops import Consistency
from libs.log import log
from libs.exceptions import NoSuchDir
from libs.customtest import CustomTestCase
from libs import utils
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class LoadGenTC(CustomTestCase):
    """Generate data on a mount point or path"""
    _fs_path = args.test_path
    _dir_n = args.dir_number
    _file_n = args.file_number
    _file_size_range = args.file_size_range

    @classmethod
    def setUpClass(cls):
        logger.info("Start generate data on {}".format(cls._fs_path))
        if not os.path.isdir(cls._fs_path):
            raise NoSuchDir(cls._fs_path)
        cls.test_path = os.path.join(cls._fs_path, "load")
        utils.mkdir_path(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        logger.info("Generate data on {} complete!".format(cls._fs_path))

    def test_create_files(self):
        """Creates files of specified size"""
        logger.info(self.__doc__)
        cdf = CreateDataFile(self.test_path)
        cdf.verify()
        test_top_path = os.path.join(self.test_path, 'create_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, "dir_{}".format(x))
            f_size_min, f_size_max = utils.strnum_to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cdf.run(test_path, self._file_n, f_size))

    def test_small_files(self):
        """Generate small files by Consistency"""
        logger.info(self.__doc__)
        cst = Consistency()
        test_top_path = os.path.join(self.test_path, 'small_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            f_size_min, f_size_max = utils.strnum_to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cst.create(test_path, self._file_n, f_size))

    def test_empty_files(self):
        """Generate empty files by Consistency"""
        logger.info(self.__doc__)
        cst = Consistency()
        test_top_path = os.path.join(self.test_path, 'small_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            self.assertTrue(cst.create(test_path, self._file_n, 0))

    def test_seq_files(self):
        """Creates files of specified size with sequential write(by fio)TODO"""
        logger.info(self.__doc__)
        fio = FIO()
        logger.info(fio.__doc__)
        test_top_path = os.path.join(self.test_path, 'seq_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            # self.assertTrue(fio.write(test_path, self._file_n))

    def test_fsstress(self):
        """Generate sub dirs/files by fsstress"""
        fs_stress = FSStress(self.test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(LoadGenTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
