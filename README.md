# storage-test
Storage Test tools/scripts

# Usage
```commandline
========================================================================
~# python storage_test.py -h
Storage Test Project

positional arguments:
  {mnt,raw,cloud}       storage test
    mnt                 storage test: mnt
    raw                 storage test: raw
    cloud               storage test: cloud

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
  {sanity,stress,load}  Test on a filesystem mount point
    sanity              storage->mnt sanity test
    stress              storage->mnt stress test
    load                storage->mnt load data files

optional arguments:
  -h, --help            show this help message and exit

========================================================================
~# python storage_test.py mnt stress -h
optional arguments:
  -h, --help            show this help message and exit
  --test_path TEST_PATH, -d TEST_PATH
                        A full path for test,default:None
  --case {consistency,create_files,fs_di,fstest,fsstress,filebench,locktests,doio,stream,readall} [{consistency,create_files,fs_di,fstest
,fsstress,filebench,locktests,doio,stream,readall} ...]
                        default:['all]

Test Case List:
  NO. CaseName                   CaseDescription
  1   consistency                Test the file consistency
  2   create_files               Creates files of specified size
  3   fs_di                      Test FileSystem Data Integrity
  4   fstest                     Test FS function:chmod, chown, link, mkdir, mkfifo, open, rename, rmdir, symlink, truncate, unlink
  5   fsstress                   filesystem stress with LTP tool fsstress
  6   filebench                  File System Workload test
  7   locktests                  Test fcntl locking functions
  8   doio                       base rw test: LTP doio & iogen
  9   stream                     LTP file stream test
  10  readall                    Perform a small read on every file in a directory tree.
========================================================================
```
