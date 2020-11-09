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

    logger.info('Execute: {cmds}'.format(cmds=cmd_spec))
    try:
        p = subprocess.Popen(cmd_spec, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = p.communicate(timeout=timeout)
        rc = p.returncode
        if rc == 0:
            out_err = out.decode("utf-8", 'ignore') + err.decode("utf-8", 'ignore') # escape(stdout)
        else:
            out_err = err.decode("utf-8", 'ignore')  # escape(stderr)
            logger.warning('Output: rc={0}, stdout/stderr:\n{1}'.format(rc, out_err))
        return rc, out_err

        # t_beginning = time.time()
        #
        # while True:
        #     if p.poll() is not None:
        #         break
        #     seconds_passed = time.time() - t_beginning
        #     if timeout and seconds_passed > timeout:
        #         p.terminate()
        #         raise TimeoutError('TimeOutError: {0} seconds'.format(timeout))
        #     time.sleep(0.1)
        #
        # rc = p.returncode
        # if output_file:
        #     # (stdout, stderr) = p.communicate()
        #     stdout, stderr = p.stdout.read(), p.stderr.read()
        #     if rc == 0:
        #         std_out_err = stdout.decode("utf-8", 'ignore')  # escape(stdout)
        #     else:
        #         std_out_err = stderr.decode("utf-8", 'ignore')  # escape(stderr)
        #         logger.warning('Output: rc={0}, stdout/stderr:\n{1}'.format(rc, std_out_err))
        # else:
        #     std_out_err = ''
        # # p.stdout.close()
        # # p.stderr.close()
        # # p.kill()
        # return rc, std_out_err
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


@retry(tries=2, delay=3)
def hash_md5(f_name):
    """
    returns the hash md5 of the opened file
    :param f_name: file full path
    :return:(string) md5_value 32-bit hexadecimal string.
    """
    logger.debug('Get MD5: {0}'.format(f_name))
    try:
        h_md5 = hashlib.md5()
        with open(f_name, "rb") as f:
            for chunk in iter(lambda: f.read(), b""):
                h_md5.update(chunk)
        return h_md5.hexdigest()
    except Exception as e:
        raise Exception(e)


def generate_random_string(str_len=16):
    """
    generate random string
    return ''.join(random.sample((string.ascii_letters + string.digits)*str_len, str_len))
    :param str_len: byte
    :return:random_string
    """

    base_string = string.ascii_letters + string.digits
    # base_string = string.printable
    base_string_len = len(base_string)
    multiple = 1
    if base_string_len < str_len:
        multiple = (str_len // base_string_len) + 1

    return ''.join(random.sample(base_string * multiple, str_len))


def create_file(path_name, total_size='4k', line_size=128, mode='w+'):
    """
    create original file, each line with line_number, and specified line size
    :param path_name:
    :param total_size:
    :param line_size:
    :param mode: w+ / a+
    :return:
    """

    logger.info('>> Create file: {0}'.format(path_name))
    original_path = os.path.split(path_name)[0]
    if not os.path.isdir(original_path):
        try:
            os.makedirs(original_path)
        except OSError as e:
            raise Exception(e)

    size = strsize_to_byte(total_size)
    line_count = size // line_size
    unaligned_size = size % line_size

    with open(path_name, mode) as f:
        logger.info("write file: {0}".format(path_name))
        for line_num in range(0, line_count):
            random_sting = generate_random_string(line_size - 2 - len(str(line_num))) + '\n'
            f.write('{line_num}:{random_s}'.format(line_num=line_num, random_s=random_sting))
        if unaligned_size > 0:
            f.write(generate_random_string(unaligned_size))
        f.flush()
        os.fsync(f.fileno())

    file_md5 = hash_md5(path_name)
    return file_md5


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
