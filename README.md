# Storage Test
Various methods/tools/scripts for storage test.

If you have any questions or requirements, please let me know. 
[tao.xu2008@outlook.com](tao.xu2008@outlook.com)


Support Types:
- raw   (base device)
- mnt   (base dir)
- cloud (base url)

# Quick Start
```shell script
git clone https://github.com/txu2k8/storage-test.git

import as a third-part pakage:
pip install storagetest
```

# Usage
```commandline
========================================================================
~# python storage_test.py -h
Storage Test Project

positional arguments:
  {mnt,raw,cloud}       Storage Test
    mnt                 base dir
    raw                 base device
    cloud               base url

optional arguments:
  -h, --help            show this help message and exit
  --debug               debug mode
  --duration DURATION   duration time(s),default:60*60*24*3 (3 days)
  --loops LOOPS         run loops(0:keep run forever),default:0
  --mail_to MAIL_TO     mail_to, split with ';'
  --output OUTPUT       output log dir path, default:None
  --runner {TextTestRunner,StressRunner,pytest}
                        Run test case with runner,default:StressRunner

========================================================================
~# python storage_test.py mnt -h
positional arguments:
  {benchmark,sanity,stress,load}
                        Test on a filesystem mount point
    benchmark           storage->mnt benchmark test
    sanity              storage->mnt sanity test
    stress              storage->mnt stress test
    load                storage->mnt load data file tools

optional arguments:
  -h, --help            show this help message and exit

========================================================================
~# python storage_test.py mnt stress -h
optional arguments:
  -h, --help            show this help message and exit
  --test_path TEST_PATH, -d TEST_PATH
                        A full path for test,default:None
  --exclude_case EXCLUDE_CASE_LIST [EXCLUDE_CASE_LIST ...]
                        exclude test case list, eg:acl doio fio, default:[]
  --case {acl,aio,compilebench,consistency,create_files,doio,filebench,fileops,fio,fs_di,fs_mark,fsstress,fstest,iozone,locktests,postmar
k,readall,stream} [{acl,aio,compilebench,consistency,create_files,doio,filebench,fileops,fio,fs_di,fs_mark,fsstress,fstest,iozone,locktes
ts,postmark,readall,stream} ...]
                        default:['all]

Test Case List:
  NO. CaseName                   CaseDescription
  1   acl                        Test ACL and Extend Attribute on Linux system
  2   aio                        a-synchronous I/O benchmark
  3   compilebench               Simulating disk IO common in creating, compiling, patching, stating and reading kernel trees.
  4   consistency                Test the file consistency
  5   create_files               Creates files of specified size
  6   doio                       base rw test: LTP doio & iogen; growfiles
  7   filebench                  File System Workload test
  8   fileops                    Test the various of file operations
  9   fio                        FIO: Flexible I/O tester.
  10  fs_di                      Test FileSystem Data Integrity
  11  fs_mark                    The fs_mark benchmark tests synchronous write workloads
  12  fsstress                   filesystem stress with LTP tool fsstress
  13  fstest                     Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink
  14  iozone                     A benchmark tests for generates and measures a variety of file operations.
  15  locktests                  Test fcntl locking functions
  16  postmark                   Simulate small-file testing similar to the tasks endured by web and mail servers
  17  readall                    Perform a small read on every file in a directory tree.
  18  stream                     LTP file stream test

========================================================================
```
