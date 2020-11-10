#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : argument.py
@Time  : 2020/11/2 10:58
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import argparse
import unittest

from storage.argument import case_dict_2_string, test_path_parser

all_tcs_info = {
    # LTP
    'acl': 'Test ACL and Extend Attribute on Linux system',
    'create_files': 'Creates files of specified size',
    'doio': 'base rw test, doio & iogen',
    'fs_di': 'Test FileSystem Data Integrity',
    'fsstress': 'filesystem stress',
    'locktests': 'Test fcntl locking functions',
    'readall': 'Perform a small read on every file in a directory tree',
    'stream': 'File stream test',

    # tools
    # 'dd': 'TODO',
    'filebench': 'File System Workload test',
    'fio': 'Flexible I/O tester',
    'fstest': 'Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink',

    # private, write with python: file_op.py
    'consistency': 'POSIX/WINDOWS: Test the file consistency',
}


def tc_sanity(action):
    sanity_tcs = ['acl', 'doio', 'fs_di', 'locktests', 'readall', 'stream',  # LTP
                  'fio', 'fstest', 'consistency']
    case_info_dict = dict((k, v) for k, v in all_tcs_info.items() if k in sanity_tcs)
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'sanity',
        help='storage->mnt sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[test_path_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='sanity')


def tc_stress(action):
    stress_tcs = ['acl', 'create_files', 'doio', 'fs_di', 'fsstress', 'locktests', 'readall', 'stream',  # LTP
                  'filebench', 'fio', 'fstest', 'consistency', ]
    case_info_dict = dict((k, v) for k, v in all_tcs_info.items() if k in stress_tcs)
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'stress',
        help='storage->mnt stress test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[test_path_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, suite='stress')


def tc_load(action):
    from storage.argument import dir_number_parser, file_number_parser, file_size_range_parser
    case_info_dict = {
        'create_files': 'Creates files of specified size.(default:1dir*1file*1MB)',
        'small_files': 'Generate small files.(default:1dir*1file*1KB)',
        'empty_files': 'Generate empty files.(default:1dir*1file*0KB)',
        'seq_files': 'Generate sequential files of specified size by fio',
        'fsstress': 'Generate files by LTP fsstress(deep path/files)',
    }

    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'load',
        help='storage->mnt load data files',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[
            test_path_parser(),
            dir_number_parser(),
            file_number_parser(),
            file_size_range_parser(),
        ]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='load', runner="TextTestRunner")


# --- Generate Test suite
def test_suite_generator(args):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    if args.suite == 'sanity':
        test_py = os.path.join(cur_dir, 'sanity.py')
        from storage.mnt.sanity import SanityTC as MntTestCase
    elif args.suite == 'stress':
        test_py = os.path.join(cur_dir, 'stress.py')
        from storage.mnt.stress import StressTC as MntTestCase
    elif args.suite == 'load':
        test_py = os.path.join(cur_dir, 'loadgen.py')
        from storage.mnt.loadgen import LoadGenTC as MntTestCase
    else:
        raise Exception("Unknown sub parser suite")

    if 'all' in args.case_list:
        # Load all test cases
        test_suite = unittest.TestLoader().loadTestsFromTestCase(MntTestCase)
    else:
        case_name_list = []
        for case in args.case_list:
            case_name = "test_" + case
            case_name_list.append(case_name)
        # Load the spec test cases
        test_suite = unittest.TestSuite(map(MntTestCase, case_name_list))

    return test_suite, test_py


def add_mnt_subparsers(action):
    """
    add subparsers for storage -> mnt
    :param action:
    :return:
    """

    # mnt
    mnt_parser = action.add_parser('mnt', help='storage test: mnt')
    mnt_parser.set_defaults(project='mnt')
    mnt_action = mnt_parser.add_subparsers(help='Test on a filesystem mount point')

    tc_sanity(mnt_action)
    tc_stress(mnt_action)
    tc_load(mnt_action)


if __name__ == '__main__':
    pass
