#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : raw_ut.py
@Time  : 2020/11/11 16:28
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import random
import json
import xlrd
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed

from storagetest.pkgs.fileops import FileOps
from storagetest.pkgs.dd import DD
from storagetest.libs import utils, log
from storagetest.libs.exceptions import PlatformError, NoSuchDir

logger = log.get_logger()


class RawUT(object):
    """RAW unit test"""

    def __init__(self, raw_device):
        self.raw_device = raw_device
        self.phase_list = []

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.raw_device):
            raise NoSuchDir(self.raw_device)

    def print_phase(self):
        if len(self.phase_list) == 0:
            return True
        step_table = PrettyTable(['No.', 'Test', 'Result', 'Comments'])
        step_table.align['TestCase'] = 'l'
        step_table.align['Comments'] = 'l'
        for idx, step in enumerate(self.phase_list):
            step_status = [idx + 1] + step
            step_table.add_row(step_status)
        logger.info("\n{0}".format(step_table))
        return True

    @staticmethod
    def load_xls(xls_path, wb_name):
        """
        get config from excel file
        :param xls_path:
        :param wb_name:
        :return: row list
        """
        logger.info('Read config from {0}, wb_name:{1} ...'.format(xls_path, wb_name))
        try:
            data = xlrd.open_workbook(xls_path)
        except Exception as e:
            raise Exception(e)

        table = data.sheet_by_name(wb_name)
        nrows = table.nrows
        # colnames = table.row_values(0)
        row_list = []
        for rownum in range(0, nrows):
            row = table.row_values(rownum)
            if not row:
                break
            row_list.append(row)
        return row_list

    def load_tcs(self):
        """
        get test case from xlsx file
        :return:
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        xls_path = os.path.join(cur_dir, 'tc', 'raw_sanity.xlsx')
        wb_name = "raw_sanity"

        skip = False
        case_list = []
        xls_row_list = self.load_xls(xls_path, wb_name)
        for row in xls_row_list[1:]:
            case_id = row[0]
            case_name = row[1]
            case_priority = row[2]
            case_loop = int(row[3]) if row[3] else ''
            case_original_file = row[4]

            # case steps:
            step_info = {}
            step_id = int(row[5]) if row[5] else ''
            step_info['skip'] = row[6]
            step_info['describe'] = row[7]
            step_info['wr'] = row[8]
            step_info['bs'] = int(row[9]) if row[9] else ''
            step_info['count'] = int(row[10]) if row[10] else ''
            step_info['seek_start'] = int(row[11]) if row[11] else ''
            step_info['seek_end'] = int(row[12]) if row[12] else ''
            step_info['seek_step'] = int(row[13]) if row[13] else ''
            step_info['oflag'] = row[14]
            step_info['expectation'] = row[15]
            step_info['comment'] = row[16]

            if case_id:
                case_info = {}
                case_info['suite'] = wb_name
                case_info['case_id'] = case_id
                case_info['case_name'] = case_name
                case_info['case_priority'] = case_priority
                case_info['case_loop'] = case_loop
                case_info['case_original_file'] = case_original_file
                case_info['steps'] = {}
                case_info['case_type'] = wb_name
            case_info['steps'][step_id] = step_info
            if step_info['skip'].lower() == 'yes':
                skip = True

            if case_id:
                if not skip:
                    case_list.append(case_info)
                skip = False

        return case_list

    @staticmethod
    def clean_up(rm_path, rm_file):
        """
        rm path_name/dd_r_*
        :return:
        """
        logger.info('>> Clean up files ...')
        rm_dd = "rm -f {0}/{1}*".format(rm_path, rm_file)
        rc, output = utils.run_cmd(rm_dd, 0)
        return rc, output

    @staticmethod
    def sync_dropcache():
        """
        sync; echo 3 > /proc/sys/vm/drop_caches
        :return:
        """
        logger.info('>> sync and clean drop_caches')
        sync_cmd = "sync; echo 3 > /proc/sys/vm/drop_caches"
        rc, output = utils.run_cmd(sync_cmd, 0)
        return rc, output

    def raw_write_read(self, case_info):
        """
        bd basic write read unit test work flow
        :param case_info:
        :return:
        """

        r_of_name = 'read_'
        case_id = case_info['case_id']
        case_suite = case_info['suite']
        case_original_file = case_info['case_original_file']
        original_file_fullpath = os.path.join('/bdut', case_suite, case_id, case_original_file)
        original_file_size = os.path.splitext(os.path.split(original_file_fullpath)[1])[0]
        original_md5 = FileOps().create_file(original_file_fullpath, original_file_size, line_size=128, mode='w+')
        logger.info('{0} {1}'.format(original_md5, original_file_fullpath))

        original_file_path, original_file_name = os.path.split(original_file_fullpath)
        r_of_path = os.path.join(original_file_path, r_of_name + original_file_name)

        case_loop = case_info['case_loop']
        steps_info = case_info['steps']

        loop_start = random.randint(1, 100)
        loop_end = loop_start + case_loop
        for loop in range(loop_start, loop_end):
            logger.info('>> Start Loop: {0}'.format(loop - loop_start))
            for step_id in steps_info.keys():
                step_info = steps_info[step_id]
                step_skip = step_info['skip']
                step_describe = step_info['describe']
                if step_skip.lower() == 'YES':
                    logger.warning('>> Skiped test step: CaseID:{0}, CaseName:{1}, StepID:{2}, StepDescribe:{3}'.format(
                        case_info['case_id'], case_info['case_name'], step_id, step_describe))
                    raise Exception()

                step_wr = step_info['wr']
                step_bs = step_info['bs']
                step_count = step_info['count']
                step_seek_start = step_info['seek_start']
                step_seek_end = step_info['seek_end']
                step_seek_step = step_info['seek_step']
                step_oflag = step_info['oflag']
                step_comment = step_info['comment']
                if step_seek_start > step_seek_end:
                    step_seek_step = step_info['seek_step'] * (-1)
                    step_seek_start -= 1
                    step_seek_end -= 1
                step_expectation = step_info['expectation']
                timeout = 900 if int(step_bs) * int(step_count) > 8388600 else 120

                self.clean_up(original_file_path, r_of_name)
                logger.info('>> Start Step: {0}, args:\n{1}'.format(step_id, json.dumps(step_info, indent=4)))
                for seek in range(step_seek_start, step_seek_end, step_seek_step):
                    total_seek = str(loop) + str(seek) if (loop_end - loop_start) > 1 else str(seek)
                    if step_wr.lower() == 'w':
                        DD().dd_exec(original_file_fullpath, self.raw_device, step_bs, step_count, seek=total_seek,
                                     oflag=step_oflag, timeout=timeout)
                    elif step_wr.lower() == 'r':
                        if step_comment == 'seek * 11 / 4 + 2':
                            total_seek = str(int(total_seek) * 11 / 4 + 2)
                        r_of_fullpath = r_of_path + '.' + str(total_seek)
                        DD().dd_exec(self.raw_device, r_of_fullpath, step_bs, step_count, skip=total_seek,
                                     oflag=step_oflag, timeout=timeout)
                        r_md5 = FileOps().hash_md5(r_of_fullpath)
                        logger.debug('{0} {1}'.format(original_md5, original_file_fullpath))
                        logger.debug('{0} {1}'.format(r_md5, r_of_fullpath))
                        if step_expectation == 'md5 match':
                            assert r_md5 == original_md5, '\n{0} {1}\n{2} {3}'.format(original_md5,
                                                                                      original_file_fullpath,
                                                                                      r_md5, r_of_fullpath)
                        else:
                            assert r_md5 != original_md5, '\n{0} {1}\n{2} {3}'.format(original_md5,
                                                                                      original_file_fullpath,
                                                                                      r_md5, r_of_fullpath)
                    else:
                        logger.error('Only support w / r mode!')
                        raise Exception('Not support: {0}'.format(step_wr))

                self.clean_up(original_file_path, r_of_name)
                self.sync_dropcache()

        return True

    def raw_write_read_inode(self, case_info):
        """
        bd basic write read unit test work flow
        :param case_info:
        :return:
        """

        def inode_wr(thread_n, bs, offset, original_file, loops=10):
            """
            inode wr
            :param thread_n:
            :param bs:
            :param offset:
            :param original_file:
            :param loops:
            :return:
            """

            for loop in range(1, loops):  # require: loops <= 1024
                i_offset = thread_n * loops + loop
                o_offset = offset + loop
                original_thread_loop_file = os.path.join(os.path.split(original_file)[0],
                                                         'inode_wr.{0}.{1}'.format(thread_n, loop))
                original_thread_loop_file_r = original_thread_loop_file + '.r'

                DD.dd_exec(original_file, original_thread_loop_file, bs, count=1, skip=i_offset, oflag='direct',
                                   timeout=60)
                DD.dd_exec(original_thread_loop_file, self.raw_device, bs, count=1, seek=o_offset, oflag='direct',
                                   timeout=60)
                DD.dd_exec(self.raw_device, original_thread_loop_file_r, bs, count=1, skip=o_offset, oflag='direct',
                                   timeout=60)
                w_md5 = FileOps().hash_md5(original_thread_loop_file)
                r_md5 = FileOps().hash_md5(original_thread_loop_file_r)
                if r_md5 != w_md5:
                    logger.error('{0} {1}'.format(w_md5, original_thread_loop_file))
                    logger.error('{0} {1}'.format(r_md5, original_thread_loop_file_r))
                    return False
            return True

        # Create original file
        case_id = case_info['case_id']
        case_suite = case_info['suite']
        case_original_file = case_info['case_original_file']
        original_file_fullpath = os.path.join('/bdut', case_suite, case_id, case_original_file)
        original_file_size = os.path.splitext(os.path.split(original_file_fullpath)[1])[0]
        original_md5 = FileOps().create_file(original_file_fullpath, original_file_size, line_size=128, mode='w+')
        logger.info('{0} {1}'.format(original_md5, original_file_fullpath))

        case_loop = case_info['case_loop']
        bs = 4096
        pool = ThreadPoolExecutor(max_workers=1000)
        futures = []
        for thread in range(1, 1000):
            offset = thread * 4194304 / bs
            futures.append(pool.submit(inode_wr, thread, bs, offset, original_file_fullpath, case_loop))

        future_result = [future.result() for future in as_completed(futures)]
        pool.shutdown()
        result = False if False in future_result else True

        self.clean_up(os.path.split(original_file_fullpath)[0], 'inode_wr')
        self.sync_dropcache()

        return result

    def run(self, test):
        if not [step['skip'] for step in test['steps'].values() if step['skip'].lower() == 'no']:
            return True

        if 'inode_write_read' in test['case_name']:
            self.raw_write_read_inode(test)
        else:
            self.raw_write_read(test)
        return True

    def sanity(self, case_id_list=None, case_priority_list=None):
        if case_priority_list is None:
            case_priority_list = []
        if case_id_list is None:
            case_id_list = []

        self.verify()
        for test in self.load_tcs():
            step_desc_list = []
            for step_id in test['steps'].keys():
                step_desc = test['steps'][step_id]['describe']
                expectation = test['steps'][step_id]['expectation']
                msg = 'CaseStep: {0}. {1}'.format(step_id, step_desc)
                if expectation:
                    msg += "--Expectation:{}".format(expectation)
                logger.info(msg)
                step_desc_list.append(step_desc)
            desc = ';'.join(step_desc_list)
            if case_id_list and test['case_id'] not in case_id_list:
                self.phase_list.append([test['case_name'], "Skiped", desc])
                continue
            if case_priority_list and test['case_priority'] not in case_priority_list:
                self.phase_list.append([test['case_name'], "Skiped", desc])
                continue
            self.phase_list.append([test['case_name'], "Start", desc])
            self.print_phase()
            try:
                logger.info(json.dumps(test, indent=4))
                self.run(test)
                self.phase_list[-1][1] = "PASS"
            except Exception as e:
                self.phase_list[-1][1] = "FAIL"
                raise e
            finally:
                self.print_phase()
        return True


if __name__ == '__main__':
    pass
