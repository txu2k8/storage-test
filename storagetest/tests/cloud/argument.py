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

from storagetest.tests.argument import case_dict_2_string, MntParser, exclude_case, \
    load_tests_from_testcase


def tc_sanity(action):
    from storagetest.tests.cloud.sanity import SanityTC
    case_info_dict = SanityTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'sanity',
        help='storage->cloud sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[MntParser().test_path, exclude_case()]
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
        test_py = os.path.join(cur_dir, 'sanity.py')
        from storagetest.tests.cloud.sanity import SanityTC as CloudTestCase
    else:
        raise Exception("Unknown sub parser suite")
    test_suite = load_tests_from_testcase(CloudTestCase, args)
    return test_suite, test_py


def add_cloud_subparsers(action):
    """
    add subparsers for tests -> cloud
    :param action:
    :return:
    """

    # raw
    mnt_parser = action.add_parser('cloud', help='base url')
    mnt_parser.set_defaults(project='cloud')
    mnt_action = mnt_parser.add_subparsers(help='Test on a cloud storage')

    tc_sanity(mnt_action)


if __name__ == '__main__':
    pass
