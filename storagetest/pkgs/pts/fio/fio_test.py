#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : fio_test.py
@Time  : 2020/11/6 15:56
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import unittest

from storagetest.libs import utils, log
from storagetest.libs.exceptions import PlatformError, NoSuchDir, NoSuchBinary
from storagetest.pkgs.base import PkgBase, TestProfile, to_safe_name

logger = log.get_logger()
cur_dir = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(cur_dir, 'bin')


class FIO(PkgBase):
    """
    FIO: Flexible I/O tester
    https://fio.readthedocs.io/en/latest/fio_doc.html
    ==========
    """

    def __init__(self, top_path):
        super(FIO, self).__init__(top_path)
        self.top_path = top_path
        self.test_path = os.path.join(top_path, "fio")

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

    def dbench_tcs(self, size="2G"):
        """FYI https://github.com/leeliu/dbench"""
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
        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list):
            test_name = "fio_{0}_{1}".format(idx + 1, to_safe_name(desc))
            f_pathname = os.path.join(self.test_path, test_name+".data")
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                command=cmd.format(f_pathname, size))
            tests.append(test)
        return tests

    def seq_write_tcs(self, num=1, size="2G"):
        cmd_list = [
            ("Write Sequential Speed", "fio --name=write_seq --filename={0} --bs=1M --iodepth=16 --size={1} --readwrite=write --thread --numjobs=4 --offset_increment=500M --randrepeat=0 --verify=0 --ioengine=libaio --direct=1 --gtod_reduce=1 --ramp_time=2s"),
        ]
        tests = []
        for idx, (desc, cmd) in enumerate(cmd_list*num):
            test_name = "fio_{0}_{1}".format(idx + 1, to_safe_name(desc))
            f_pathname = os.path.join(self.test_path, test_name + ".data")
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(f_pathname, size))
            tests.append(test)
        return tests

    def seq_write(self, num=1, size="2G"):
        return self.run_tests(self.seq_write_tcs(num, size))

    def sanity(self):
        """Run dbench tests"""
        return self.run_tests(self.dbench_tcs(size="10G"))

    def stress(self):
        """Run dbench tests"""
        return self.run_tests(self.dbench_tcs(size="10G"))

    def google_benchmark(self):
        """Benchmarking test from google disk"""
        gbm = GoogleBenchmarking(self.test_path)
        self.run(gbm.write_throughput)
        self.run(gbm.read_throughput)
        self.run(gbm.write_iops)
        self.run(gbm.read_iops)
        return True

    def google_raw_benchmark(self):
        """Benchmarking test from google disk"""
        gbm_raw = GoogleRawBenchmarking(self.test_path)
        self.run(gbm_raw.fill_disk)
        self.run(gbm_raw.write_bandwidth)
        self.run(gbm_raw.write_iops)
        self.run(gbm_raw.write_latency)
        self.run(gbm_raw.read_bandwidth)
        self.run(gbm_raw.read_iops)
        self.run(gbm_raw.read_latency)
        self.run(gbm_raw.seq_read_bandwidth)
        self.run(gbm_raw.seq_write_bandwidth)
        return True


