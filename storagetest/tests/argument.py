#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : argument.py
@Time  : 2020/11/2 11:03
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import argparse
import unittest


def case_dict_2_string(case_dict, case_name_len=25):
    case_string = '  {0:<3} {1:<{2}}  {3}\n'.format(
        'NO.', 'CaseName', case_name_len, 'CaseDescription')
    for i, (k, v) in enumerate(case_dict.items()):
        case_string += '  {n:<3} {k:<{le}}  {v}\n'.format(
            n=i + 1, k=k, le=case_name_len, v=v)
    return case_string


def load_tests_from_testcase(test_case_class, args):
    """
    load tests from testcase class
    Args:
        test_case_class: TestCase class object
        args: parse args

    Returns: unittest.TestSuite()
    """
    if 'all' in args.case_list:
        # Load all test cases
        # test_suite = unittest.TestLoader().loadTestsFromTestCase(RawTestCase)
        test_suite = unittest.TestSuite()
        tc_names = unittest.TestLoader().getTestCaseNames(test_case_class)
        if not tc_names and hasattr(test_case_class, 'runTest'):
            tc_names = ['runTest']
        for tc_name in tc_names:
            if tc_name.split("test_")[1] in args.exclude_case_list:
                continue
            test_suite.addTest(test_case_class(tc_name, args))
    else:
        case_name_list = []
        args_list = []
        for case in args.case_list:
            if case in args.exclude_case_list:
                continue
            case_name = "test_" + case
            case_name_list.append(case_name)
            args_list.append(args)
        # Load the spec test cases
        # test_suite = unittest.TestSuite(map(RawTestCase, case_name_list))
        test_suite = unittest.TestSuite(map(lambda x, y: test_case_class(x, y), case_name_list, args_list))
    return test_suite


def runner(default='StressRunner'):
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--runner",
        action="store", dest="runner", default=default,
        choices=['TextTestRunner', 'StressRunner', 'pytest'],
        help="Run test case with runner,default:{0}".format(default)
    )
    return arg_parser


def exclude_case():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--exclude_case", action="store",
        dest="exclude_case_list", default=[], nargs='+',
        help="exclude test case list, eg:acl doio fio, default:[]"
    )
    return arg_parser


def smb_parser():
    """smb related parser"""
    arg_parser = argparse.ArgumentParser(add_help=False)
    smb_group = arg_parser.add_argument_group('SMB arguments')
    smb_group.add_argument("--smb_server",
                           action="store", dest="smb_server",
                           default="",
                           help="smb server,default:")
    smb_group.add_argument("--smb_user",
                           action="store", dest="smb_user",
                           default="",
                           help="smb user,default:")
    smb_group.add_argument("--smb_pwd", action="store",
                           dest="smb_pwd", default='',
                           help="smb password,default:")
    smb_group.add_argument("--case_filter", action="store",
                           dest="case_filter", default='',
                           help="smb test case filter, startswith(),default:")
    return arg_parser


class MntParser(object):
    """mnt related parser"""

    @property
    def test_path(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--test_path", "-d",
            required=True, action="store", dest="test_path",
            default=None, help="A full path for test,default:None"
        )
        return arg_parser

    @property
    def file_size(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--file_size", action="store", dest="file_size", type=int,
            default=1, help="file size(MB),default:1"
        )
        return arg_parser

    @property
    def file_size_range(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--file_size_range", action="store", dest="file_size_range",
            default="1,1", help="file size range(K/MB),default:1,1"
        )
        return arg_parser

    @property
    def file_number(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--file_number", action="store", dest="file_number", type=int,
            default=1, help="File number,default:1"
        )
        return arg_parser

    @property
    def dir_number(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--dir_number", action="store", dest="dir_number", type=int,
            default=1, help="Sub dir number,default:1"
        )
        return arg_parser


class RawParser(object):
    """raw related parser"""

    @property
    def device_path(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--device", "-d",
            required=True, action="store", dest="device",
            default=None, help="A full raw device path for test,default:None"
        )
        return arg_parser

    @property
    def case_ids(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--case_ids", action="store", dest="case_id_list",
            default=[], nargs='+', help="Filter: case_id list, default:[]")
        return arg_parser

    @property
    def case_priority(self):
        arg_parser = argparse.ArgumentParser(add_help=False)
        arg_parser.add_argument(
            "--case_priority", action="store", dest="case_priority_list",
            default=[], nargs='+', help="Filter: case_priority list, default:[]")
        return arg_parser

    @property
    def sanity(self):
        """RAW sanity test base info args"""

        arg_parser = argparse.ArgumentParser(
            parents=[
                self.device_path,
                self.case_ids,
                self.case_priority,
            ],
            add_help=False
        )
        return arg_parser


if __name__ == '__main__':
    pass
