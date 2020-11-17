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

from storagetest.tests.argument import case_dict_2_string, mnt_path_parser


def tc_benchmark(action):
    """Benchmark test arguments"""
    from storagetest.tests.mnt.benchmark import BenchMarkTC
    case_info_dict = BenchMarkTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'benchmark',
        help='tests->mnt benchmark test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[mnt_path_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='benchmark')


def tc_sanity(action):
    """Sanity test arguments"""
    from storagetest.tests.mnt import SanityTC
    case_info_dict = SanityTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'sanity',
        help='tests->mnt sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[mnt_path_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='sanity')


def tc_stress(action):
    """Stress test arguments"""
    from storagetest.tests.mnt import StressTC
    case_info_dict = StressTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'stress',
        help='tests->mnt stress test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[mnt_path_parser()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, suite='stress')


def tc_load(action):
    """Load data tools arguments"""

    from storagetest.tests.mnt import LoadGenTC
    from storagetest.tests.argument import dir_number_parser, file_number_parser, file_size_range_parser
    case_info_dict = LoadGenTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'load',
        help='tests->mnt load data file tools',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[
            mnt_path_parser(),
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
    if args.suite == 'benchmark':
        test_py = os.path.join(cur_dir, 'benchmark.py')
        from storagetest.tests.mnt import BenchMarkTC as MntTestCase
    elif args.suite == 'sanity':
        test_py = os.path.join(cur_dir, 'sanity.py')
        from storagetest.tests.mnt import SanityTC as MntTestCase
    elif args.suite == 'stress':
        test_py = os.path.join(cur_dir, 'stress.py')
        from storagetest.tests.mnt import StressTC as MntTestCase
    elif args.suite == 'load':
        test_py = os.path.join(cur_dir, 'loadgen.py')
        from storagetest.tests.mnt import LoadGenTC as MntTestCase
    else:
        raise Exception("Unknown sub parser suite")

    if 'all' in args.case_list:
        # Load all test cases
        test_suite = unittest.TestLoader().loadTestsFromTestCase(MntTestCase)
    else:
        case_name_list = []
        args_list = []
        for case in args.case_list:
            case_name = "test_" + case
            case_name_list.append(case_name)
            args_list.append(args)
        # Load the spec test cases
        test_suite = unittest.TestSuite(map(lambda x, y: MntTestCase(x, y), case_name_list, args_list))

    return test_suite, test_py


def add_mnt_subparsers(action):
    """
    add subparsers for tests -> mnt
    :param action:
    :return:
    """

    # mnt
    mnt_parser = action.add_parser('mnt', help='tests test: mnt')
    mnt_parser.set_defaults(project='mnt')
    mnt_action = mnt_parser.add_subparsers(help='Test on a filesystem mount point')

    tc_benchmark(mnt_action)
    tc_sanity(mnt_action)
    tc_stress(mnt_action)
    tc_load(mnt_action)


if __name__ == '__main__':
    pass