class GoogleBenchmarking(object):
    """
    Benchmarking test from google disk
    https://cloud.google.com/compute/docs/disks/benchmarking-pd-performance#existing-disk
    """
    def __init__(self, test_path):
        self.test_path = test_path  # eg: /mnt/test

    @property
    def write_throughput(self):
        """
        Test write throughput by performing sequential writes with multiple parallel streams (8+),
        using an I/O block size of 1 MB and an I/O depth of at least 64
        """
        cmd = "sudo fio --name=write_throughput --directory={0} --numjobs=8 " \
              "--size=10G --time_based --runtime=60s --ramp_time=2s " \
              "--ioengine=libaio --direct=1 --verify=0 --bs=1M --iodepth=64 " \
              "--rw=write --group_reporting=1".format(self.test_path)
        test = TestProfile(
            name="write_throughput",
            desc=self.write_throughput.__doc__,
            test_path=self.test_path,
            command=cmd,
        )
        return test

    @property
    def read_throughput(self):
        """
        Test read throughput by performing sequential writes with multiple parallel streams (8+),
        using an I/O block size of 1 MB and an I/O depth of at least 64
        """
        cmd = "sudo fio --name=read_throughput --directory={0} --numjobs=8 " \
              "--size=10G --time_based --runtime=60s --ramp_time=2s --ioengine=libaio " \
              "--direct=1 --verify=0 --bs=1M --iodepth=64 --rw=read --group_reporting=1".format(self.test_path)
        test = TestProfile(
            name="read_throughput",
            desc=self.read_throughput.__doc__,
            test_path=self.test_path,
            command=cmd,
        )
        return test

    @property
    def write_iops(self):
        """
        Test write IOPS by performing sequential writes,
        using an I/O block size of 4 KB and an I/O depth of at least 64
        """
        cmd = "sudo fio --name=write_iops --directory={0} --size=10G " \
              "--time_based --runtime=60s --ramp_time=2s --ioengine=libaio " \
              "--direct=1 --verify=0 --bs=4K --iodepth=64 --rw=randwrite " \
              "--group_reporting=1".format(self.test_path)
        test = TestProfile(
            name="write_iops",
            desc=self.write_iops.__doc__,
            test_path=self.test_path,
            command=cmd,
        )
        return test

    @property
    def read_iops(self):
        """
        Test read IOPS, using an I/O block size of 4 KB and an I/O depth of at least 64
        """
        cmd = "sudo fio --name=read_iops --directory={0} --size=10G " \
              "--time_based --runtime=60s --ramp_time=2s --ioengine=libaio --direct=1 " \
              "--verify=0 --bs=4K --iodepth=64 --rw=randread --group_reporting=1".format(self.test_path)
        test = TestProfile(
            name="read_iops",
            desc=self.read_iops.__doc__,
            test_path=self.test_path,
            command=cmd,
        )
        return test


