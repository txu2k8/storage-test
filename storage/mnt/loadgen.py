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
from libs.file_ops import Consistency
from libs.log import log
from libs import utils
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class LoadGenTC(unittest.TestCase):
    """Generate data on a mount point or path"""
    _test_path = os.path.join(args.test_path, "sanity")
    _dir_n = args.dir_number
    _file_n = args.file_number
    _file_size_range = args.file_size_range

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_files(self):
        """
        Creates files of specified size
        """
        logger.info(self.__doc__)
        cdf = CreateDataFile(self._test_path)
        cdf.verify()
        test_top_path = os.path.join(self._test_path, 'create_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, "dir_{}".format(x))
            f_size_min, f_size_max = utils.strnum_to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cdf.run(test_path, self._file_n, f_size))

    def test_small_files(self):
        """
        Generate small files by Consistency
        """
        logger.info(self.__doc__)
        cst = Consistency()
        test_top_path = os.path.join(self._test_path, 'small_files')
        for x in range(0, self._dir_n):
            test_path = os.path.join(test_top_path, 'dir_{0}'.format(x))
            f_size_min, f_size_max = utils.strnum_to_int_list(self._file_size_range)
            f_size = random.randint(f_size_min, f_size_max)
            self.assertTrue(cst.create(test_path, self._file_n, f_size))

    def test_fsstress(self):
        fs_stress = FSStress(self._test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(LoadGenTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
