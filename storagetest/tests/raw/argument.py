#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : argument.py
@Time  : 2020/11/2 14:31
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import argparse
import unittest

from storagetest.tests.argument import case_dict_2_string, RawSanityParser


def tc_sanity(action):
    case_info_dict = {
        'ut': 'RAW device write/read unit test',
    }

    case_desc = case_dict_2_string(case_info_dict, 25)
    raw_parser = RawSanityParser()
    parser = action.add_parser(
        'sanity',
        help='tests->raw sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[raw_parser.base]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, suite='sanity')


# --- Test suite
def test_suite_generator(args):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    if args.suite == 'sanity':
        test_py = os.path.join(cur_dir, 'sanity.py.py')
        from storagetest.tests.raw.sanity import SanityTC as RawTestCase
    else:
        raise Exception("Unknown sub parser suite")

    if 'all' in args.case_list:
        # Load all test cases
        # test_suite = unittest.TestLoader().loadTestsFromTestCase(RawTestCase)
        test_suite = unittest.TestSuite()
        tc_names = unittest.TestLoader().getTestCaseNames(RawTestCase)
        if not tc_names and hasattr(RawTestCase, 'runTest'):
            tc_names = ['runTest']
        for tc_name in tc_names:
            test_suite.addTest(RawTestCase(tc_name, args))
    else:
        case_name_list = []
        args_list = []
        for case in args.case_list:
            case_name = "test_" + case
            case_name_list.append(case_name)
            args_list.append(args)
        # Load the spec test cases
        # test_suite = unittest.TestSuite(map(RawTestCase, case_name_list))
        test_suite = unittest.TestSuite(map(lambda x, y: RawTestCase(x, y), case_name_list, args_list))

    return test_suite, test_py


def add_raw_subparsers(action):
    """
    add subparsers for tests -> raw
    :param action:
    :return:
    """

    # raw
    raw_parser = action.add_parser('raw', help='tests test: raw')
    raw_parser.set_defaults(project='raw')
    raw_action = raw_parser.add_subparsers(help='tests test on a raw device')

    tc_sanity(raw_action)


if __name__ == '__main__':
    pass
