#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sanity.py
@Time  : 2020/10/26 15:12
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from datetime import datetime

from storagetest.libs import utils, log
from storagetest.libs.exceptions import NoSuchDir
from storagetest.libs.customtestcase import CustomTestCase
from storagetest.pkgs.base import posix_ready

logger = log.get_logger()


class SanityTC(CustomTestCase):
    """Sanity test on a mount point or path"""

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()
        fs_path = self.args[0].test_path
        if not os.path.isdir(fs_path):
            raise NoSuchDir(fs_path)
        self.test_path = os.path.join(fs_path, "sanity_{0}_{1}".format(self.str_time, self.tc_loop[self.id()]))
        utils.mkdir_path(self.test_path)

    # ==== LTP ====
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    def test_01(self):
        """Test DESC: TODO"""
        logger.info(self.test_01.__doc__)
        self.assertTrue(True)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
