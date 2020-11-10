#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : filebench.py
@Time  : 2020/11/2 16:45
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest
from parameterized import parameterized, param

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary

# --- Global Value
logger = log.get_logger()


class FileBench(object):
    """
    Filebench - A Model Based File System Workload Generator
    https://github.com/filebench/filebench/wiki
    ===============
    Filebench is a file system and storage benchmark that can generate a large
    variety of workloads. Unlike typical benchmarks it is extremely flexible and
    allows to specify application's I/O behavior using its extensive Workload Model
    Language (WML). Users can either describe desired workloads from scratch or use
    (with or without modifications) workload personalities shipped with Filebench
    (e.g., mail-, web-, file-, and database-server workloads).
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("fs_test just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)
        rc, output = utils.run_cmd('which filebench')
        if not output.strip("\n") or 'no filebench' in output:
            logger.warning("yum install filebench -y")
            raise NoSuchBinary("filebench not installed")

    @staticmethod
    def set_workload(test_path, workload_conf_template):
        logger.info('Load: {0}'.format(workload_conf_template))
        conf_name = os.path.split(workload_conf_template)[-1]
        tmp_path = os.path.join(os.getcwd(), 'tmp')
        utils.mkdir_path(tmp_path)

        test_conf_name = 'filebench_{0}_{1}'.format(test_path.replace('/', '_'), conf_name)
        test_conf = os.path.join(tmp_path, test_conf_name)
        rc, output = utils.run_cmd('cp {0} {1}'.format(workload_conf_template, test_conf))
        print(output)

        # modify the tmp workload conf file: dir
        config_cmd = "sed -i 's/set \$dir=\/tmp/set \$dir={test_path}/g' {test_conf}".format(
            test_path=test_path.replace('/', '\/'), test_conf=test_conf)
        rc, output = utils.run_cmd(config_cmd)
        print(output)

        # add run time
        with open(test_conf, "a+") as f:
            f_text = f.read()
            if f_text.find('run 60') == -1:
                f.write('run 60\n')
        return test_conf

    @staticmethod
    def get_workload_templates():
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        conf_path = os.path.join(cur_dir, 'workloads')
        conf_list = os.popen('ls {0}'.format(conf_path)).read().split('\n')
        fb_conf_names = []
        for fb_conf in conf_list:
            if not fb_conf.endswith('.f'):
                continue
            fb_conf_names.append(os.path.join(conf_path, fb_conf))
        return fb_conf_names

    def run(self, test_path, workload_conf_template):
        """
        filebench -f workload.f
        """
        rc, output = utils.run_cmd('which filebench')
        if not output.strip("\n") or 'no filebench' in output:
            logger.warning("yum install filebench -y")
            raise NoSuchBinary("filebench not installed")

        rc, output = utils.run_cmd('echo 0 to /proc/sys/kernel/randomize_va_space')
        logger.info(output.strip('\n'))

        workload_conf = self.set_workload(test_path, workload_conf_template)
        conf_name = os.path.split(workload_conf)[-1]
        test_log = os.path.join(self.top_path, '{}.log'.format(conf_name))
        fb_cmd = 'filebench -f {0} | tee -a {1}'.format(workload_conf, test_log)

        try:
            rc, output = utils.run_cmd(fb_cmd, timeout=72000)
            logger.info('\n'.format(output.strip('\n')))
            logger.info("Complete: Run fstest on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run fstest on {0}".format(test_path))
            raise e
        finally:
            utils.run_cmd('rm -rf {0}'.format(workload_conf))

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "filebench")
        utils.mkdir_path(test_path)
        fb_conf_list = self.get_workload_templates()
        len_conf = len(fb_conf_list)
        for idx, fb_conf in enumerate(fb_conf_list):
            logger.info("({0}/{1}) Run FileBench with workload: {2}".format(
                idx+1, len_conf, fb_conf))
            self.run(test_path, fb_conf)
        return True

    def stress(self):
        test_path = os.path.join(self.top_path, "filebench")
        utils.mkdir_path(test_path)
        fb_conf_list = self.get_workload_templates()
        len_conf = len(fb_conf_list)
        for idx, fb_conf in enumerate(fb_conf_list):
            logger.info("({0}/{1}) Run FileBench with workload: {2}".format(
                idx + 1, len_conf, fb_conf))
            self.run(test_path, fb_conf)
        return True


def custom_name_func():
    def custom_naming_func(testcase_func, param_num, param):
        return '{0}_{1}_{2}'.format(testcase_func.__name__, param_num, parameterized.to_safe_name(param.args[0]))
        # return testcase_func.__name__ + '_' + parameterized.to_safe_name(param.args[0])

    return custom_naming_func


class FilebenchTestCase(unittest.TestCase):
    _test_path = ""
    # Verify
    if os.name != "posix":
        raise PlatformError("fs_test just support for linux machine!")
    if not os.path.isdir(_test_path):
        raise NoSuchDir(_test_path)
    rc, output = utils.run_cmd('which filebench')
    if not output.strip("\n") or 'no filebench' in output:
        logger.warning("yum install filebench -y")
        raise NoSuchBinary("filebench not installed")

    def setUp(self):
        logger.info("Filebench Test Start ...")

    def tearDown(self):
        logger.info("Filebench Test Complete!")

    fb_parameterized = []
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(cur_dir, 'workloads')
    conf_list = os.popen('ls {0}'.format(conf_path)).read().split('\n')

    for fb_conf in conf_list:
        if not fb_conf.endswith('.f'):
            continue
        fb_conf_pathname = os.path.join(conf_path, fb_conf)
        p = param(fb_conf.split('.')[0], fb_conf_pathname)
        fb_parameterized.append(p)

    @parameterized.expand(fb_parameterized, name_func=custom_name_func())
    def test_filebench(self, _, fb_conf_pathname):
        fb_test = FileBench(self._test_path)
        logger.info(fb_test.__doc__)
        fb_test.run(self._test_path, fb_conf_pathname)


if __name__ == '__main__':
    # fb = FileBench("/tmp")
    # fb.sanity()

    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(FilebenchTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
