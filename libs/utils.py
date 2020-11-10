#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : utils.py
@Time  : 2020/10/26 17:29
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import sys
import re
import time
import subprocess
import inspect
import string
import hashlib

from libs.log import log
from libs.retry import retry, retry_call

"""utils"""

# --- Global Value
logger = log.get_logger()
# --- OS constants
POSIX = os.name == "posix"
WINDOWS = os.name == "nt"
PY2 = sys.version_info[0] == 2
ENCODING = None if PY2 else 'utf-8'
DD_BINARY = os.path.join(os.getcwd(), r'bin\dd\dd.exe') if WINDOWS else 'dd'
MD5SUM_BINARY = os.path.join(os.getcwd(), r'bin\git\md5sum.exe') if WINDOWS else 'md5sum'


def subprocess_popen_cmd(cmd_spec, output=True, timeout=7200):
    """
    Executes command and Returns (rc, output) tuple
    :param cmd_spec: Command to be executed
    :param output: Output STDOUT and STDERR to a specified file
    :param timeout
    :return:
    """

    rc, out_err = 0, ""
    logger.info('Execute: {cmds}'.format(cmds=cmd_spec))
    try:
        p = subprocess.Popen(cmd_spec, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = p.communicate(timeout=timeout)
        rc = p.returncode
        if output:
            out_err = err.decode("utf-8", 'ignore') + out.decode("utf-8", 'ignore')
        if rc != 0:
            logger.warning('Output: rc={0}, stdout/stderr:\n{1}'.format(rc, out_err))
        return rc, out_err
    except Exception as e:
        raise Exception('Failed to execute: {0}\n{1}'.format(cmd_spec, e))


def run_cmd(cmd_spec, expected_rc=0, output=True, tries=1, delay=3, timeout=7200):
    """
    A generic method for running commands which will raise exception if return code of exeuction is not as expected.
    :param cmd_spec:A list of words constituting a command line
    :param expected_rc:An expected value of return code after command execution, defaults to 0, If expected. RC.upper()
    is 'IGNORE' then exception will not be raised.
    :param output:
    :param tries: retry times
    :param delay: retry delay
    :param timeout
    :return:
    """

    method_name = inspect.stack()[1][3]    # Get name of the calling method, returns <methodName>'
    rc, output = retry_call(subprocess_popen_cmd, fkwargs={'cmd_spec': cmd_spec, 'output': output, 'timeout': timeout},
                            tries=tries, delay=delay, logger=logger)

    if isinstance(expected_rc, str) and expected_rc.upper() == 'IGNORE':
        return rc, output

    if rc != expected_rc:
        raise Exception('%s(): Failed command: %s\nMismatched RC: Received [%d], Expected [%d]\nError: %s' % (
            method_name, cmd_spec, rc, expected_rc, output))
    return rc, output


def sort_dict(dict_data, base='key', reverse=False):
    """
    sort dict by base key
    :param dict_data: dict_data
    :param base: 'key' or 'value'
    :param reverse: descending order if True, else if False:ascending
    :return:(list) list_data
    """

    if base == 'key':
        return sorted(dict_data.items(), key=lambda d: d[0], reverse=reverse)
    elif base == 'value':
        return sorted(dict_data.items(), key=lambda d: d[1], reverse=reverse)
    else:
        logger.error("Please input the correct base value, should be 'key' or 'value'")
        return False


def strsize_to_byte(str_size):
    """
    convert str_size such as 1K,1M,1G,1T to size 1024 (byte)
    :param str_size:such as 1K,1M,1G,1T
    :return:size (byte)
    """

    str_size = str(str_size) if not isinstance(str_size, str) else str_size

    if not bool(re.search('[a-z_A-Z]', str_size)):
        return int(str_size)

    if not bool(re.search('[0-9]', str_size)):
        raise Exception('Not support string size: {}'.format(str_size))

    regx = re.compile(r'(\d+)\s*([a-z_A-Z]+)', re.I)
    tmp_size_unit = regx.findall(str_size)[0]
    tmp_size = int(tmp_size_unit[0])
    tmp_unit = tmp_size_unit[1]
    if bool(re.search('K', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024
    elif bool(re.search('M', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024 * 1024
    elif bool(re.search('G', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024 * 1024 * 1024
    elif bool(re.search('T', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024 * 1024 * 1024 * 1024
    else:
        raise Exception("Error string input, fmt:<int>KB/MB/GB/TB(IGNORECASE)")

    return size_byte


def mkdir_path(local_path):
    """
    verify the local path exist, if not create it
    :param local_path:
    :return:
    """
    if not os.path.isdir(local_path):
        try:
            os.makedirs(local_path)
        except OSError as e:
            raise Exception(e)


def strnum_to_int_list(str_num, rtn_len=2, style=','):
    """
    Format a string to number list
    :param str_num: string_number
    :param rtn_len: return number list length
    :param style: string split with style, '-' not support
    :return: a number list
    """

    if isinstance(str_num, int):
        return [str_num]*rtn_len
    elif isinstance(str_num, str):
        pass
    else:
        str_num = str(str_num)

    if bool(re.search('[^0-9{0}|\-1\-\-9]'.format(style), str_num)):
        raise Exception('None-INT char in string: {}'.format(str_num))

    str_num_list = str_num.split(style)
    num_list = [int(n) for n in str_num_list]
    num_list_len = len(num_list)
    if rtn_len > num_list_len:
        num_list += [num_list[-1]] * (rtn_len - num_list_len)
    return num_list[:rtn_len]


if __name__ == '__main__':
    pass
