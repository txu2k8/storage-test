#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fio_test.py
@Time  : 2020/11/6 15:56
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import time
import unittest

from libs import utils
from libs.log import log
from libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary

logger = log.get_logger()


class Test(object):
    """Define the test struct"""
    def __init__(self, name="", desc="", test_path="", command=""):
        self.name = name
        self.desc = desc
        self.test_path = test_path
        self.command = command


class FIO(object):
    """
    FIO: Flexible I/O tester
    https://fio.readthedocs.io/en/latest/fio_doc.html
    ==========
    """

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)
        try:
            utils.run_cmd("which fio", expected_rc=0)
        except Exception as e:
            logger.error(e)
            raise NoSuchBinary("fio, try install it.(apt-get install -y fio)")

    @staticmethod
    def dbench_tcs(test_path, size="2G"):
        """FYI https://github.com/leeliu/dbench"""
        str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        cmd_list = [
            ("Read IOPS", "fio --name=read_iops --filename={0} --bs=4K --iodepth=64 --size={1} --readwrite=randread --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
            ("Write IOPS", "fio --name=write_iops --filename={0} --bs=4K --iodepth=64 --size={1} --readwrite=randwrite --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
            ("Read Bandwidth", "fio --name=read_bw --filename={0} --bs=128K --iodepth=64 --size={1} --readwrite=randread --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
            ("Write Bandwidth", "fio --name=write_bw --filename={0} --bs=128K --iodepth=64 --size={1} --readwrite=randwrite --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
            ("Read Latency", "fio --name=read_latency --filename={0} --bs=4K --iodepth=4 --size={1} --readwrite=randread --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --ramp_time=2s"),
            ("Write Latency", "fio --name=write_latency --filename={0} --bs=4K --iodepth=4 --size={1} --readwrite=randwrite --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --ramp_time=2s"),
            ("Read Sequential Speed", "fio --name=read_seq --filename={0} --bs=1M --iodepth=16 --size={1} --readwrite=read --thread --numjobs=4 --offset_increment=500M --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
            ("Write Sequential Speed", "fio --name=write_seq --filename={0} --bs=1M --iodepth=16 --size={1} --readwrite=write --thread --numjobs=4 --offset_increment=500M --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
            ("Read Write Mixed", "fio --name=rw_mix --filename={0} --bs=4k --iodepth=64 --size={1} --readwrite=randrw --rwmixread=75 --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
        ]

        tcs = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            tc_name = "fio_{0}_{1}".format(idx+1, utils.to_safe_name(desc))
            f_pathname = os.path.join(test_path, "{0}_{1}.data".format(tc_name, str_time))
            tc = Test(
                name=tc_name,
                desc=desc,
                test_path=test_path,
                command=cmd.format(f_pathname, size))
            tcs.append(tc)
        return tcs

    @staticmethod
    def seq_write_tcs(test_path, size="2G"):
        str_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        cmd_list = [
            ("Write Sequential Speed", "fio --name=write_seq --filename={0} --bs=1M --iodepth=16 --size={1} --readwrite=write --thread --numjobs=4 --offset_increment=500M --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
        ]

        tcs = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            tc_name = "fio_{0}_{1}".format(idx + 1, '_'.join(desc.lower().split(" ")))
            f_pathname = os.path.join(test_path, "{0}_{1}.data".format(tc_name, str_time))
            tc = Test(
                name=tc_name,
                desc=desc,
                test_path=test_path,
                command=cmd.format(f_pathname, size))
            tcs.append(tc)
        return tcs

    def run(self, test):
        logger.info(self.run.__doc__)
        test_name = test.name
        test_path = test.test_path
        test_log = os.path.join(self.top_path, '{0}.log'.format(test_name))
        test_cmd = "{0} | tee -a {1}".format(test.command, test_log)
        utils.mkdir_path(test_path)

        try:
            logger.info("Testing {} ...".format(test.desc))
            rc, output = utils.run_cmd(test_cmd)
            logger.info(output)
            if "Error" in output:
                raise Exception("FAIL: Run {0} on {1}".format(test_name, test_path))
            logger.info("PASS: Run {0} on {1}".format(test_name, test_path))
        except Exception as e:
            logger.info("FAIL: Run {0} on {1}".format(test_name, test_path))
            raise e
        finally:
            pass

        return True

    def seq_write(self, test_path, size="2G"):
        self.verify()
        for tc in self.seq_write_tcs(test_path, size):
            assert self.run(tc)
        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fio")
        for tc in self.dbench_tcs(test_path, size="2G"):
            assert self.run(tc)
        return True

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "fio")
        for tc in self.dbench_tcs(test_path, size="10G"):
            assert self.run(tc)
        return True


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fio = FIO("/mnt/test")

    def test_01(self):
        self.fio.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
