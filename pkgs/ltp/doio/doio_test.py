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


class DoIO(object):
    """LTP doio"""

    def __init__(self, top_path):
        self.top_path = top_path

    def verify(self):
        if os.name != "posix":
            raise PlatformError("Just support for linux machine!")
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)


class RWTest(DoIO):
    """
    RWTest with: iogen & doio
    =============

    This is a pair of programs that does basic I/O operations on a set of files.
    The file offset, I/O length, I/O operation, and what open(2) flags are
    selected randomly from a pre-defined or commandline given set. All data
    written can be verified (this is the usual method).
    """

    def __init__(self, top_path):
        super(RWTest, self).__init__(top_path)
        pass

    def rwtest_cases(self, test_path):
        """
        Generate Test case list FYI:
        https://github.com/linux-test-project/ltp/blob/master/runtest/fs
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        rwtest_bin = os.path.join(cur_dir, 'bin/rwtest')

        tcs = [
            {
                "name": "rwtest01",
                "desc": "rw-sync",
                "cmd": "{0} -N rwtest01 -c -q -i 60s -f sync 10%25000:{1}/rw-sync-$$".format(rwtest_bin, test_path)
            },
            {
                "name": "rwtest02",
                "desc": "rw-buffered",
                "cmd": "{0} -N rwtest02 -c -q -i 60s -f buffered 10%25000:{1}/rw-buffered-$$".format(rwtest_bin, test_path)
            },
            {
                "name": "rwtest03",
                "desc": "rw-mem-buffered",
                "cmd": "{0} -N rwtest03 -c -q -i 60s -n 2 -f buffered -s mmread,mmwrite -m random -Dv 10%25000:{1}/mm-buff-$$".format(rwtest_bin, test_path)
            },
            {
                "name": "rwtest04",
                "desc": "rw-mm-sync",
                "cmd": "{0} -N rwtest04 -c -q -i 60s -n 2 -f sync -s mmread,mmwrite -m random -Dv 10%25000:{1}/mm-sync-$$".format(rwtest_bin, test_path)
            },
            {
                "name": "rwtest05",
                "desc": "rw-50-iterations",
                "cmd": "{0} -N rwtest01 -c -q -i 50 -T 64b 500b:{1}/rwtest01%f".format(rwtest_bin, test_path)
            },
            {
                "name": "rwtest06",
                "desc": "rw-sync",
                "cmd": "{0} -N iogen01 -i 120s -s read,write -Da -Dv -n 2 500b:{1}/doio.f1.$$ 1000b:{1}/doio.f2.$$".format(rwtest_bin, test_path)
            },
        ]

    def run(self, test_path):
        """
        Examples:
        ---------
        # run forever:  8 process - using record locks
        iogen -i 0 100000b:doio_1 | doio -av -n 8 -m 1000

        # run forever:  8 process - using record locks
        iogen -i 0 100000b:doio_2 | doio -akv -n 8 -m 1000
        """
        logger.info(self.run.__doc__)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        iogen_bin = os.path.join(cur_dir, 'bin/iogen')
        doio_bin = os.path.join(cur_dir, 'bin/doio')
        test_log = os.path.join(self.top_path, 'iogen.log')

        iogen_cmd = "{0} -i 120s -s read,write 500b:{1}doio.f1.$$ 1000b:{1}doio.f2.$$ | {2} -akv -n 2 | tee -a {3}".format(
            iogen_bin, test_path, doio_bin, test_log)

        try:
            os.system('chmod 777 {0}*'.format(iogen_cmd))
            rc, output = utils.run_cmd(iogen_cmd)
            logger.info('\n'.format(output.strip('\n')))
            logger.info("PASS: Run iogen/doio on {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run iogen/doio on {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "IOGen", "sanity")
        utils.mkdir_path(test_path)
        return self.run(test_path)

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "IOGen", "stress")
        utils.mkdir_path(test_path)
        return self.run(test_path)


class GrowFiles(DoIO):
    """
    GROWFILES
    =============

    Growfiles will create and truncate files in gradual steps using write, and
    lseek. All system calls are checked for proper returns. The writes or the
    whole file content can be verified.  It can cause disk fragmentation.

    Examples:
    ---------
    growfiles -E output:
    # run forever: writes of 4090 bytes then on every 100 iterval
    # truncate file by 408990 bytes.  Done to 200 files in dir1.
    growfiles -i 0 -g 4090 -T 100 -t 408990 -l -C 10 -c 1000 -d dir1 -S 200

    # same as above with writes of 5000 bytes and truncs of 499990
    growfiles -i 0 -g 5000 -T 100 -t 499990 -l -C 10 -c 1000 -d dir2 -S 200

    # runs forever: beats on opens and closes of file ocfile - no io
    growfiles -i 0 -g 0 -c 0 -C 0 ocfile

    # writes 4096 to files until 50 blocks are written
    growfiles -i 0 -g 4096 -B 50b file1 file2

    # write one byte to 750 files in gdir then unlinks them
    growfiles -g 1 -C 0 -d gdir -u -S 750

    # run 30 secs: random iosize, random lseek up to eof
    # Only valid for one growfile process per file.
    growfiles -r 1-5000 -R 0--1 -i 0 -L 30 -C 1 g_rand1 g_rand2

    # run 30 secs: grow by lseek then write single byte, trunc every 10 itervals
    growfiles -g 5000 -wlu -i 0 -L 30 -C 1 -T 10  g_sleek1 g_lseek2

    # run forever: 5 copies of random iosize, random lseek to beyond eof,
    # rand io types doing a trunc every 5 iterations, with unlinks.
    growfiles -i0 -r 1-50000 -R 0--2 -I r -C1 -l -n5 -u -U 100-200 gf_rana gf_ranb

    # run forever: 5 copies of random iosize, random lseek to beyond eof,
    # random open flags, rand io types doing a trunc every 10 iterations.
    growfiles -i0 -r 1-50000 -R 0--2 -o random -I r -C0 -l -T 20 -uU100-200 -n 5 gf_rand1 gf_rand2

    """

    def __init__(self, top_path):
        super(GrowFiles, self).__init__(top_path)
        pass


if __name__ == '__main__':
    rwt = RWTest("/tmp")
    rwt.sanity()