class GoogleRawBenchmarking(object):
    """
    Benchmarking raw disk performance
    https://cloud.google.com/compute/docs/disks/benchmarking-pd-performance#existing-disk
    """
    def __init__(self, device):
        self.device = device  # eg: /dev/sdb

    @property
    def fill_disk(self):
        """
        Fill the disk with nonzero data. Persistent disk reads from empty blocks
        have a latency profile that is different from blocks that contain data.
        We recommend filling the disk before running any read latency benchmarks.
        """
        # --filename=/dev/sdb
        cmd = "sudo fio --name=fill_disk --filename={0} --filesize=2500G " \
              "--ioengine=libaio --direct=1 --verify=0 --randrepeat=0 " \
              "--bs=128K --iodepth=64 --rw=randwrite".format(self.device)
        test = TestProfile(
            name="raw_fill_disk",
            desc=self.fill_disk.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def write_bandwidth(self):
        """
        Test write bandwidth by performing sequential writes with multiple parallel streams (8+),
        using 1 MB as the I/O size and having an I/O depth that is greater than or equal to 64.
        """
        cmd = "sudo fio --name=fill_disk --filename={0} --filesize=2500G " \
              "--ioengine=libaio --direct=1 --verify=0 --randrepeat=0 " \
              "--bs=128K --iodepth=64 --rw=randwrite".format(self.device)
        test = TestProfile(
            name="raw_write_bandwidth",
            desc=self.write_bandwidth.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def write_iops(self):
        """
        Test write IOPS. To achieve maximum PD IOPS, you must maintain a deep I/O queue.
        If, for example, the write latency is 1 millisecond, the VM can achieve,
        at most, 1,000 IOPS for each I/O in flight.
        To achieve 15,000 write IOPS, the VM must maintain at least 15 I/Os in flight.
        If your disk and VM are able to achieve 30,000 write IOPS,
        the number of I/Os in flight must be at least 30 I/Os.
        If the I/O size is larger than 4 KB, the VM might reach the bandwidth limit
        before it reaches the IOPS limit.
        """
        cmd = "sudo fio --name=write_iops_test --filename={0} --filesize=2500G " \
              "--time_based --ramp_time=2s --runtime=1m --ioengine=libaio --direct=1 " \
              "--verify=0 --randrepeat=0 --bs=4K --iodepth=256 --rw=randwrite".format(self.device)
        test = TestProfile(
            name="raw_write_iops",
            desc=self.write_iops.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def write_latency(self):
        """
        Test write latency. While testing I/O latency, the VM must not reach maximum bandwidth or IOPS;
        otherwise, the observed latency won't reflect actual persistent disk I/O latency.
        For example, if the IOPS limit is reached at an I/O depth of 30 and the fio command has double that,
        then the total IOPS remains the same and the reported I/O latency doubles.
        """
        cmd = "sudo fio --name=write_latency_test --filename={0} --filesize=2500G " \
              "--time_based --ramp_time=2s --runtime=1m --ioengine=libaio --direct=1 " \
              "--verify=0 --randrepeat=0 --bs=4K --iodepth=4 --rw=randwrite".format(self.device)
        test = TestProfile(
            name="raw_write_latency",
            desc=self.write_latency.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def read_bandwidth(self):
        """
        Test read bandwidth by performing sequential reads with multiple parallel streams (8+),
        using 1 MB as the I/O size and having an I/O depth that is equal to 64 or greater.
        """
        cmd = "sudo fio --name=read_bandwidth_test --filename={0} --filesize=2500G " \
              "--time_based --ramp_time=2s --runtime=1m --ioengine=libaio --direct=1 " \
              "--verify=0 --randrepeat=0 --bs=1M --iodepth=64 --rw=read --numjobs=8 " \
              "--offset_increment=100G".format(self.device)
        test = TestProfile(
            name="raw_read_bandwidth",
            desc=self.read_bandwidth.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def read_iops(self):
        """
        Test read IOPS. To achieve the maximum PD IOPS, you must maintain a deep I/O queue.
        If, for example, the I/O size is larger than 4 KB, the VM might reach the bandwidth
        limit before it reaches the IOPS limit. To achieve the maximum 100k read IOPS,
        specify --iodepth=256 for this test.
        """
        cmd = "sudo fio --name=read_iops_test  --filename={0} --filesize=2500G " \
              "--time_based --ramp_time=2s --runtime=1m --ioengine=libaio --direct=1 " \
              "--verify=0 --randrepeat=0 --bs=4K --iodepth=256 --rw=randread".format(self.device)
        test = TestProfile(
            name="raw_read_iops",
            desc=self.read_iops.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def read_latency(self):
        """
        Test read latency. It's important to fill the disk with data to get a realistic latency measurement.
        It's important that the VM not reach IOPS or throughput limits during this test because after the
        persistent disk reaches its saturation limit, it pushes back on incoming I/Os and this is
        reflected as an artificial increase in I/O latency.
        """
        cmd = "sudo fio --name=read_latency_test --filename={0} --filesize=2500G " \
              " --time_based --ramp_time=2s --runtime=1m  --ioengine=libaio --direct=1 " \
              "--verify=0 --randrepeat=0  --bs=4K --iodepth=4 --rw=randread".format(self.device)
        test = TestProfile(
            name="raw_read_latency",
            desc=self.read_latency.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def seq_read_bandwidth(self):
        """Test sequential read bandwidth."""
        cmd = "sudo fio --name=seq_read_bandwidth_test --filename={0} --filesize=2500G " \
              "--time_based --ramp_time=2s --runtime=1m --ioengine=libaio --direct=1 --verify=0 " \
              "--randrepeat=0 --numjobs=4 --thread --offset_increment=500G --bs=1M " \
              "--iodepth=64 --rw=read".format(self.device)
        test = TestProfile(
            name="raw_seq_read_bandwidth",
            desc=self.seq_read_bandwidth.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test

    @property
    def seq_write_bandwidth(self):
        """Test sequential write bandwidth."""
        cmd = "sudo fio --name=seq_write_bandwidth_test  --filename={0} --filesize=2500G " \
              "--time_based --ramp_time=2s --runtime=1m --ioengine=libaio --direct=1 --verify=0 " \
              "--randrepeat=0 --numjobs=4 --thread --offset_increment=500G --bs=1M " \
              "--iodepth=64 --rw=write".format(self.device)
        test = TestProfile(
            name="raw_seq_write_bandwidth",
            desc=self.seq_write_bandwidth.__doc__,
            test_path=self.device,
            command=cmd,
        )
        return test


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.fio = FIO("/mnt/test")

    def test_01(self):
        self.fio.sanity()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
