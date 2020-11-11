#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sanity.py
@Time  : 2020/11/6 8:43
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import unittest

from libs import log
from libs.customtest import CustomTestCase
from pkgs.raw.ut import RawUT
from config import const

logger = log.get_logger()
args = const.get_value('args')


class SanityTC(CustomTestCase):
    """RAW device write/read unit test"""
    _device = args.device
    _case_id_list = args.case_id_list
    _case_priority_list = args.case_priority_list

    @classmethod
    def setUpClass(cls):
        logger.info("Start sanity test on raw device {}".format(cls._device))

    @classmethod
    def tearDownClass(cls):
        logger.info("Sanity test on raw device {} complete!".format(cls._device))

    def test_ut(self):
        """Raw write/read unit test"""
        raw = RawUT(self._device)
        logger.info(raw.__doc__)
        self.assertTrue(raw.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
