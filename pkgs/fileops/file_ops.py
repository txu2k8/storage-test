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

from libs import log
from libs import utils
from libs.exceptions import NoSuchDir

logger = log.get_logger()


class Consistency(object):
    """Test the file consistency"""
    def __init__(self, top_path):
        self.top_path = top_path
        self.local_path = '/tmp/consistency'
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
    def file_name_generator(self):
        pass

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

        logger.info('>> Create file: {0}'.format(file_path))
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
            logger.info("write file: {0}".format(file_path))
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
    def rename_files(file_path, suffix="_new"):
        try:
           file_name = os.path.basename(file_path)
           file_name_split = file_name.split(".")
           new_file_path = "{0}{1}.{2}".format(file_name_split[0], suffix, file_name_split[1])
           os.rename(file_path, new_file_path)
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
        dir_name_list = []
        str_time = time.strftime("%H%M%S")
        for x in range(dirs_num):
            dir_name = "{0}_{1}_{2}".format(name_prefix, str_time, x)
            dir_path = os.path.join(parent_path, dir_name)
            utils.mkdir_path(dir_path)
            dir_name_list.append(dir_name)
        return dir_name_list

    def create_sub_dirs(self, parent_path, dirs_num):
        """Created subdir inside the parent_dir"""
        return self.create_dirs(parent_path, dirs_num, "SubDir")

    def create_nested_dirs(self, parent_path, levels):
        tmp =[[parent_path]]  # temp list storing the TopLevel dir
        nested_dir_path=[]
        for i in range(levels):
            tmp.append(["Nested_"+str(i)])
        for item in itertools.product(*tmp):
            dir_path=os.path.join(parent_path, *item)
            utils.mkdir_path(dir_path)
            tmp.append(dir_path)
            nested_dir_path = os.path.join(*item)
        return nested_dir_path

    def rename_dir(self, parent_path, dir_list, suffix="_new"):
        """Rename the dir by add suffix"""
        new_dir_list =[]
        for the_dir in dir_list:
            dir_path=os.path.join(parent_path, the_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                print("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                new_dir_list.append(the_dir + suffix)
            else:
               raise Exception("{0} does not exist".format(dir_path))
        return new_dir_list

    @staticmethod
    def remove_dir(dir_path):
        """rm dir tree"""
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)
        else:
            raise Exception("{0} does not exist".format(dir_path))

    @staticmethod
    def list_dirs(parent_path, dirs, expected_dirs_num):
        """list the dirs[] and check number expected"""
        count = 0
        for the_dir in dirs:
            dir_path = os.path.join(parent_path, the_dir)
            if os.path.isdir(dir_path):
                for dirname, dirnames, filenames in os.walk(dir_path):
                    print(dirname)
                    count += 1
            else:
                print("Error: {0} does not exist".format(dir_path))
        if count != expected_dirs_num:
            raise Exception("FAIL: All the directories created dont exist")
        print("PASS: All the directories created exist")

    # ==== acls/attributes ops ==== TODO


class GlobalMetaFileOps(FileOps):
    """The various file operations on a Global File System"""
    def __init__(self):
        super(GlobalMetaFileOps, self).__init__()
        self.Dirs = []  # this will store all directory names after creation
        self.NewDirs = [] # this will store directory names after rename
        self.NestedDirs = [] # this will store nested directory under a TopLevelDir
        self.NewNestedDirs = [] # this will store the nested dirs after rename
        self.SubDirs = []  # this will store subdirs inside a Dir
        self.NewSubDirs = [] # this will store new subdirs after rename
        self.Files = []  # this will store all files inside a dir provided
        self.NewFiles = [] # this will store all files after renames
        self.FilesAfterDirRename = [] # this will store all files after dir renames
        self.FilesCreatedBeforeDirRename = [] # this will store all files after dir renames
        self.FilesInSubDir = []    # this will store all files in subdir
        self.FilesInNestedDir = [] # this will store all files in nested dir
        self.FilesInNewNestedDir = [] # this will store all files after nested dir rename
        self.Md5Csum = {}  # dict with filename as the key to hold md5 checksum after file creation
        self.TopLevelDir = "Dir_" + time.strftime("%H%M%S")

    def create_dirs(self, drive, dirs_num):
        """method to create number of dirs and save dir_name in a list"""
        for x in range(dirs_num):
            dir_name = "Dir_{0}_{1}".format(time.strftime("%H%M%S"), x)
            dir_path = os.path.join(drive, dir_name)
            utils.mkdir_path(dir_path)
            self.Dirs.append(dir_name)

    def create_nested_dirs(self, parent_path, levels):
        tmp =[[self.TopLevelDir]]  # temp list storing the TopLevel dir
        dir_nested_path=[]
        for i in range(levels):
            tmp.append(["S_"+str(i)])
        for item in itertools.product(*tmp):
            dir_path=os.path.join(parent_path, *item)
            utils.mkdir_path(dir_path)
            tmp.append(dir_path)
            dir_nested_path = os.path.join(*item)

        self.Dirs.append(self.TopLevelDir)
        self.NestedDirs.append(dir_nested_path)

    def create_sub_dirs(self, drive, parent_dir):
        """Created subdir inside the parent_dir"""
        sub_dir_name = "SubDir_" + time.strftime("%H%M%S")
        dir_path=os.path.join(drive, parent_dir, sub_dir_name)
        utils.mkdir_path(dir_path)
        tmp_path = os.path.join(parent_dir, sub_dir_name)
        self.SubDirs.append(tmp_path)

    def rename_dir(self, drive, suffix="_new"):
        """Rename the dir by add suffix"""
        for the_dir in self.Dirs:
            dir_path=os.path.join(drive, the_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                print("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                self.NewDirs.append(the_dir + suffix)

                # Update the files path under the dir
                new_files_path=[]
                dirname = ""
                for dirname, dirnames, filenames in os.walk(new_dir_path):
                  new_files_path=filenames
                # print(new_files_path)
                for new_file_path in new_files_path:
                    tmp_path = os.path.join(drive, dirname)
                    new_path = os.path.join(tmp_path, new_file_path)
                    # print(new_path)
                    self.FilesCreatedBeforeDirRename.append(new_path)
            else:
               raise Exception("{0} does not exist".format(dir_path))

    def rename_nested_dirs(self, drive, suffix="_new"):
        """Rename the nested dir by add suffix"""
        for nested_dir in self.NestedDirs:
            dir_path=os.path.join(drive, nested_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                print("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                self.NewNestedDirs.append(nested_dir + suffix)
            else:
               raise Exception("{0} does not exist".format(dir_path))

    def rename_subdir(self, drive, suffix="_new"):
        """Rename the nested dir by add suffix"""
        for sub_dir in self.SubDirs:
            dir_path=os.path.join(drive, sub_dir)
            new_dir_path = dir_path + suffix
            if os.path.isdir(dir_path):
                print("Rename {0} -> {1}".format(dir_path, new_dir_path))
                os.rename(dir_path, new_dir_path)
                self.NewSubDirs.append(sub_dir + suffix)
            else:
               raise Exception("{0} does not exist".format(dir_path))


    def create_filenames(self, parent_dir, f_type, f_num, *threaded):
        """
        create file_names with .type extension.
        arg *threaded is for creating names with timestamps if use multiple threads
        """
        for i in range(f_num):
            if threaded:
               name = "file" + "-" + str(threaded[0]) + "-"
            else:
               name = "file" + "-"
            file_name = name + str(i) + f_type
            tmp_path = os.path.join(parent_dir, file_name)
            self.Files.append(tmp_path)

            # if there is a dir rename need to save in this list FilesAfterDirRename
            for new_dir in self.NewDirs:
                tmp_path = os.path.join(new_dir, file_name)
                self.FilesAfterDirRename.append(tmp_path)
            # if Subdir exists
            for sub_dir in self.SubDirs:
                tmp_path = os.path.join(sub_dir, file_name)
                self.FilesInSubDir.append(tmp_path)
            # if NestedDir exists
            for nested_dir in self.NestedDirs:
                tmp_path = os.path.join(nested_dir, file_name)
                self.FilesInNestedDir.append(tmp_path)
            # if NewNestedDir exists
            for new_nested_dir in self.NewNestedDirs:
                tmp_path = os.path.join(new_nested_dir, file_name)
                self.FilesInNewNestedDir.append(tmp_path)

    def create_files(self, drive, f_size, *threaded):
        """Create files"""
        for file in self.Files:
            try:
               if threaded:
                  if str(threaded[0]) in file:
                     file_path=os.path.join(drive, file)
                     fl = open(file_path,'w')
                     rand_bytes = self.random_bytes(f_size)
                     fl.write(str(rand_bytes))
                     fl.close()
                     md5checksum = self.md5(file_path)
                     self.Md5Csum [file_path] = md5checksum
               else:
                  file_path=os.path.join(drive, file)
                  fl = open(file_path,'w')
                  rand_bytes = self.random_bytes(f_size)
                  fl.write(str(rand_bytes))
                  fl.close()
                  md5checksum = self.md5(file_path)
                  self.Md5Csum [file_path] = md5checksum
                  print " Filename is " + file_path + " and md5_checksum is " + md5checksum
            except Exception as e:
                 print "Error creating file " +str(e)
                 print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                 sys.exit(0)
        for file in self.FilesAfterDirRename:
            try:
                 file_path=os.path.join(drive, file)
                 fl = open(file_path,'w')
                 rand_bytes = self.randomBytes(bytes)
                 fl.write(str(rand_bytes))
                 fl.close()
                 md5checksum = self.md5(file_path)
                 self.Md5Csum [file_path] = md5checksum
                 print " Filename is " + file_path + " and md5_checksum is " + md5checksum
            except Exception as e:
                 print "Error creating file " +str(e)
                 print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                 sys.exit(0)

    def create_large_size_file_names(self,drive,dir,type,number_files):
        for i in range(number_files):
            new_dir_full_path=os.path.join(drive, dir)
            name = "file" + "-"
            file_name=name+str(i)+type
            file_path=os.path.join(new_dir_full_path, file_name)
            # save the file_path without the drive label
            #tmp_path =   file_path[3:]
            tmp_path = dir + "/" + file_name
            self.Files.append(tmp_path)
		#if there is a dir rename need to save in this list FilesAfterDirRename
            for dir in self.NewDirs:
                new_dir_full_path=os.path.join(drive, dir)
                name = "file" + "-"
                file_name=name+str(i)+type
                file_path=os.path.join(new_dir_full_path, file_name)
                # save the file_path without the drive label
                tmp_path1 =   file_path[3:]
                self.FilesAfterDirRename.append(tmp_path1)


    def modify_files(self,drive,file,bytes):
           #if there is a dir rename need to save in this list FilesAfterDirRename
           if self.NewDirs:
               for dir in self.NewDirs:
               #taking out file_name, it would just return base file_name
                  file_name =	 os.path.basename(file)
                  file_path=os.path.join(dir, file_name)
                  file_full_path=os.path.join(drive,file_path)
                  # save the file_path without the drive label
                  #tmp_path1 =   file_full_path[3:]
                  tmp_path1 = file_path
                  #print "Deb77" +tmp_path1
           elif self.NewNestedDirs:
               for dir in self.NewNestedDirs:
               #taking out file_name, it would just return base file_name
                  file_name =	 os.path.basename(file)
                  file_path=os.path.join(dir, file_name)
                  file_full_path=os.path.join(drive,file_path)
                  # save the file_path without the drive label
                  #tmp_path1 =   file_full_path[3:]
                  tmp_path1 = file_path
                  #print "Deb77" +tmp_path1
           else:
               file_full_path=os.path.join(drive, file)
           try:
               fl = open(file_full_path,'w')
               rand_bytes = self.randomBytes(bytes)
               fl.write(str(rand_bytes))
               fl.close()
           except Exception as e:
               print "Error writing to file {}".format(file)
               print str(e)
               print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
               sys.exit(0)

    def add_attributes(self,drive,dir):
        try:
           dir_path=os.path.join(drive,dir)
           os.system("attrib +a " +dir_path)
           os.system("attrib +r " +dir_path)
           os.system("attrib +h " +dir_path)
           #os.system("attrib +s " +file_full_path)
        except Exception as e:
           print "Error setting attribute to dir {}".format(dir_path)
           print str(e)
           print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
           sys.exit(0)

    def remove_attributes(self,drive,dir):
        try:
           dir_path=os.path.join(drive, dir)
           os.system("attrib -a " +dir_path)
           os.system("attrib -r " +dir_path)
           os.system("attrib -h " +dir_path)
           #os.system("attrib -s " +file_full_path)
        except Exception as e:
           print "Error removing attribute to dir {}".format(dir_path)
           print str(e)
           print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
           sys.exit(0)

    def add_acls(self,drive,dir):
        try:
           dir_path=os.path.join(drive,dir)
           #os.system("icacls " + dir_path + " /grant Everyone:f")
           os.system("icacls " + dir_path + " /grant user63:(OI)(CI)F")
        except Exception as e:
           print "Error setting acls to dir {}".format(dir_path)
           print str(e)
           print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
           sys.exit(0)

    def remove_acls(self,drive,dir):
        try:
           dir_path=os.path.join(drive,dir)
           #os.system("icacls " + dir_path + " /remove Everyone:g")
           os.system("icacls " + dir_path + " /remove user63:g")
        except Exception as e:
           print "Error setting acls to dir {}".format(dir_path)
           print str(e)
           print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
           sys.exit(0)

    def __del__(self):
        self.TopLevelDir = " "


class UnitTestCase(unittest.TestCase):
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
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
