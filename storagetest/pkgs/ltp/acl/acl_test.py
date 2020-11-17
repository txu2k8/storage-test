#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : acl_test.py
@Time  : 2020/11/9 9:25
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import unittest

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class AclXattr(object):
    """Test ACL and Extend Attribute on Linux system"""
    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)
        try:
            utils.run_cmd("which attr", expected_rc=0)
        except Exception as e:
            logger.error(e)
            raise NoSuchBinary("attr, try install it.(apt-get install -y attr)")

    def run(self, test_path):
        """cd <test_path>; ./tacl_xattr.sh """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)
        acl_bin = os.path.join(bin_path, 'tacl_xattr.sh')
        test_log = os.path.join(self.top_path, 'tacl_xattr.log')
        acl_cmd = "rm -rf {0}/*; cd {0}; {1} | tee {2}".format(test_path, acl_bin, test_log)

        try:
            os.system('chmod +x {0}/*'.format(bin_path))
            rc, output = utils.run_cmd(acl_cmd, expected_rc="ignore")
            logger.info(output)
            if rc != 0:
                raise Exception("tacl_xattr.sh exit with !0")
            if "FAILED:" in output:
                raise Exception("FAIL: test acl_xattr on {}".format(test_path))
            logger.info("PASS: test acl_xattr on {}".format(test_path))
        except Exception as e:
            logger.info("FAIL: test acl_xattr on {}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "acl_attribute")
        assert self.run(test_path)
        return True

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "acl_attribute")
        assert self.run(test_path)
        return True


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.acl = AclXattr("/mnt/test")

    def test_01(self):
        self.acl.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
