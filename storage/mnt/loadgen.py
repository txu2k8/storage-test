#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : loadgen.py
@Time  : 2020/11/6 8:42
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from libs.file_ops import Consistency
from pkgs.ltp.fsstress import FSStress
from pkgs.filebench import FileBench
from libs.log import log
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class LoadGenTC(unittest.TestCase):
    """Generate data on a mount point or path"""
    _test_path = args.test_path

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_files(self):
        """
        Generate files
        """
        logger.info(self.__doc__)
        cst = Consistency()
        test_top_path = os.path.join(self._test_path, 'small_files')
        for x in range(0, 10):
            test_path = os.path.join(test_top_path, 'dir{0}'.format(x))
            self.assertTrue(cst.create(test_path, 10, 1))

    def test_gen_small_files(self):
        """
        Generate small files
        """
        logger.info(self.__doc__)
        cst = Consistency()
        test_top_path = os.path.join(self._test_path, 'small_files')
        for x in range(0, 10):
            test_path = os.path.join(test_top_path, 'dir{0}'.format(x))
            self.assertTrue(cst.create(test_path, 10, 1))

    def test_gen_by_fsstress(self):
        fs_stress = FSStress(self._test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.sanity()

    def test_gen_by_filebench(self):
        fb = FileBench(self._test_path)
        logger.info(fb.__doc__)
        self.assertTrue(fb.stress())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(LoadGenTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
