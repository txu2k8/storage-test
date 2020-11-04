#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : doio_test.py
@Time  : 2020/11/3 11:37
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
from concurrent.futures import ThreadPoolExecutor

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir

logger = log.get_logger()


class Test(object):
    """Define the test struct"""
    def __init__(self, name="", desc="", test_path="", bin_path="", command=""):
        self.name = name
        self.desc = desc
        self.test_path = test_path
        self.bin_path = bin_path
        self.command = command


class DoIO(object):
    """
    Run Test with LTP tools:
    1. iogen & doio
    2. growfiles

    IOGEN & DOIO
    =============
    This is a pair of programs that does basic I/O operations on a set of files.
    The file offset, I/O length, I/O operation, and what open(2) flags are
    selected randomly from a pre-defined or commandline given set. All data
    written can be verified (this is the usual method).
    rwtest is a shell script that is a wrapper of iogen and doio.

    GROWFILES
    =============
    Growfiles will create and truncate files in gradual steps using write, and
    lseek. All system calls are checked for proper returns. The writes or the
    whole file content can be verified.  It can cause disk fragmentation.
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    @staticmethod
    def iogen_doio_tcs(test_path):
        """
        Examples:
        ---------
        # run forever:  8 process - using record locks
        iogen -i 0 100000b:doio_1 | doio -av -n 8 -m 1000

        # run forever:  8 process - using record locks
        iogen -i 0 100000b:doio_2 | doio -akv -n 8 -m 1000
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        bin_path = os.path.join(cur_dir, 'bin')
        iogen_bin = os.path.join(bin_path, 'iogen')
        doio_bin = os.path.join(bin_path, 'doio')
        tcs = [
            Test(name="iogen01", test_path=test_path, bin_path=bin_path,
                 command="{0} -i 120s -s read,write 500b:{1}doio.f1.$$ 1000b:{1}doio.f2.$$ | {2} -akv -n 2".format(
                     iogen_bin, test_path, doio_bin))
        ]
        return tcs

    @staticmethod
    def rwtest_tcs(test_path):
        """
        Return rwtest case list FYI:
        https://github.com/linux-test-project/ltp/blob/master/runtest/fs
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        bin_path = os.path.join(cur_dir, 'bin')
        rwtest_bin = os.path.join(bin_path, 'rwtest')
        cmd_list = [
            "{0} -N rwtest01 -c -q -i 60s -f sync 10%25000:{1}/rw-sync-$$",
            "{0} -N rwtest02 -c -q -i 60s -f buffered 10%25000:{1}/rw-buffered-$$",
            "{0} -N rwtest03 -c -q -i 60s -n 2 -f buffered -s mmread,mmwrite -m random -Dv 10%25000:{1}/mm-buff-$$",
            "{0} -N rwtest04 -c -q -i 60s -n 2 -f sync -s mmread,mmwrite -m random -Dv 10%25000:{1}/mm-sync-$$",
            "{0} -N rwtest05 -c -q -i 50 -T 64b 500b:{1}/rwtest01%f",
            "{0} -N iogen01 -i 120s -s read,write -Da -Dv -n 2 500b:{1}/doio.f1.$$ 1000b:{1}/doio.f2.$$",
        ]

        tcs = []
        for idx, cmd in enumerate(cmd_list):
            tc = Test(name="rwtest-"+str(idx+1), test_path=test_path, bin_path=bin_path,
                      command=cmd.format(rwtest_bin, test_path))
            tcs.append(tc)
        return tcs

    @staticmethod
    def growfiles_tcs(test_path):
        """
        Return growfiles case list FYI:
        https://github.com/linux-test-project/ltp/blob/master/runtest/fs
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        bin_path = os.path.join(cur_dir, 'bin')
        growfiles_bin = os.path.join(bin_path, 'growfiles')
        cmd_list = [
            "{0} -W gf01 -b -e 1 -u -i 0 -L 20 -w -C 1 -l -I r -T 10 -f glseek20 -S 2 -d {1}"
            "{0} -W gf02 -b -e 1 -L 10 -i 100 -I p -S 2 -u -f gf03_ -d {1}"
            "{0} -W gf03 -b -e 1 -g 1 -i 1 -S 150 -u -f gf05_ -d {1}"
            "{0} -W gf04 -b -e 1 -g 4090 -i 500 -t 39000 -u -f gf06_ -d {1}"
            "{0} -W gf05 -b -e 1 -g 5000 -i 500 -t 49900 -T10 -c9 -I p -u -f gf07_ -d {1}"
            "{0} -W gf06 -b -e 1 -u -r 1-5000 -R 0--1 -i 0 -L 30 -C 1 -f g_rand10 -S 2 -d {1}"
            "{0} -W gf07 -b -e 1 -u -r 1-5000 -R 0--2 -i 0 -L 30 -C 1 -I p -f g_rand13 -S 2 -d {1}"
            "{0} -W gf08 -b -e 1 -u -r 1-5000 -R 0--2 -i 0 -L 30 -C 1 -f g_rand11 -S 2 -d {1}"
            "{0} -W gf09 -b -e 1 -u -r 1-5000 -R 0--1 -i 0 -L 30 -C 1 -I p -f g_rand12 -S 2 -d {1}"
            "{0} -W gf10 -b -e 1 -u -r 1-5000 -i 0 -L 30 -C 1 -I l -f g_lio14 -S 2 -d {1}"
            "{0} -W gf11 -b -e 1 -u -r 1-5000 -i 0 -L 30 -C 1 -I L -f g_lio15 -S 2 -d {1}"
            "{0} -W gf12 -b -e 1 -u -i 0 -L 30 {1}"
            "{0} -W gf13 -b -e 1 -u -i 0 -L 30 -I r -r 1-4096 {1}"
            "{0} -W gf14 -b -e 1 -u -i 0 -L 20 -w -l -C 1 -T 10 -f glseek19 -S 2 -d {1}"
            "{0} -W gf15 -b -e 1 -u -r 1-49600 -I r -u -i 0 -L 120 -f Lgfile1 -d {1}"
            "{0} -W gf16 -b -e 1 -i 0 -L 120 -u -g 4090 -T 101 -t 408990 -l -C 10 -c 1000 -S 10 -f Lgf02_ -d {1}"
            "{0} -W gf17 -b -e 1 -i 0 -L 120 -u -g 5000 -T 101 -t 499990 -l -C 10 -c 1000 -S 10 -f Lgf03_ -d {1}"
            "{0} -W gf18 -b -e 1 -i 0 -L 120 -w -u -r 10-5000 -I r -l -S 2 -f Lgf04_ -d {1}"
            "{0} -W gf19 -b -e 1 -g 5000 -i 500 -t 49900 -T10 -c9 -I p -o O_RDWR,O_CREAT,O_TRUNC -u -f gf08i_ -d {1}"
            "{0} -W gf20 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -r 1-256000:512 -R 512-256000 -T 4 -f gfbigio-$$ -d {1}"
            "{0} -W gf21 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -g 20480 -T 10 -t 20480 -f gf-bld-$$ -d {1}"
            "{0} -W gf22 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -g 20480 -T 10 -t 20480 -f gf-bldf-$$ -d {1}"
            "{0} -W gf23 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -r 512-64000:1024 -R 1-384000 -T 4 -f gf-inf-$$ -d {1}"
            "{0} -W gf24 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -g 20480 -f gf-jbld-$$ -d {1}"
            "{0} -W gf25 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -r 1024000-2048000:2048 -R 4095-2048000 -T 1 -f gf-large-gs-$$ -d {1}"
            "{0} -W gf26 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -r 128-32768:128 -R 512-64000 -T 4 -f gfsmallio-$$ -d {1}"
            "{0} -W gf27 -b -D 0 -w -g 8b -C 1 -b -i 1000 -u -f gfsparse-1-$$ -d {1}"
            "{0} -W gf28 -b -D 0 -w -g 16b -C 1 -b -i 1000 -u -f gfsparse-2-$$ -d {1}"
            "{0} -W gf29 -b -D 0 -r 1-4096 -R 0-33554432 -i 0 -L 60 -C 1 -u -f gfsparse-3-$$ -d {1}"
            "{0} -W gf30 -D 0 -b -i 0 -L 60 -u -B 1000b -e 1 -o O_RDWR,O_CREAT,O_SYNC -g 20480 -T 10 -t 20480 -f gf-sync-$$ -d {1}"
        ]
        tcs = []
        for idx, cmd in enumerate(cmd_list):
            tc = Test(name="gf"+str(idx+1), desc="growfiles test-"+str(idx+1),
                      test_path=test_path, bin_path=bin_path,
                      command=cmd.format(growfiles_bin, test_path))
            tcs.append(tc)
        return tcs

    def run(self, test):
        """
        Run Test with command:
        support for:
            1. iogen & doio
            2. rwtest
            3. growfiles
        """
        logger.info(self.run.__doc__)
        test_name = test.name
        test_path = test.test_path
        bin_path = test.bin_path
        test_log = os.path.join(self.top_path, '{0}.log'.format(test_name))
        test_cmd = "{0} | tee -a {1}".format(test.command, test_log)

        try:
            os.system('chmod +x /{0}*'.format(bin_path))
            rc, output = utils.run_cmd(test_cmd)
            logger.info('\n'.format(output.strip('\n')))
            if "Test failed" in output:
                raise Exception("FAIL: Run {0} on {1}".format(test_name, test_path))
            logger.info("PASS: Run {0} on {1}".format(test_name, test_path))
        except Exception as e:
            logger.info("FAIL: Run {0} on {1}".format(test_name, test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "doio", "sanity")
        utils.mkdir_path(test_path)
        for tc in self.iogen_doio_tcs(test_path):
            assert self.run(tc)
        return True

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "doio", "stress")
        utils.mkdir_path(test_path)
        for tc in self.rwtest_tcs(test_path):
            assert self.run(tc)
        for tc in self.growfiles_tcs(test_path):
            assert self.run(tc)
        return True


if __name__ == '__main__':
    rwt = DoIO("/tmp")
    rwt.sanity()
