#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : read_all.py
@Time  : 2020/11/6 18:21
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class ReadAll(object):
    """Perform a small read on every file in a directory tree."""

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
        ./read_all -d /mnt/test/ -I 30 -v -h
        Options
        -------
        -h       Prints this help
        -i n     Execute test n times
        -I x     Execute test for n seconds
        -C ARG   Run child process with ARG arguments (used internally)
        -v       Print information about successful reads.
        -q       Don't print file read or open errors.
        -d path  Path to the directory to read from, defaults to /sys.
        -e pattern Ignore files which match an 'extended' pattern, see fnmatch(3).
        -r count The number of times to schedule a file for reading.
        -w count Set the worker count limit, the default is 15.
        -W count Override the worker count. Ignores (-w) and the processor count.
        -p       Drop privileges; switch to the nobody user.

        """
        logger.info(self.run.__doc__)
        utils.mkdir_path(test_path)

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        readall_bin = os.path.join(cur_dir, 'bin/read_all')
        test_log = os.path.join(self.top_path, 'stream.log')
        readall_cmd = "{0} -d {1} -i {2} -I {3} -v | tee {4}".format(
            readall_bin, test_path, loops, runtime, test_log)

        try:
            os.system('chmod +x {0}*'.format(readall_cmd))
            rc, output = utils.run_cmd(readall_cmd)
            logger.info(output)
            if "TFAIL" in output:
                raise Exception("FAIL: Run read_all test on {0}".format(test_path))
            logger.info("PASS: Run read_all test on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run read_all test on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "read_all")
        return self.run(test_path, 5, 10)

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "read_all")
        return self.run(test_path, 10, 60)


if __name__ == '__main__':
    pass
