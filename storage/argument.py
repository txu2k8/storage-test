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


def mnt_path_parser():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--test_path", "-d",
        required=True, action="store", dest="test_path",
        default=None, help="A full path for test,default:None"
    )
    return arg_parser


def file_size_parser():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--file_size", action="store", dest="file_size", type=int,
        default=1, help="file size(MB),default:1"
    )
    return arg_parser


def file_size_range_parser():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--file_size_range", action="store", dest="file_size_range",
        default="1,1", help="file size range(K/MB),default:1,1"
    )
    return arg_parser


def file_number_parser():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--file_number", action="store", dest="file_number", type=int,
        default=1, help="File number,default:1"
    )
    return arg_parser


def dir_number_parser():
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument(
        "--dir_number", action="store", dest="dir_number", type=int,
        default=1, help="Sub dir number,default:1"
    )
    return arg_parser


# raw
class RawSanityParser(object):
    """ raw sanity related parser"""

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
    def base(self):
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
