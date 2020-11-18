#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : iozone_test.py
@Time  : 2020/11/13 13:53
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


import os
import unittest

from storagetest.libs.log import log
from storagetest.pkgs.base import PkgBase, TestProfile, to_safe_name

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class IOzone(PkgBase):
    """
    IOzone Filesystem Benchmark
    https://sourceforge.net/projects/fsmark/
    =============
    Generates and measures a variety of file operations.
    -i #  Test to run
        0=write/rewrite, 1=read/re-read, 2=random-read/write
        3=Read-backwards, 4=Re-write-record, 5=stride-read, 6=fwrite/re-fwrite
        7=fread/Re-fread, 8=random_mix, 9=pwrite/Re-pwrite, 10=pread/Re-pread
        11=pwritev/Re-pwritev, 12=preadv/Re-preadv
    """

    def __init__(self, top_path):
        super(IOzone, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "iozone")
        self.record_size_list = [
            ("Record Size: 4Kb", "-r 4k"),
            ("Record Size: 128Kb", "-r 128k"),
            ("Record Size: 1MB", "-r 1m"),
        ]
        self.file_size_list = [
            ("File Size: 512MB", "-s 512m"),
            ("File Size: 2GB", "-s 2048m"),
            ("File Size: 8GB", "-s 8192m"),
        ]
        self.test_item_list = [
            ("write/rewrite", "-i 0"),
            ("read/re-read", "-i 1"),
            ("random-read/write", "-i 2"),
            ("Read-backwards", "-i 3"),
            ("Re-write-record", "-i 4"),
            ("stride-read", "-i 5"),
            ("fwrite/re-fwrite", "-i 6"),
            ("fread/Re-fread", "-i 7"),
            ("random_mix", "-i 8"),
            ("pwrite/Re-pwrite", "-i 9"),
            ("pread/Re-pread", "-i 1"),
            ("pwritev/Re-pwritev", "-i 11"),
            ("preadv/Re-preadv", "-i 12"),
        ]

    def stress_profiles(self):
        """
        Return fs_mark test case list
        """
        ioz_bin = os.path.join(bin_path, 'iozone')
        tests = []
        idx = 0
        file_desc, file_size = self.file_size_list[0]
        for test_desc, test_item in self.test_item_list:
            for record_desc, record_size in self.record_size_list:
                test_name = "iozone_{0}_{1}".format(idx + 1, to_safe_name(test_desc))
                test_filename = os.path.join(self.test_path, test_name+".data")
                cmd = "{0} -e -o -f {1} {2} {3} {4}".format(
                    ioz_bin, test_filename, record_size, file_size, test_item)
                test = TestProfile(
                    name=test_name,
                    desc="{0}-{1}-{2}".format(record_desc, file_desc, test_desc),
                    test_path=self.test_path,
                    bin_path=bin_path,
                    command=cmd)
                tests.append(test)
                idx += 1
        return tests

    def benchmark_profiles(self):
        """0=write/rewrite, 1=read/re-read, 2=random-read/write"""
        ioz_bin = os.path.join(bin_path, 'iozone')
        tests = []
        idx = 0
        for test_desc, test_item in self.test_item_list[:3]:
            for record_desc, record_size in self.record_size_list:
                for file_desc, file_size in self.file_size_list:
                    test_name = "iozone_{0}_{1}".format(idx + 1, to_safe_name(test_desc))
                    test_filename = os.path.join(self.test_path, test_name + ".data")
                    cmd = "{0} -e -o -f {1} {2} {3} {4}".format(
                        ioz_bin, test_filename, record_size, file_size, test_item)
                    test = TestProfile(
                        name=test_name,
                        desc="{0}-{1}-{2}".format(record_desc, file_desc, test_desc),
                        test_path=self.test_path,
                        bin_path=bin_path,
                        command=cmd)
                    tests.append(test)
                    idx += 1
        return tests

    def benchmark(self):
        """Test to run: 0=write/rewrite, 1=read/re-read, 2=random-read/write"""
        logger.info(self.benchmark.__doc__)
        return self.run_tests(self.benchmark_profiles())

    def stress(self):
        """
        Test to run:
        0=write/rewrite, 1=read/re-read, 2=random-read/write
        3=Read-backwards, 4=Re-write-record, 5=stride-read, 6=fwrite/re-fwrite
        7=fread/Re-fread, 8=random_mix, 9=pwrite/Re-pwrite, 10=pread/Re-pread
        11=pwritev/Re-pwritev, 12=preadv/Re-preadv
        """
        logger.info(self.stress.__doc__)
        return self.run_tests(self.stress_profiles())


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.ioz = IOzone("/mnt/test")

    def test_benchmark(self):
        self.ioz.benchmark()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
