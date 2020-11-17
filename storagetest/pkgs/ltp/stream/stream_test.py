#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : stream_test.py
@Time  : 2020/11/6 17:55
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class StreamTest(object):
    """
    stream01: freopen()
    stream02: fseek() mknod() fopen()
    stream03: fseek() ftell()
    stream04: fwrite() fread()
    stream05: ferror() feof() clearerr() fileno()
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def run(self, test_path, loops=5, runtime=10):
        """
        Usage:
        -h      Show this help screen
        -i n    Execute test n times
        -I x    Execute test for x seconds
        """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        bin_path = os.path.join(cur_dir, 'bin')
        test_log = os.path.join(self.top_path, 'stream.log')

        try:
            os.system('chmod +x {0}/*'.format(bin_path))
            for x in range(1, 6):
                stream_bin = os.path.join(bin_path, 'stream0{}'.format(x))
                stream_cmd = "cd {0}; {1} -i {2} -I {3} | tee {4}".format(
                    test_path, stream_bin, loops, runtime, test_log)
                rc, output = utils.run_cmd(stream_cmd)
                logger.info(output)
                if "TFAIL" in output:
                    raise Exception("FAIL: Run stream0{0} test on {1}".format(x, test_path))
            logger.info("PASS: Run stream test on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run stream test on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "stream")
        return self.run(test_path, 5, 10)

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "stream")
        return self.run(test_path, 10, 60)


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.st = StreamTest("/mnt/test")

    def test_01(self):
        self.st.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
