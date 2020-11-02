#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fs_stress.py
@Time  : 2020/10/30 14:58
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
from concurrent.futures import ThreadPoolExecutor

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir

# --- Global Value
logger = log.get_logger()


class FSStress(object):
    """Functions for fs stress with binary ltp-fsstress"""

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("fs_test just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    def _run(self, test_path, nops=100, nproc=10, loops=1):
        """
        -d dir      specifies the base directory for operations
        -n nops     specifies the no. of operations per process (default 1)
        -p nproc    specifies the no. of processes (default 1)
        -l loops    specifies the no. of times the testrun should loop
        -c          specifies not to remove files(cleanup) after execution
        -r          specifies random name padding
        """
        logger.info(self._run.__doc__)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        fsstress_bin = os.path.join(cur_dir, 'fsstress')
        test_log = os.path.join(self.top_path, 'fsstress.log')

        fsstress_cmd = "{0} -d {1} -l {2} -n {3} -p {4} -v -w -r -c | tee -a {5}".format(
            fsstress_bin, test_path, str(loops), str(nops),  str(nproc), test_log)

        try:
            os.system('chmod 777 {0}*'.format(fsstress_bin))
            rc, output = utils.run_cmd(fsstress_cmd)
            logger.info('\n'.format(output.strip('\n')))
            logger.info("PASS: Run fsstress on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run fsstress on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fsstress", "sanity")
        utils.mkdir_path(test_path)
        return self._run(test_path, nops=100, nproc=10, loops=1)

    def stress(self):
        self.verify()
        stress_path = os.path.join(self.top_path, "fsstress", "stress")
        pool = ThreadPoolExecutor(max_workers=8)
        futures = []
        for x in range(1, 5):
            test_path = os.path.join(stress_path, str(x))
            utils.mkdir_path(test_path)
            futures.append(pool.submit(self._run, test_path, nops=1000, nproc=50, loops=3))
        pool.shutdown()
        future_result = [future.result() for future in futures]
        result = False if False in future_result else True
        return result


if __name__ == '__main__':
    fs_stress = FSStress("/tmp")
    fs_stress.sanity()
