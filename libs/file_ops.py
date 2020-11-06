#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : file_ops.py
@Time  : 2020/10/26 15:43
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import time
import sys
import os
import hashlib
import unittest

from libs.log import log
from libs import utils

logger = log.get_logger()


class Consistency(object):
    """Test the file consistency"""
    def __init__(self):
        self.help = """
Storage-Consistency-Test:
    A python script for test.sh the file consistency between 2 path(or cloud). 
    It could be use for s3fs or other fuse based tool test.sh.
    
    Usage: cst.py cmd [path] [num] [size(k)]
    
    create 50 files, size 10k test.sh file in the /mnt/s3/test01 dir.(this dir has been mount to s3)
    #python cst.py create /mnt/s3/test01 50 10
    create 50 file(s), time:6.90075492859(seconds)
    
    create 50 files, size 10k test.sh file in the test01 dir.(local disk)
    #python cst.py create test01 50 10
    create 50 file(s), time:0.0640368461609(seconds)
    
    compare the local dir and s3fs mount point
    #python cst.py compare test01 /mnt/s3/test01 10
    compare 10 file(s), equal: 100.0% time:0.520743846893(seconds)
    
    update local files to 15k
    #python cst.py create test01 50 15 
    create 50 file(s), time:0.0967829227448(seconds)
    
    update s3fs files to 15k
    #python cst.py create /mnt/s3/test01 50 15
    create 50 file(s), time:7.60858488083(seconds)
    
    compare files on test.sh server B, all files update failure
    #python cst.py compare test01 /mnt/s3/test01 10
    compare 10 file(s), equal: 0.0% time:0.741319894791(seconds)
        """

    @staticmethod
    def create(top_path, f_num, f_size):
        utils.mkdir_path(top_path)
        start = time.time()
        for idx in range(0, int(f_num)):
            f = open(top_path + "/test_" + str(idx) + ".txt", "w")
            for line in range(0, 105 * int(f_size)):
                f.write(str(idx) + " " + str(line) + " line\n")
            f.close()
        end = time.time()
        during = end - start
        logger.info("{0}: create {1} file(s), time: {2}(seconds)".format(
            top_path, f_num, during))
        return True

    @staticmethod
    def compare(path_1, path_2, f_num):
        start = time.time()
        equal_num = 0
        for idx in range(0, int(f_num)):
            f_path_1 = open(path_1 + "/test_" + str(idx) + ".txt", "r")
            data_path_1 = f_path_1.read()

            filename = path_2 + "/test_" + str(idx) + ".txt"
            try:
                f_path_2 = open(filename, "r")
                data_path_2 = f_path_2.read()
                if hashlib.sha224(data_path_1.encode()).hexdigest() == hashlib.sha224(data_path_2.encode()).hexdigest():
                    equal_num += 1
            except IOError as e:
                logger.error(filename + ":file not exist")
                raise e
        end = time.time()
        during = end - start
        equal_rate = float(equal_num) / int(f_num) * 100
        logger.info("Compare path1:{0}; path2: ".format(path_1, path_2))
        if equal_num <= f_num:
            logger.error("Compared {0} file(s), equal: {1}% time: {2}(seconds)".format(
                f_num, equal_rate, during))
            raise Exception("Consistency Test FAIL")
        logger.info("Compared {0} file(s), equal: {1}% time: {2}(seconds)".format(
            f_num, equal_rate, during))
        return True

    def test(self):
        if len(sys.argv) < 2:
            print('Usage: ' + sys.argv[0] + ' cmd [path] [num] [size(k)]\n' + self.help)
        else:
            cmd = sys.argv[1]
            path = "test.sh"
            if len(sys.argv) >= 3:
                path = sys.argv[2]

            if cmd == "create":
                num = 500
                size = 1
                if len(sys.argv) >= 4:
                    num = sys.argv[3]
                if len(sys.argv) >= 5:
                    size = sys.argv[4]
                self.create(path, num, size)
                exit(0)
            elif cmd == "compare":
                path2 = ""
                if len(sys.argv) >= 4:
                    path2 = sys.argv[3]
                else:
                    print("need two paths for compare.")
                    exit(1)
                num = 500
                if len(sys.argv) >= 5:
                    num = sys.argv[4]
                self.compare(path, path2, num)
                exit(0)


class FileOpsTestCase(unittest.TestCase):
    """file ops test.sh case"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_consistency(self):
        cst = Consistency()
        print(cst.__doc__)
        self.assertTrue(cst.create('/tmp/dir_1', 500, 1))
        self.assertTrue(cst.create('/tmp/dir_2', 500, 1))
        self.assertTrue(cst.compare('/tmp/dir_1', '/tmp/dir_2', 500))


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(FileOpsTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
