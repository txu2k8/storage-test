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

from storagetest.tests.argument import case_dict_2_string, exclude_case, MntParser, \
    load_tests_from_testcase


def tc_benchmark(action):
    """Benchmark test arguments"""
    from storagetest.tests.mnt.benchmark import BenchMarkTC
    case_info_dict = BenchMarkTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'benchmark',
        help='storage->mnt benchmark test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[MntParser().test_path, exclude_case()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='benchmark')


def tc_sanity(action):
    """Sanity test arguments"""
    from storagetest.tests.mnt.sanity import SanityTC
    case_info_dict = SanityTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'sanity',
        help='storage->mnt sanity test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[MntParser().test_path, exclude_case()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, loops=1, suite='sanity')


def tc_stress(action):
    """Stress test arguments"""
    from storagetest.tests.mnt.stress import StressTC
    case_info_dict = StressTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)

    parser = action.add_parser(
        'stress',
        help='storage->mnt stress test',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[MntParser().test_path, exclude_case()]
    )
    parser.add_argument("--case", action="store", dest="case_list",
                        default=['all'], nargs='+',
                        choices=case_info_dict.keys(),
                        help="default:['all]")
    parser.set_defaults(func=test_suite_generator, suite='stress')


def tc_load(action):
    """Load data tools arguments"""

    from storagetest.tests.mnt.loadgen import LoadGenTC
    case_info_dict = LoadGenTC().get_case_name_desc()
    case_desc = case_dict_2_string(case_info_dict, 25)
    mnt_p = MntParser()
    parser = action.add_parser(
        'load',
        help='storage->mnt load data file tools',
        epilog='Test Case List:\n{0}'.format(case_desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[
            mnt_p.test_path,
            mnt_p.dir_number,
            mnt_p.file_number,
            mnt_p.file_size_range,
            exclude_case()
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
        from storagetest.tests.mnt.benchmark import BenchMarkTC as MntTestCase
    elif args.suite == 'sanity':
        test_py = os.path.join(cur_dir, 'sanity.py')
        from storagetest.tests.mnt.sanity import SanityTC as MntTestCase
    elif args.suite == 'stress':
        test_py = os.path.join(cur_dir, 'stress.py')
        from storagetest.tests.mnt.stress import StressTC as MntTestCase
    elif args.suite == 'load':
        test_py = os.path.join(cur_dir, 'loadgen.py')
        from storagetest.tests.mnt.loadgen import LoadGenTC as MntTestCase
    else:
        raise Exception("Unknown sub parser suite")

    test_suite = load_tests_from_testcase(MntTestCase, args)
    return test_suite, test_py


def add_mnt_subparsers(action):
    """
    add subparsers for tests -> mnt
    :param action:
    :return:
    """

    # mnt
    mnt_parser = action.add_parser('mnt', help='base dir')
    mnt_parser.set_defaults(project='mnt')
    mnt_action = mnt_parser.add_subparsers(help='Test on a filesystem mount point')

    tc_benchmark(mnt_action)
    tc_sanity(mnt_action)
    tc_stress(mnt_action)
    tc_load(mnt_action)


if __name__ == '__main__':
    pass
