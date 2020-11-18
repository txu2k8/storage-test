#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : main.py
@Time  : 2020/11/18 9:55
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import sys
import time
import argparse
sys.path.append("..")
from storagetest.libs import log

"""stresstest entrance"""

THREE_DAYS = 60*60*24*3
STR_TIME = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def base_parser():
    """
    Set base argument
    :return:
    """

    # Parent parser
    parser = argparse.ArgumentParser(description='Storage Test Project')
    parser.add_argument("--debug", action="store_true", dest="debug",
                        default=False, help="debug mode")
    parser.add_argument("--duration", action="store", dest="duration",
                        default=THREE_DAYS, type=int,
                        help="duration time(s),default:60*60*24*3 (3 days)")
    parser.add_argument("--loops", action="store", dest="loops",
                        default=0, type=int,
                        help="run loops(0:keep run forever),default:0")
    parser.add_argument("--mail_to", action="store", dest="mail_to",
                        default=None, help="mail_to, split with ';'")
    parser.add_argument("--output", action="store", dest="output",
                        default=None, help="output log dir path, default:None")
    parser.add_argument("--runner", action="store", dest="runner",
                        default='StressRunner',
                        choices=['TextTestRunner', 'StressRunner', 'pytest'],
                        help="Run test case with runner,default:StressRunner")

    return parser


def storage_test_parser_args():
    """
    Set parser for tests test
    :return:
    """

    # Parent parser
    parser = base_parser()
    action = parser.add_subparsers(help='Storage Test')

    # mnt
    from storagetest.tests.mnt.argument import add_mnt_subparsers
    add_mnt_subparsers(action)

    # raw
    from storagetest.tests.raw.argument import add_raw_subparsers
    add_raw_subparsers(action)

    # raw
    from storagetest.tests.cloud.argument import add_cloud_subparsers
    add_cloud_subparsers(action)

    return parser.parse_args()


# --- Init logger
global log_path, log_title
def init_logger(args):
    """
    init the logger
    :param args:
    :return:
    """

    log_title = '{project}'.format(project=args.project)
    log_dir = os.path.join(CUR_DIR, 'log', args.project)
    if args.suite and args.project != args.suite:
        log_title += '-{suite}'.format(suite=args.suite)
        log_dir = os.path.join(log_dir, args.suite)
    if args.case_list:
        log_title += '-{str_case}'.format(str_case='_'.join(args.case_list))
    if args.output:
        log_dir = os.path.join(CUR_DIR, args.output)

    log_name = log_title + '-' + STR_TIME
    log_path = os.path.join(log_dir, log_name + '.log')
    logger = log.get_logger(log_path, output_logfile=True, debug=args.debug, reset_logger=True)

    return logger


# --- Init Test Session
def init_test_session(args):
    logger = init_logger(args)
    logger.info('{0} Args {0} '.format('=' * 15))
    command = 'python ' + ' '.join(sys.argv)
    logger.info(command)
    logger.info(args)
    logger.info('{0} End {0} '.format('=' * 15))

    return logger


def teardown_test_session(result):
    # tar logs, TODO
    if (result.failure_count + result.error_count) > 0:
        pass
    # write test result mysql, TODO

    return


# =============================
# --- Run with XXX Runner
# --- Support: TextTestRunner, StressRunner, Pytest
# =============================
# TextTestRunner
def run_with_text_test_runner(args):
    """Run with TextTestRunner"""
    from unittest import TextTestRunner

    _logger = init_test_session(args)
    runner = TextTestRunner(verbosity=2)

    # get unittest test suite and then run unittest case
    test_suite, _ = args.func(args)
    runner.run(test_suite)


# StressRunner
def run_with_stress_runner(args):
    """Run with StressRunner -- report html"""

    logger = init_test_session(args)

    # run with StressRunner -- report html
    from stressrunner import StressRunner, MailInfo
    mail_info = MailInfo(m_to=args.mail_to)
    runner = StressRunner(report_path=log_path.replace('.log', '.html'),
                          logger=logger, iteration=args.loops,
                          tc_elapsed_limit=None, save_last_result=False,
                          test_title=log_title, mail_info=mail_info)
    # get unittest test suite and then run unittest case
    test_suite, _ = args.func(args)
    runner.run(test_suite)


# Pytest
def run_with_pytest(args):
    """Run with Pytest"""

    import pytest

    const.set_value('args', args)
    logger = init_test_session(args)
    log_path = const.get_value('log_path')

    _, tc_py = args.func(args)  # test_xx.py full path
    run_tests = ' or '.join(args.case_list)
    loops = int(1e4) if args.loops < 1 else args.loops
    cmd = [
        '-s',
        '-x',  # Stop test when FAIL
        '-v',
        '-rA',
        '--instafail',
        '--disable-warnings',
        '--show-capture=no',
        '-k {tests}'.format(tests=run_tests),
        '--count={count}'.format(count=loops),
        '--repeat-scope=session',
        '--html={0}'.format(log_path.replace('.log', '.html')),
        '--self-contained-html',
        '--junit-xml={0}'.format(log_path.replace('.log', '.xml')),
        '--color=yes',
        # '--full-trace',
        tc_py
    ]

    logger.info('Run test command: {cmd}'.format(cmd=cmd))
    pytest.main(cmd)


def run(args):
    """Main method"""
    const.set_value('args', args)

    # -----------------------------
    # --- Run unittest suite
    # -----------------------------
    if args.runner == 'TextTestRunner':
        run_with_text_test_runner(args)
    elif args.runner == 'StressRunner':
        run_with_stress_runner(args)
    elif args.runner.lower() == 'pytest':
        run_with_pytest(args)
    else:
        raise Exception("Just Support: StressRunner, TextTestRunner, Pytest\n"
                        "Not support runner: {0}.".format(args.runner))
    return True


if __name__ == '__main__':
    run(args=storage_test_parser_args())
