#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : file_ops.py
@Time  : 2020/10/26 15:43
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import datetime
import copy
from collections import defaultdict
from prettytable import PrettyTable

from storagetest.libs.log import log
from storagetest.libs import utils
from storagetest.libs import retry


logger = log.get_logger()
WINDOWS = os.name == "nt"


class DD(object):
    """run IO with dd
    Copy a file, converting and formatting according to the operands.
    """
    def __init__(self, targets=""):
        super(DD, self).__init__()
        self.target_dirs = targets if isinstance(targets, list) else [targets]
        self.run_cmd = utils.run_cmd

    def dd_exec(self, if_path, of_path, bs, count, skip=None,
                seek=None, oflag=None, timeout=1800):
        """
        dd read write
        :param if_path: read path
        :param of_path: write path
        :param bs:
        :param count:
        :param skip: read offset
        :param seek: write offset
        :param oflag: eg: direct
        :param timeout: run_cmd timeout second
        :return:
        """

        dd_cmd = "dd if={0} of={1} bs={2} count={3}".format(
            if_path, of_path, bs, count)
        if oflag:
            dd_cmd += " oflag={0}".format(oflag)
        if skip:
            dd_cmd += " skip={0}".format(skip)
        if seek:
            dd_cmd += " seek={0}".format(seek)

        rc, output = self.run_cmd(dd_cmd, 'ignore', tries=30, delay=20, timeout=timeout)

        return rc, output

    @retry(tries=5, delay=3)
    def ssh_md5sum(self, f_name):
        """
        get md5sum on POSIX by cmd: md5sum file_name
        :param f_name:file full path
        :return:
        """

        md5sum_cmd = "md5sum {0}".format(f_name)
        rc, output = self.run_cmd(md5sum_cmd, 0, tries=3)
        return output.strip('\n').split(' ')[0].split('\\')[-1]

    @staticmethod
    def verify_md5(w_file_md5_dict, r_file_md5_dict):
        """
        verify 2 file_md5_dict match
        :param w_file_md5_dict:
        :param r_file_md5_dict:
        :return:
        """
        sort_r_file_md5_dict = utils.sort_dict(r_file_md5_dict)
        table = PrettyTable(['File Name', 'Expected', 'Actually'])
        table_err = copy.deepcopy(table)
        for r_file, r_md5 in sort_r_file_md5_dict:
            w_file = r_file.rstrip('.r') + '.w'
            w_md5 = w_file_md5_dict[w_file]
            if r_md5 != w_md5:
                table_err.add_row([r_file, w_md5, r_md5])
            table.add_row([r_file, w_md5, r_md5])
        logger.info("> Files md5 compare:\n" + str(table))
        if len(table_err._rows) > 0:
            logger.error("> Files md5 compare:\n" + str(table_err))
            raise Exception('Files md5 mismatch!')
        return True

    def dd_write_read(self, file_size='4k', bs='4k', rename=True):
        f_size = utils.strsize_to_byte(file_size)
        bs_size = utils.strsize_to_byte(bs)
        count = f_size // bs_size

        file_md5_dict = defaultdict(str)
        for target in self.target_dirs:
            dd_w_file_md5_dict = defaultdict(str)
            dd_r_file_md5_dict = defaultdict(str)

            dd_f_name_prefix = os.path.basename(target)
            if rename:
                str_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                dd_f_name = '{0}.{1}.dat'.format(dd_f_name_prefix, str_time)
            else:
                dd_f_name = '{0}.dat'.format(dd_f_name_prefix)
            w_file = os.path.join(target + "/", dd_f_name + '.w')
            r_file = os.path.join(target + "/", dd_f_name + '.r')
            original_file = os.path.join('/tmp/', dd_f_name)

            original_md5 = utils.create_file(original_file, file_size, line_size=128, mode='w+')
            file_md5_dict[w_file] = original_md5

            # write into bd
            self.dd_exec(original_file, w_file, bs, count, oflag='direct')
            dd_w_file_md5_dict[w_file] = original_md5

            # read from bd
            self.dd_exec(w_file, r_file, bs, count, oflag='direct')
            r_md5 = self.ssh_md5sum(r_file)
            dd_r_file_md5_dict[r_file] = r_md5

            # Verify w/r file md5sum
            self.verify_md5(dd_w_file_md5_dict, dd_r_file_md5_dict)

        return file_md5_dict

    def dd_read(self, expect_file_md5_dict, file_size='4k', bs='4k'):
        f_size = util.strsize_to_byte(file_size)
        bs_size = util.strsize_to_byte(bs)
        count = f_size // bs_size
        file_md5_dict = defaultdict(str)

        for w_file, w_md5 in expect_file_md5_dict.items():
            r_file = w_file.rstrip('.w') + '.r'
            # read from bd
            self.dd_exec(w_file, r_file, bs, count, oflag='direct')

            r_md5 = self.ssh_md5sum(r_file)
            file_md5_dict[r_file] = r_md5

            # Verify w/r file md5sum
            self.verify_md5(expect_file_md5_dict, file_md5_dict)

        return True

    @staticmethod
    def remove_filesystem():
        logger.info("SKIP ...")
        return True
