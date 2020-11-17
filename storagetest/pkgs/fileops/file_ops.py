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
import shutil
import hashlib
import string
import random
import itertools
import unittest
from prettytable import PrettyTable

from storagetest.libs import utils, log
from storagetest.libs.schedule import enter_phase
from storagetest.libs.exceptions import NoSuchDir

logger = log.get_logger()


class Consistency(object):
    """Test the file consistency"""

    def __init__(self, top_path):
        self.top_path = top_path
        self.local_path = '/tmp/consistency_local'
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

    def verify(self):
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    @staticmethod
    def create(test_path, f_num, f_size):
        utils.mkdir_path(test_path)
        start = time.time()
        for idx in range(0, int(f_num)):
            f = open(test_path + "/test_" + str(idx) + ".txt", "w")
            for line in range(0, 105 * int(f_size)):
                f.write(str(idx) + " " + str(line) + " line\n")
            f.close()
        end = time.time()
        during = end - start
        logger.info("{0}: create {1} file(s), time: {2}(seconds)".format(
            test_path, f_num, during))
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
        logger.info("Compare path1:{0}; path2: {1}".format(path_1, path_2))
        if equal_num < f_num:
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

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "consistency")
        try:
            self.create(self.local_path, 500, 1)
            self.create(test_path, 500, 1)
            self.compare(self.local_path, test_path, 500)
            return True
        except Exception as e:
            raise e

    def stress(self):
        self.verify()
        test_top_path = os.path.join(self.top_path, "consistency")
        try:
            self.create(self.local_path, 1000, 1)
            for x in range(0, 100):
                test_path = os.path.join(test_top_path, 'dir{0}'.format(x))
                self.create(test_path, 1000, 1)
                self.compare(self.local_path, test_path, 1000)
            return True
        except Exception as e:
            raise e


