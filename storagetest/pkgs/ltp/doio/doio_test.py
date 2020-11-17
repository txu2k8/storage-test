#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : doio_test.py
@Time  : 2020/11/3 11:37
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest

from storagetest.libs.log import log
from storagetest.pkgs.base import PkgBase, TestProfile

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class DoIO(PkgBase):
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
        super(DoIO, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "doio")

    def iogen_doio_test_profile(self):
        """
        Examples:
        ---------
        # run forever:  8 process - using record locks
        iogen -i 0 100000b:doio_1 | doio -av -n 8 -m 1000

        # run forever:  8 process - using record locks
        iogen -i 0 100000b:doio_2 | doio -akv -n 8 -m 1000
        """
        iogen_bin = os.path.join(bin_path, 'iogen')
        doio_bin = os.path.join(bin_path, 'doio')
        test = TestProfile(
            name="iogen01",
            test_path=self.test_path,
            bin_path=bin_path,
            command="{0} -i 120s -s read,write 500b:{1}doio.f1.$$ 1000b:{1}doio.f2.$$ | {2} -akv -n 2".format(
                     iogen_bin, self.test_path, doio_bin),
            fail_flag="Test failed",
        )

        return test

    def rwtest_profiles(self):
        """
        Return rwtest case list FYI:
        https://github.com/linux-test-project/ltp/blob/master/runtest/fs
        """
        rwtest_bin = os.path.join(bin_path, 'rwtest')
        cmd_list = [
            "{0} -N rwtest01 -c -q -i 60s -f sync 10%25000:{1}/rw-sync-$$",
            "{0} -N rwtest02 -c -q -i 60s -f buffered 10%25000:{1}/rw-buffered-$$",
            "{0} -N rwtest03 -c -q -i 60s -n 2 -f buffered -s mmread,mmwrite -m random -Dv 10%25000:{1}/mm-buff-$$",
            "{0} -N rwtest04 -c -q -i 60s -n 2 -f sync -s mmread,mmwrite -m random -Dv 10%25000:{1}/mm-sync-$$",
            "{0} -N rwtest05 -c -q -i 50 -T 64b 500b:{1}/rwtest01%f",
            "{0} -N iogen01 -i 120s -s read,write -Da -Dv -n 2 500b:{1}/doio.f1.$$ 1000b:{1}/doio.f2.$$",
        ]

        tests = []
        for idx, cmd in enumerate(cmd_list):
            test = TestProfile(
                name="rwtest-"+str(idx+1),
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(rwtest_bin, self.test_path),
                fail_flag="Test failed",
            )
            tests.append(test)
        return tests

    def growfiles_test_profiles(self):
        """
        Return growfiles case list FYI:
        https://github.com/linux-test-project/ltp/blob/master/runtest/fs
        """
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

        tests = []
        for idx, cmd in enumerate(cmd_list):
            test = TestProfile(
                name="gf_" + str(idx + 1),
                desc="growfiles test-" + str(idx + 1),
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(growfiles_bin, self.test_path),
                fail_flag="Test failed",
            )
            tests.append(test)
        return tests

    def rwtest(self):
        self.test_path = os.path.join(self.top_path, "rwtest")
        return self.run_tests(self.rwtest_profiles())

    def growfiles(self):
        self.test_path = os.path.join(self.top_path, "growfiles")
        return self.run_tests(self.growfiles_test_profiles())

    def iogen_doio(self):
        self.test_path = os.path.join(self.top_path, "iogen_doio")
        return self.run(self.iogen_doio_test_profile())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.doio = DoIO("/mnt/test")

    def test_01(self):
        self.doio.rwtest()

    def test_02(self):
        self.doio.growfiles()

    def test_03(self):
        self.doio.iogen_doio()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
