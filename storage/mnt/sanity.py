#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : sanity.py
@Time  : 2020/10/26 16:14
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import unittest
from libs.file_ops import Consistency


class MntSanityTC(unittest.TestCase):
    """Sanity test.sh on a mount ponit or path"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_consistency(self):
        cst = Consistency()
        print(cst.__doc__)
        cst.create('/tmp/consistency/', 500, 1)
        cst.create('/tmp/dir_2', 500, 1)
        cst.compare('/tmp/dir_1', '/tmp/dir_2', 500)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(FileOpsTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
