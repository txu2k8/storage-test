#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : tc.py
@Time  : 2020/10/26 16:14
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import unittest
from libs.file_ops import Consistency
from pkgs.ltp.fsstress import FSStress
from libs.log import log
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class SanityTC(unittest.TestCase):
    """Sanity test on a mount point or path"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_01_consistency():
        cst = Consistency()
        logger.info(cst.__doc__)
        cst.create('/tmp/consistency/', 500, 1)
        cst.create('/tmp/dir_2', 500, 1)
        cst.compare('/tmp/dir_1', '/tmp/dir_2', 500)

    def test_02_fsstress(self):
        fs_stress = FSStress(TEST_PATH)
        logger.info(fs_stress.__doc__)
        fs_stress.sanity()


class StressTC(unittest.TestCase):
    """Stress test on a mount point or path"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_01_consistency():
        cst = Consistency()
        logger.info(cst.__doc__)
        cst.create('/tmp/consistency/', 500, 1)
        cst.create('/tmp/dir_2', 500, 1)
        cst.compare('/tmp/dir_1', '/tmp/dir_2', 500)

    def test_03_fsstress(self):
        fs_stress = FSStress(TEST_PATH)
        logger.info(fs_stress.__doc__)
        fs_stress.stress()


class LoadGenTC(unittest.TestCase):
    """Generate data on a mount point or path"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_01_consistency():
        cst = Consistency()
        logger.info(cst.__doc__)
        cst.create('/tmp/consistency/', 500, 1)
        cst.create('/tmp/dir_2', 500, 1)
        cst.compare('/tmp/dir_1', '/tmp/dir_2', 500)

    def test_03_fsstress(self):
        fs_stress = FSStress(TEST_PATH)
        logger.info(fs_stress.__doc__)
        fs_stress.stress()



if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
