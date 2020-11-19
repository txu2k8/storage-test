#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : filebench.py
@Time  : 2020/11/2 16:45
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os

from storagetest.libs import utils
from storagetest.libs.log import log
from storagetest.libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary
from storagetest.pkgs.base import PkgBase, TestProfile

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))


class FileBench(PkgBase):
    """
    Filebench - A Model Based File System Workload Generator
    https://github.com/filebench/filebench/wiki
    ===============
    Filebench is a file system and tests benchmark that can generate a large
    variety of workloads. Unlike typical benchmarks it is extremely flexible and
    allows to specify application's I/O behavior using its extensive Workload Model
    Language (WML). Users can either describe desired workloads from scratch or use
    (with or without modifications) workload personalities shipped with Filebench
    (e.g., mail-, web-, file-, and database-server workloads).
    """

    def __init__(self, top_path):
        super(FileBench, self).__init__(top_path)
        self.test_path = os.path.join(self.top_path, "filebench")

    def verify(self):
        if os.name != "posix":
            raise PlatformError("fs_test just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)
        rc, output = utils.run_cmd('which filebench')
        if not output.strip("\n") or 'no filebench' in output:
            logger.warning("yum install filebench -y")
            raise NoSuchBinary("filebench not installed")

    @property
    def workload_templates(self):
        conf_path = os.path.join(cur_dir, 'workloads')
        conf_list = os.popen('ls {0}'.format(conf_path)).read().split('\n')
        fb_conf_names = []
        for fb_conf in conf_list:
            if not fb_conf.endswith('.f'):
                continue
            fb_conf_names.append(os.path.join(conf_path, fb_conf))
        return fb_conf_names

    def new_workload(self, workload_conf_template):
        logger.info('Load: {0}'.format(workload_conf_template))
        conf_name = os.path.split(workload_conf_template)[-1]
        tmp_path = os.path.join(os.getcwd(), 'tmp')
        utils.mkdir_path(tmp_path)

        test_conf_name = 'filebench-{0}'.format(conf_name)
        test_conf = os.path.join(tmp_path, test_conf_name)
        rc, output = utils.run_cmd('cp {0} {1}'.format(workload_conf_template, test_conf))
        print(output)

        # modify the tmp workload conf file: dir
        config_cmd = "sed -i 's/set \$dir=\/tmp/set \$dir={test_path}/g' {test_conf}".format(
            test_path=self.test_path.replace('/', '\/'), test_conf=test_conf)
        rc, output = utils.run_cmd(config_cmd)
        print(output)

        # add run time
        with open(test_conf, "a+") as f:
            f_text = f.read()
            if f_text.find('run 60') == -1:
                f.write('run 60\n')
        return test_conf

    def tests_generator(self):
        tests = []
        for idx, conf_template in enumerate(self.workload_templates):
            workload_conf = self.new_workload(conf_template)
            conf_name = os.path.split(workload_conf)[-1]
            test_name = "filebench_{0}_{1}".format(idx+1, conf_name)
            test = TestProfile(
                name=test_name,
                desc=conf_name,
                test_path=self.test_path,
                command="echo 0 to /proc/sys/kernel/randomize_va_space; filebench -f {0}".format(workload_conf))
            tests.append(test)
        return tests

    def sanity(self):
        return self.run_tests(self.tests_generator())

    def stress(self):
        return self.run_tests(self.tests_generator())


if __name__ == '__main__':
    fb = FileBench("/tmp")
    fb.sanity()