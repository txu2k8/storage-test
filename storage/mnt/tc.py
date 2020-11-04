#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : tc.py
@Time  : 2020/10/26 16:14
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from libs.file_ops import Consistency
from pkgs.ltp.fsstress import FSStress
from pkgs.fstest import FSTest
from pkgs.filebench import FileBench
from pkgs.ltp.locktests import LockTest
from pkgs.ltp.doio import DoIO
from libs.log import log
from config import const

logger = log.get_logger()
args = const.get_value('args')

TEST_PATH = args.test_path


class SanityTC(unittest.TestCase):
    """Sanity test on a mount point or path"""
    _test_path = args.test_path

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_consistency(self):
        cst = Consistency()
        logger.info(cst.__doc__)
        local_path = '/tmp/consistency'
        test_path = os.path.join(self._test_path, 'consistency')
        self.assertTrue(cst.create(local_path, 500, 1))
        self.assertTrue(cst.create(test_path, 500, 1))
        self.assertTrue(cst.compare(local_path, test_path, 500))

    def test_fstest(self):
        fs_test = FSTest(self._test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.sanity())

    def test_fsstress(self):
        fs_stress = FSStress(self._test_path)
        logger.info(fs_stress.__doc__)
        self.assertTrue(fs_stress.sanity())

    def test_locktests(self):
        lct = LockTest(self._test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.sanity())


class StressTC(unittest.TestCase):
    """Stress test on a mount point or path"""
    _test_path = args.test_path

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_consistency(self):
        cst = Consistency()
        logger.info(cst.__doc__)
        local_path = '/tmp/consistency'
        self.assertTrue(cst.create(local_path, 1000, 1))
        test_top_path = os.path.join(self._test_path, 'consistency')
        for x in range(0, 100):
            test_path = os.path.join(test_top_path, 'dir{0}'.format(x))
            self.assertTrue(cst.create(test_path, 1000, 1))
            self.assertTrue(cst.compare(local_path, test_path, 1000))

    def test_fstest(self):
        fs_test = FSTest(self._test_path)
        logger.info(fs_test.__doc__)
        self.assertTrue(fs_test.stress())

    def test_fsstress(self):
        fs_stress = FSStress(self._test_path)
        logger.info(fs_stress.__doc__)
        fs_stress.stress()

    def test_filebench(self):
        fb = FileBench(self._test_path)
        logger.info(fb.__doc__)
        self.assertTrue(fb.stress())

    def test_locktests(self):
        lct = LockTest(self._test_path)
        logger.info(lct.__doc__)
        self.assertTrue(lct.stress())

    def test_doiotests(self):
        dio = DoIO(self._test_path)
        logger.info(dio.__doc__)
        self.assertTrue(dio.stress())


class LoadGenTC(unittest.TestCase):
    """Generate data on a mount point or path"""
    _test_path = args.test_path

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
