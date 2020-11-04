#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : argument.py
@Time  : 2020/11/2 11:03
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import argparse


def case_dict_2_string(case_dict, case_name_len=25):
    case_string = '  {0:<3} {1:<{2}}  {3}\n'.format(
        'NO.', 'CaseName', case_name_len, 'CaseDescription')
    for i, (k, v) in enumerate(case_dict.items()):
        case_string += '  {n:<3} {k:<{le}}  {v}\n'.format(
            n=i + 1, k=k, le=case_name_len, v=v)
    return case_string


def runner(default='StressRunner'):
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--runner",
        action="store", dest="runner", default=default,
        choices=['TextTestRunner', 'StressRunner', 'pytest'],
        help="Run test case with runner,default:{0}".format(default)
    )
    return arg_parser


def test_path_parser():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--test_path",
        required=True, action="store", dest="test_path",
        default=None, help="A full path for test,default:None"
    )
    return arg_parser


if __name__ == '__main__':
    pass