#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : dbench_test.py
@Time  : 2020/11/19 18:10
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
loadfiles_tar = os.path.join(bin_path, 'loadfiles.tar.gz')
loadfiles_path = os.path.join(cur_dir, 'loadfiles')


class Dbench(PkgBase):
    """
    dbench
    https://openbenchmarking.org/test/pts/dbench
    =============
    A loadtester for various protocols such as iSCSI, NFS, SCSI, SMB.

    DBENCH is a tool to generate I/O workloads to either a filesystem or to
    a networked CIFS or NFS server. It can even talk to an iSCSI target.
    DBENCH can be used to stress a filesystem or a server to see which workload
    it becomes saturated and can also be used for preditcion analysis to determine
    "How many concurrent clients/applications performing this workload can my server
    handle before response starts to lag?"

    Usage: [OPTION...]
        -t, --timelimit=integer       timelimit
        -c, --loadfile=filename       loadfile
        -D, --directory=STRING        working directory
        -T, --tcp-options=STRING      TCP socket options
        -R, --target-rate=DOUBLE      target throughput (MB/sec)
        -s, --sync                    use O_SYNC
        -S, --sync-dir                sync directory changes
        -F, --fsync                   fsync on write
        -x, --xattr                   use xattrs
        --no-resolve                  disable name resolution simulation
        --clients-per-process=INT     number of clients per process
        --one-byte-write-fix          try to fix 1 byte writes
        --stat-check                  check for pointless calls with stat
        --fake-io                     fake up read/write calls
        --skip-cleanup                skip cleanup operations
        --per-client-results          show results per client
    """

    def __init__(self, top_path):
        super(Dbench, self).__init__(top_path)
        self.test_path = os.path.join(top_path, "dbench")

    def tests_generator(self, load_file, runtime=60, clients=(1, 6, 12, 48, 128, 256)):
        """
        Return dbench test case list
        """
        db_bin = os.path.join(bin_path, 'dbench')
        cmd = "{0} -c {1} -t {2} -D {3} {4}"
        tests = []
        for idx, client in enumerate(clients):
            desc = "{}clients".format(client)
            test_name = "dbench_{0}_{1}".format(idx + 1, to_safe_name(desc))
            test = TestProfile(
                name=test_name,
                desc=desc,
                test_path=self.test_path,
                bin_path=bin_path,
                command=cmd.format(db_bin, load_file, runtime, self.test_path, client))
            tests.append(test)
        return tests

    @staticmethod
    def tar_loadfiles():
        if not os.path.isdir(loadfiles_path):
            try:
                os.system("tar -zxvf {0} -C {1}".format(loadfiles_tar, cur_dir))
            except Exception as e:
                raise e
        return True

    def sanity(self):
        self.tar_loadfiles()
        load_file = os.path.join(loadfiles_path, 'client.txt')
        return self.run_tests(self.tests_generator(load_file, 60, (1,)))

    def stress(self):
        self.tar_loadfiles()
        load_file = os.path.join(loadfiles_path, 'client.txt')
        return self.run_tests(self.tests_generator(load_file, 600, (1, 6)))

    def benchmark(self):
        self.tar_loadfiles()
        load_file = os.path.join(loadfiles_path, 'client.txt')
        return self.run_tests(self.tests_generator(load_file, 600))


class UnitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Dbench("/mnt/test")

    def test_benchmark(self):
        self.db.benchmark()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
