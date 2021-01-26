#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : smbtorture.py
@Time  : 2021/1/26 15:21
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
    """Sanity test"""

    def setUp(self):
        self.phase_list.append([self.id().split('.')[-1], "Start", '', self.shortDescription()])
        self.start_time = datetime.now()
        self.print_phase()
        fs_path = self.args[0].test_path
        if not os.path.isdir(fs_path):
            raise NoSuchDir(fs_path)
        self.test_path = os.path.join(fs_path, "sanity_{0}_{1}".format(self.str_time, self.tc_loop[self.id()]))
        utils.mkdir_path(self.test_path)
        self.smb_server = self.args[0].smb_server
        self.smb_user = self.args[0].smb_user
        self.smb_pwd = self.args[0].smb_pwd
        self.case_filter = self.args[0].case_filter
        self.expect_failures = []

    # ==== smbtorture ====
    @unittest.skipUnless(posix_ready(), "Not supported platform")
    def test_smbtorture(self):
        """Samba torture test suite"""
        from storagetest.pkgs.smb.smbtorture import SMBTorture
        smb = SMBTorture(self.test_path, self.smb_server, self.smb_user, self.smb_pwd,
                         self.case_filter, self.expect_failures)
        logger.info(smb.__doc__)
        self.assertTrue(smb.sanity())


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTC)
    unittest.TextTestRunner(verbosity=2).run(suite)
