#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : postmark_test.py
@Time  : 2020/11/2 17:52
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from concurrent.futures import ThreadPoolExecutor

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class PostMark(object):
    """
    PostMark: A Mail server workload
    http://openbenchmarking.org/test/pts/postmark
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("PostMark just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    @staticmethod
    def set_cfg(test_path, cfg_template):
        logger.info('cfg: {0}'.format(cfg_template))
        cfg_name = os.path.split(cfg_template)[-1]
        tmp_path = os.path.join(os.getcwd(), 'tmp')
        utils.mkdir_path(tmp_path)

        test_cfg_name = 'postmark_{0}_{1}'.format(test_path.replace('/', '_'), cfg_name)
        test_cfg = os.path.join(tmp_path, test_cfg_name)
        rc, output = utils.run_cmd('cp {0} {1}'.format(cfg_template, test_cfg))
        print(output)

        # modify the tmp cfg file: dir
        sed_cfg_cmd = "sed -i 's/\/tmp/{test_path}/g' {cfg_file}".format(
            test_path=test_path.replace('/', '\/'), cfg_file=test_cfg)
        rc, output = utils.run_cmd(sed_cfg_cmd)
        print(output)
        return test_cfg

    def run(self, test_path):
        """
        cd /path/to/file/system/you/want/to/test/
        prove -r /path/to/fstest/
        """
        logger.info(self.run.__doc__)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        postmark_bin = os.path.join(cur_dir, 'bin/postmark')
        cfg_template = os.path.join(cur_dir, 'bin/postmark-template.cfg')
        test_log = os.path.join(self.top_path, 'postmark.log')

        test_cfg = self.set_cfg(test_path, cfg_template)
        pm_cmd = '{0} {1} | tee -a {2}'.format(postmark_bin, test_cfg, test_log)

        try:
            os.system('rm -rf %s/{0..10000}' % test_path)
            os.system('chmod +x {0}*'.format(postmark_bin))
            rc, output = utils.run_cmd(pm_cmd, timeout=72000)
            logger.info('\n'.format(output.strip('\n')))
            logger.info("Complete: Run fstest on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run fstest on {0}".format(test_path))
            raise e
        finally:
            utils.run_cmd('rm -rf {0}'.format(test_cfg))

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "postmark")
        utils.mkdir_path(test_path)
        return self.run(test_path)

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "postmark")
        utils.mkdir_path(test_path)
        return self.run(test_path)


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pm = PostMark("/mnt/test")

    def test_01(self):
        self.pm.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
