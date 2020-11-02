#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : argument.py
@Time  : 2020/11/2 14:37
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import argparse
import unittest

from storage.argument import case_dict_2_string, test_path_parser


def tc_sanity(action):
    case_info_dict = {
        '01_consistency': 'test the file consistency',
        '02_fsstress': 'filesystem stress with LTP tool fsstress',
    }

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
    parser.set_defaults(func=test_suite_generator, suite='mnt.sanity')


# --- Test suite
def test_suite_generator(args):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    if args.suite == 'mnt.sanity':
        test_py = os.path.join(cur_dir, 'tc.py')
        from storage.mnt.tc import SanityTC as MntTestCase
    elif args.suite == 'mnt.stress':
        test_py = os.path.join(cur_dir, 'tc.py')
        from storage.mnt.tc import StressTC as MntTestCase
    elif args.suite == 'mnt.load':
        test_py = os.path.join(cur_dir, 'tc.py')
        from storage.mnt.tc import LoadGenTC as MntTestCase
    else:
        test_py = os.path.join(cur_dir, 'tc.py')
        from storage.mnt.tc import SanityTC as MntTestCase

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


def add_cloud_subparsers(action):
    """
    add subparsers for storage -> cloud
    :param action:
    :return:
    """

    # raw
    mnt_parser = action.add_parser('cloud', help='storage test: cloud ')
    mnt_parser.set_defaults(project='cloud')
    mnt_action = mnt_parser.add_subparsers(help='storage test on a cloud storage')

    tc_sanity(mnt_action)


if __name__ == '__main__':
    pass
