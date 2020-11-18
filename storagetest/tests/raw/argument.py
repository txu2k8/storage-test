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

from storagetest.tests.argument import case_dict_2_string, RawParser, exclude_case, \
    load_tests_from_testcase


def tc_sanity(action):
    case_info_dict = {
        'ut': 'RAW device write/read unit test',
    }

    case_desc = case_dict_2_string(case_info_dict, 25)
    raw_p = RawParser()
    parser = action.add_parser(
        'sanity',
        help='storage->raw sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[raw_p.sanity, exclude_case()]
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

    test_suite = load_tests_from_testcase(RawTestCase, args)
    return test_suite, test_py


def add_raw_subparsers(action):
    """
    add subparsers for tests -> raw
    :param action:
    :return:
    """

    # raw
    raw_parser = action.add_parser('raw', help='base device')
    raw_parser.set_defaults(project='raw')
    raw_action = raw_parser.add_subparsers(help='Test on a raw device')

    tc_sanity(raw_action)


if __name__ == '__main__':
    pass