class FileOps(object):
    """The various file operations"""

    def __init__(self):
        pass

    # ==== file ops ====
    @staticmethod
    def file_name_generator(files_num, file_type="txt"):
        for i in range(files_num):
            file_name = "file_{0}.{1}".format(i, file_type)
            yield file_name

    @staticmethod
    def random_bytes(n):
        """returns a byte array of random bytes"""
        return bytearray(random.getrandbits(8) for _ in range(n))

    @staticmethod
    def random_string(str_len=16):
        """
        generate random string
        return ''.join(random.sample((string.ascii_letters + string.digits)*str_len, str_len))
        :param str_len: byte
        :return:random_string
        """

        base_string = string.ascii_letters + string.digits
        # base_string = string.printable
        base_string_len = len(base_string)
        multiple = 1
        if base_string_len < str_len:
            multiple = (str_len // base_string_len) + 1

        return ''.join(random.sample(base_string * multiple, str_len))

    @staticmethod
    def hash_md5(file_path):
        """
        returns the hash md5 of the opened file
        :param file_path: file full path
        :return:(string) md5_value 32-bit hexadecimal string.
        """
        logger.debug('Get MD5: {0}'.format(file_path))
        try:
            h_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(), b""):
                    h_md5.update(chunk)
            return h_md5.hexdigest()
        except Exception as e:
            raise Exception(e)

    def create_file(self, file_path, total_size='4k', line_size=128, mode='w+'):
        """
        create original file, each line with line_number, and specified line size
        :param file_path:
        :param total_size:
        :param line_size:
        :param mode: w+ / a+
        :return:
        """

        original_path = os.path.split(file_path)[0]
        if not os.path.isdir(original_path):
            try:
                os.makedirs(original_path)
            except OSError as e:
                raise Exception(e)

        size = utils.strsize_to_byte(total_size)
        line_count = size // line_size
        unaligned_size = size % line_size

        with open(file_path, mode) as f:
            logger.debug("write file: {0}".format(file_path))
            for line_num in range(0, line_count):
                random_sting = self.random_string(line_size - 2 - len(str(line_num))) + '\n'
                f.write('{line_num}:{random_s}'.format(line_num=line_num, random_s=random_sting))
            if unaligned_size > 0:
                f.write(self.random_string(unaligned_size))
            f.flush()
            os.fsync(f.fileno())

        file_md5 = self.hash_md5(file_path)
        return file_md5

    def modify_file(self, file_path):
        return self.create_file(file_path, '4k', 128, mode='a+')

    def create_large_size_file(self, file_path, size='4k'):
        """Create large size enpty file"""
        size_b = utils.strsize_to_byte(size)
        with open(file_path, "wb") as out:
            out.truncate(size_b)
        file_md5 = self.hash_md5(file_path)
        return file_md5

    @staticmethod
    def rename_file(file_path, suffix="_new"):
        """return new_file_path"""
        try:
            file_name = os.path.basename(file_path)
            file_dirname = os.path.dirname(file_path)
            file_name_split = file_name.split(".")
            new_file_name = "{0}{1}.{2}".format(file_name_split[0], suffix, file_name_split[1])
            new_file_path = os.path.join(file_dirname, new_file_name)
            os.rename(file_path, new_file_path)
            return new_file_path
        except Exception as e:
            logger.error("Error renaming the file {}".format(file_path))
            raise e

    @staticmethod
    def delete_files(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error("Failed delete the file {}".format(file_path))
            raise e

    # ==== dir ops ====
    def create_dirs(self, parent_path, dirs_num, name_prefix="Dir"):
        """method to create number of dirs and return dir_names list"""
        logger.info("Create {0} dirs under path: {1}".format(dirs_num, parent_path))
        dir_path_list = []
        for x in range(dirs_num):
            dir_name = "{0}_{1}".format(name_prefix, x)
            dir_path = os.path.join(parent_path, dir_name)
            utils.mkdir_path(dir_path)
            dir_path_list.append(dir_path)
        return dir_path_list

    def create_sub_dirs(self, parent_path, dirs_num):
        """Created subdir inside the parent_dir"""
        return self.create_dirs(parent_path, dirs_num, "SubDir")

    def create_nested_dirs(self, parent_path, level):
        logger.info("Create nested dirs under path: {0}, level={1}".format(parent_path, level))
        tmp = [[parent_path]]  # temp list storing the TopLevel dir
        nested_dir_path = []
        for i in range(level):
            tmp.append(["Nested_" + str(i)])
        for item in itertools.product(*tmp):
            dir_path = os.path.join(parent_path, *item)
            utils.mkdir_path(dir_path)
            tmp.append(dir_path)
            nested_dir_path.append(os.path.join(*item))
        return nested_dir_path

    @staticmethod
    def rename_dirs(dir_path_list, suffix="_new"):
        """Rename the dir by add suffix"""
        logger.info("Rename all dirs with suffix: {}".format(suffix))
        new_dir_path_list = []
        for dir_path in dir_path_list:
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                logger.debug("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                new_dir_path_list.append(new_dir_path)
            else:
                raise Exception("{0} does not exist".format(dir_path))
        return new_dir_path_list

    @staticmethod
    def remove_dir(dir_path):
        """rm dir tree"""
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)
        else:
            raise Exception("{0} does not exist".format(dir_path))

    @staticmethod
    def list_dirs(dir_path_list):
        """list the dirs"""
        for dir_path in dir_path_list:
            if os.path.isdir(dir_path):
                for dirname, dirnames, filenames in os.walk(dir_path):
                    # print(dirname)
                    pass
            else:
                raise Exception("Error: {0} does not exist".format(dir_path))
        logger.info("PASS: All the directories created exist")

    # ==== acls/attributes ops ====
    @staticmethod
    def add_attributes(dir_path):
        """attrib +a/r/h/s"""
        try:
            os.system("attrib +a " + dir_path)
            os.system("attrib +r " + dir_path)
            os.system("attrib +h " + dir_path)
            # os.system("attrib +s " +dir_path)
        except Exception as e:
            logger.error("Error setting attribute to dir {}".format(dir_path))
            raise e

    @staticmethod
    def remove_attributes(dir_path):
        """attrib -a/r/h/s"""
        try:
            os.system("attrib -a " + dir_path)
            os.system("attrib -r " + dir_path)
            os.system("attrib -h " + dir_path)
            # os.system("attrib -s " + dir_path)
        except Exception as e:
            logger.error("Error removing attribute to dir {}".format(dir_path))
            raise e

    @staticmethod
    def add_acls(dir_path):
        """icacls /dir /grant Everyone:(OI)(CI)F"""
        try:
            # os.system("icacls " + dir_path + " /grant Everyone:f")
            os.system("icacls " + dir_path + " /grant user63:(OI)(CI)F")
        except Exception as e:
            logger.error("Error setting acls to dir {}".format(dir_path))
            raise e

    @staticmethod
    def remove_acls(dir_path):
        """icacls /dir /remove Everyone:g"""
        try:
            # os.system("icacls " + dir_path + " /remove Everyone:g")
            os.system("icacls " + dir_path + " /remove user63:g")
        except Exception as e:
            logger.error("Error setting acls to dir {}".format(dir_path))
            raise e


class LocalFileOps(FileOps):
    """The various of file operations on local File System mount path"""

    def __init__(self, top_path):
        super(LocalFileOps, self).__init__()
        self.top_path = top_path
        self.phase_list = []  # PrettyTable(['Step', 'Result', 'Comments'])

        self.Dirs = []  # dir path list after creation
        self.SubDirs = []  # sub dirs inside a parent_dir
        self.NestedDirs = []  # nested dir inside a parent_dir
        self.Files = []  # files inside a dir provided
        self.Md5Csum = {}  # dict with filename as the key to hold md5 checksum, {"f_name":"md5"}

    def verify(self):
        if not os.path.isdir(self.top_path):
            raise NoSuchDir(self.top_path)

    @staticmethod
    def large_file_name_generator(files_num, file_type="dat"):
        for i in range(files_num):
            file_name = "large_file_{0}.{1}".format(i, file_type)
            yield file_name

    @enter_phase()
    def test_check_files_md5(self):
        """Check files md5 match in dict Md5Csum"""
        table_err = PrettyTable(['File', 'Expected', 'Actual'])
        for file_path, expected_md5 in self.Md5Csum.items():
            actual_md5 = self.hash_md5(file_path)
            if actual_md5 != expected_md5:
                table_err.add_row([file_path, expected_md5, actual_md5])
                continue
        if len(table_err._rows) > 0:
            logger.error("Md5sum Check:\n".format(table_err))
            raise Exception("FAILED: File md5 NOT matched!")
        return True

    @enter_phase()
    def test_create_dirs(self, test_path, dirs_num):
        """Create dirs"""
        self.Dirs = self.create_dirs(test_path, dirs_num)
        return True

    @enter_phase()
    def test_list_dirs(self):
        """List dirs, sub dirs, nested dirs"""
        self.list_dirs(self.Dirs)
        self.list_dirs(self.SubDirs)
        self.list_dirs(self.NestedDirs)
        return True

    @enter_phase()
    def test_create_sub_dirs(self, sub_dirs_num):
        """Create sub dirs"""
        for the_dir in self.Dirs:
            self.SubDirs.extend(self.create_sub_dirs(the_dir, sub_dirs_num))
        return True

    @enter_phase()
    def test_create_nested_dirs(self, nested_level):
        """Create nested dirs"""
        for the_dir in self.Dirs:
            self.NestedDirs.extend(self.create_nested_dirs(the_dir, nested_level))
        return True

    @enter_phase()
    def test_create_files(self, files_num, file_size):
        """Create files inside all dirs"""
        logger.info("Create {0} files under all dirs(size:{1})".format(files_num, file_size))
        for the_dir in self.Dirs + self.SubDirs + self.NestedDirs:
            for f_name in self.file_name_generator(files_num):
                file_path = os.path.join(the_dir, f_name)
                md5 = self.create_file(file_path, file_size, 128, 'w+')
                self.Md5Csum[file_path] = md5
                self.Files.append(file_path)
        return True

    @enter_phase()
    def test_create_large_files(self, files_num, file_size):
        """Create files inside dirs"""
        logger.info("Create {0} large size files under all dirs(size:{1})".format(files_num, file_size))
        for the_dir in self.Dirs:  # + self.SubDirs + self.NestedDirs
            for f_name in self.large_file_name_generator(files_num):
                file_path = os.path.join(the_dir, f_name)
                md5 = self.create_large_size_file(file_path, file_size)
                self.Md5Csum[file_path] = md5
                self.Files.append(file_path)
        return True

    @enter_phase()
    def test_modify_files(self):
        """Modify files by write a+"""
        logger.info("Modify files by write a+(extend size:1k)")
        for file_path in self.Files:
            md5 = self.create_file(file_path, "1K", 128, 'a+')
            self.Md5Csum[file_path] = md5
        return True

    @enter_phase()
    def test_rename_files(self):
        """Rename files"""
        logger.info("Rename files with suffix: _new")
        renamed_files = []
        renamed_md5csum = {}
        for file_path in self.Files:
            new_file_path = self.rename_file(file_path, suffix="_new")
            renamed_md5csum[new_file_path] = self.Md5Csum[file_path]
            renamed_files.append(new_file_path)
        self.Files = renamed_files
        self.Md5Csum = renamed_md5csum
        return True

    @enter_phase()
    def test_delete_files(self):
        """Delete some of files(The latest 5 files)"""
        for file_path in self.Files[-5:]:
            self.delete_files(file_path)
        return True

    @enter_phase()
    def test_rename_dirs(self):
        """Rename dirs, sub dirs, nested dirs"""
        self.NestedDirs = self.rename_dirs(self.NestedDirs, suffix="_new")
        self.SubDirs = self.rename_dirs(self.SubDirs, suffix="_new")
        self.Dirs = self.rename_dirs(self.Dirs, suffix="_new")
        return True

    @enter_phase()
    def test_remove_dirs(self):
        """Delete some of dirs(rmtree the latest 3 dirs)"""
        for dir_path in self.Dirs[-3:]:
            self.remove_dir(dir_path)
        return True

    def run(self, test_path, dirs_num=10, nested_level=10, files_num=100, file_size='1K'):
        utils.mkdir_path(test_path)
        try:
            # Create dirs
            self.test_create_dirs(test_path, dirs_num)

            # Create sub dirs
            self.test_create_sub_dirs(dirs_num)

            # Create nested dirs
            self.test_create_nested_dirs(nested_level)

            # Create files
            self.test_create_files(files_num, file_size)

            # Create large files
            self.test_create_large_files(random.randint(1, 3), "100M")

            # List dirs
            self.test_list_dirs()

            # Modify files
            self.test_check_files_md5()
            self.test_modify_files()

            # Rename files
            self.test_check_files_md5()
            self.test_rename_files()
            self.test_check_files_md5()

            # Delete some of files
            self.test_delete_files()

            # Rename dirs
            self.test_rename_dirs()

            # rmtree dir_path
            self.test_remove_dirs()

            logger.info("PASS: Run FileOps test on local FS {0}".format(test_path))
        except Exception as e:
            logger.info("FAIL: Run FileOps test on local FS {0}".format(test_path))
            raise e
        finally:
            pass

        return True

    def sanity(self):
        self.verify()
        test_path = os.path.join(self.top_path, "LocalFileOps")
        return self.run(test_path, 3, 10, 10, "1k")

    def stress(self):
        self.verify()
        test_path = os.path.join(self.top_path, "LocalFileOps")
        return self.run(test_path, 10, 10, 100, "4k")


class GlobalMetaFileOps(FileOps):
    """The various file operations on a Global File System TODO"""

    def __init__(self):
        super(GlobalMetaFileOps, self).__init__()
        self.Dirs = []  # this will store all directory names after creation
        self.NewDirs = []  # this will store directory names after rename
        self.NestedDirs = []  # this will store nested directory under a TopLevelDir
        self.NewNestedDirs = []  # this will store the nested dirs after rename
        self.SubDirs = []  # this will store subdirs inside a Dir
        self.NewSubDirs = []  # this will store new subdirs after rename
        self.Files = []  # this will store all files inside a dir provided
        self.NewFiles = []  # this will store all files after renames
        self.FilesAfterDirRename = []  # this will store all files after dir renames
        self.FilesCreatedBeforeDirRename = []  # this will store all files after dir renames
        self.FilesInSubDir = []  # this will store all files in subdir
        self.FilesInNestedDir = []  # this will store all files in nested dir
        self.FilesInNewNestedDir = []  # this will store all files after nested dir rename
        self.Md5Csum = {}  # dict with filename as the key to hold md5 checksum after file creation
        self.TopLevelDir = "Dir_" + time.strftime("%H%M%S")

    def create_dirs(self, drive, dirs_num, name_prefix="Dir"):
        """method to create number of dirs and save dir_name in a list"""
        for x in range(dirs_num):
            dir_name = "{0}_{1}_{2}".format(name_prefix, time.strftime("%H%M%S"), x)
            dir_path = os.path.join(drive, dir_name)
            utils.mkdir_path(dir_path)
            self.Dirs.append(dir_name)

    def create_nested_dirs(self, parent_path, levels):
        tmp = [[self.TopLevelDir]]  # temp list storing the TopLevel dir
        dir_nested_path = []
        for i in range(levels):
            tmp.append(["S_" + str(i)])
        for item in itertools.product(*tmp):
            dir_path = os.path.join(parent_path, *item)
            utils.mkdir_path(dir_path)
            tmp.append(dir_path)
            dir_nested_path = os.path.join(*item)

        self.Dirs.append(self.TopLevelDir)
        self.NestedDirs.append(dir_nested_path)

    def create_sub_dirs(self, drive, parent_dir):
        """Created subdir inside the parent_dir"""
        sub_dir_name = "SubDir_" + time.strftime("%H%M%S")
        dir_path = os.path.join(drive, parent_dir, sub_dir_name)
        utils.mkdir_path(dir_path)
        tmp_path = os.path.join(parent_dir, sub_dir_name)
        self.SubDirs.append(tmp_path)

    def rename_dirs(self, drive, suffix="_new"):
        """Rename the dir by add suffix"""
        for the_dir in self.Dirs:
            dir_path = os.path.join(drive, the_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                logger.debug("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                self.NewDirs.append(the_dir + suffix)

                # Update the files path under the dir
                new_files_path = []
                dirname = ""
                for dirname, dirnames, filenames in os.walk(new_dir_path):
                    new_files_path = filenames
                # logger.debug(new_files_path)
                for new_file_path in new_files_path:
                    tmp_path = os.path.join(drive, dirname)
                    new_path = os.path.join(tmp_path, new_file_path)
                    # logger.debug(new_path)
                    self.FilesCreatedBeforeDirRename.append(new_path)
            else:
                raise Exception("{0} does not exist".format(dir_path))

    def rename_nested_dirs(self, drive, suffix="_new"):
        """Rename the nested dir by add suffix"""
        for nested_dir in self.NestedDirs:
            dir_path = os.path.join(drive, nested_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                logger.debug("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                self.NewNestedDirs.append(nested_dir + suffix)
            else:
                raise Exception("{0} does not exist".format(dir_path))

    def rename_subdir(self, drive, suffix="_new"):
        """Rename the nested dir by add suffix"""
        for sub_dir in self.SubDirs:
            dir_path = os.path.join(drive, sub_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                logger.debug("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                self.NewSubDirs.append(sub_dir + suffix)
            else:
                raise Exception("{0} does not exist".format(dir_path))


class UnitTestCase(unittest.TestCase):
    """file ops test.sh case"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_consistency(self):
        cst = Consistency("/tmp/")
        logger.info(cst.__doc__)
        self.assertTrue(cst.create('/tmp/dir_1', 500, 1))
        self.assertTrue(cst.create('/tmp/dir_2', 500, 1))
        self.assertTrue(cst.compare('/tmp/dir_1', '/tmp/dir_2', 500))


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
