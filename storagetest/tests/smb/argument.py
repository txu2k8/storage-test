#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : argument.py
@Time  : 2021/1/26 15:21
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import argparse

from storagetest.tests.argument import case_dict_2_string, exclude_case, MntParser, smb_parser, \
    load_tests_from_testcase


def tc_sanity(action):
    """Sanity test arguments"""
    from storagetest.tests.smb.sanity import SanityTC
    case_info_dict = SanityTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'sanity',
        help='storage->smb sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[MntParser().test_path, exclude_case(), smb_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='sanity')


def tc_stress(action):
    """Stress test arguments"""
    from storagetest.tests.smb.stress import StressTC
    case_info_dict = StressTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'stress',
        help='storage->smb stress test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[MntParser().test_path, exclude_case(), smb_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, suite='stress')


# --- Generate Test suite
def test_suite_generator(args):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    if args.suite == 'sanity':
        test_py = os.path.join(cur_dir, 'sanity.py')
        from storagetest.tests.smb.sanity import SanityTC as SMBTestCase
    elif args.suite == 'stress':
        test_py = os.path.join(cur_dir, 'stress.py')
        from storagetest.tests.smb.stress import StressTC as SMBTestCase
    else:
        raise Exception("Unknown sub parser suite")

    test_suite = load_tests_from_testcase(SMBTestCase, args)
    return test_suite, test_py


def add_smb_subparsers(action):
    """
    add subparsers for tests -> smb
    :param action:
    :return:
    """

    # smb
    parser = action.add_parser('smb', help='base smb server')
    parser.set_defaults(project='smb')
    smb_action = parser.add_subparsers(help='Test on smb')

    tc_sanity(smb_action)
    tc_stress(smb_action)


if __name__ == '__main__':
    pass
