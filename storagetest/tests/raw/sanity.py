#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sanity.py
@Time  : 2020/11/6 8:43
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import unittest
from datetime import datetime

from storagetest.libs import log
from storagetest.libs.customtestcase import CustomTestCase
from storagetest.pkgs.raw.ut import RawUT

logger = log.get_logger()


class SanityTC(CustomTestCase):
    """RAW device write/read unit test"""

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()
        self.device = self.args[0].device
        self.case_id_list = self.args[0].case_id_list
        self.case_priority_list = self.args[0].case_priority_list

    def test_ut(self):
        """Raw write/read unit test"""
        raw = RawUT(self.device)
        logger.info(raw.__doc__)
        self.assertTrue(raw.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
