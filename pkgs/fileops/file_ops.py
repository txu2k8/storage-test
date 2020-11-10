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


import os, sys, shutil, time, random
from random import randint
import hashlib
import itertools
import threading
from threading import Thread
from collections import OrderedDict

class FileOps(object):
    """The various file operations"""
    def __init__(self):
        self.Dirs = []  # this will store all directory names after creation
        self.NewDirs = [] # this will store directory names after rename
        self.NestedDirs = [] # this will created nested directory under a TopLevelDir
        self.NewNestedDirs = [] # this will rename the nested dirs
        self.SubDirs = []  # this will create subdirs inside a Dir
        self.NewSubDirs = [] # this will rename subdirs
        self.Files = []  # this will store all files inside a dir provided
        self.NewFiles = [] # this will store all files after renames
        self.FilesAfterDirRename = [] # this will store all files after dir renames
        self.FilesCreatedBeforeDirRename = [] # this will store all files after dir renames
        self.FilesInSubDir = []    # this will store all files in subdir
        self.FilesInNestedDir = [] # this will store all files in nested dir
        self.FilesInNewNestedDir = [] # this will store all files after nested dir rename
        self.Md5Csum = {}  # dict with filename as the key to hold md5 checksum after file creation
        self.cc_drive1 = sys.argv[1]
        self.cc_drive2 = sys.argv[2]
        self.cc_drive3 = sys.argv[3]
        self.TopLevelDir = "Dir_" + time.strftime("%H%M%S")

    # method to create number_dirs dirs and save this in a list
    def create_dir(self,drive,number_dirs):
        for i in range(number_dirs):
            name = "Dir_" + time.strftime("%H%M%S") + "-" #appending timestamp to "Dir_"
            dir_name=name+str(i)
            self.Dirs.append(dir_name)
        for the_dir in self.Dirs:
            dir_full_path=os.path.join(drive, the_dir)
            if os.path.isdir(dir_full_path):
                print("Error: dir_full_path exists")
            else:
               os.mkdir(dir_full_path)

    def create_nested_dirs(self,drive,levels):
        tmp =[[self.TopLevelDir]]    # temp list storing the TopLevel dir
        # tmp =[]    # temp list storing the TopLevel dir
        dir_nested_path=[]
        for i in range(levels):
            tmp.append(["S_"+str(i)])
        for item in itertools.product(*tmp):
             dir_full_path=os.path.join(drive,*item)
             #dir_nested_path=os.path.join(self.TopLevelDir,*item)
             dir_nested_path=os.path.join(*item)
             #print "Deb22" +dir_full_path
             #print "Deb33" +dir_nested_path
             tmp.append(dir_full_path)
             if os.path.isdir(dir_full_path):
                 print("Error: {} exists".format(dir_full_path))
             else:
                os.makedirs(dir_full_path)
                # save the dirpath without the drive label
                #tmp_path =   dir_full_path[3:]
                #tmp_path = dir_nested_path
                #print "Deb10" +tmp_path
         # also keep track of top level Dir
        self.Dirs.append(self.TopLevelDir)
        self.NestedDirs.append(dir_nested_path)

    def create_sub_dirs(self, cc_drive, dir):
        # Subdir will be created inside the dir
        name = "SubDir_" + time.strftime("%H%M%S")
        top_dir_path=os.path.join(cc_drive,dir)
        dir_full_path=os.path.join(top_dir_path,name)
        if os.path.isdir(dir_full_path):
            print("Error: {} exists".format(dir_full_path))
        else:
           os.makedirs(dir_full_path)
           # save the dirpath without the drive label
           # tmp_path =   dir_full_path[3:]
           tmp_path = os.path.join(dir, name)  # changed by tao.xu, txu@panzura.com
           self.SubDirs.append(tmp_path)

    def rename_dir(self,drive):
        # "_new" will be appended to new name
        name = "_new"
        for dir in self.Dirs:
            dir_full_path=os.path.join(drive, dir)
            new_dir_full_path = dir_full_path+name
            if os.path.isdir(dir_full_path):
               #try:
                  os.rename(dir_full_path,new_dir_full_path)
                  print new_dir_full_path
                  # save the dirpath without the drive label
                  tmp_path = dir + name
                  #tmp_path =   new_dir_full_path[3:]
                  self.NewDirs.append(tmp_path)
                  # if the files are already created
                  tmp_file_path=[]
                  for dirname, dirnames, filenames in os.walk(new_dir_full_path):
                      tmp_file_path=filenames
                      print tmp_file_path
                  for file in tmp_file_path:
                      tmp_path = os.path.join(drive,dirname)
                      new_path = os.path.join(tmp_path,file)
                      print new_path
                      self.FilesCreatedBeforeDirRename.append(new_path)
               #except WindowsError:
               #   print "Permission or AccessDenied error reported, expected in rename in a multi CC setup"
            else:
               print "Error: " + dir_full_path + " does not exist"

    def rename_nested_dirs(self,drive):
        # "_new" will be appended to new name
        name = "_new"
        for dir in self.NestedDirs:
            dir_full_path=os.path.join(drive, dir)
            new_dir_full_path = dir_full_path+name
            if os.path.isdir(dir_full_path):
               os.rename(dir_full_path,new_dir_full_path)
               # save the dirpath without the drive label
               tmp_path = dir + name
               #print "Deb66" +tmp_path
               #tmp_path =   new_dir_full_path[3:]
               self.NewNestedDirs.append(tmp_path)
            else:
               print "Error: " + dir_full_path + " does not exist"

    def rename_subdir(self,drive):
        # "_new" will be appended to new name
        name = "_new"
        for dir in self.SubDirs:
            dir_full_path=os.path.join(drive, dir)
            new_dir_full_path = dir_full_path+name
            if os.path.isdir(dir_full_path):
               os.rename(dir_full_path,new_dir_full_path)
               # save the dirpath without the drive label
               tmp_path = dir + name
               #tmp_path =   new_dir_full_path[3:]
               self.NewSubDirs.append(tmp_path)
            else:
               print "Error: " + dir_full_path + " does not exist"

    def list_dir(self,drive, Dirs, number_dirs):
        count = 0
        for dir in Dirs:
            dir_full_path=os.path.join(drive, dir)
            if os.path.isdir(dir_full_path):
               for dirname, dirnames, filenames in os.walk(dir_full_path):
                   print dirname
                   count = count + 1
            else:
               print "Error: " + dir_full_path + " does not exist"
        if count == number_dirs:
           print "PASS: All the directories created exist"
        else:
           print "FAIL: All the directories created dont exist"

    def remove_dir(self,drive,Dirs):
        for dir in Dirs:
            dir_full_path=os.path.join(drive, dir)
            if os.path.isdir(dir_full_path):
               #os.rmdir(dir_full_path)
               shutil.rmtree(dir_full_path, ignore_errors=True)
            else:
               print "Error: " + dir_full_path + " does not exist"

    # returns a byte array of random bytes
    def randomBytes(self,n):
        return bytearray(random.getrandbits(8) for i in range(n))

    # returns the md5 checksum of the opened file
    def md5(self,fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
             for chunk in iter(lambda: f.read(4096), b""):
                 hash_md5.update(chunk)
        return hash_md5.hexdigest()


    # this will create file_names with .type extension. optional argument *threaded is for creating
    # names with timestamps if multiple threads are used to create the files.
    def create_filenames(self,drive,dir,type,number_files,*threaded):
        for i in range(number_files):
            new_dir_full_path=os.path.join(drive, dir)
            if threaded:
               name = "file" + "-" + str(threaded[0]) + "-"
            else:
               name = "file" + "-"
            file_name=name+str(i)+type
            file_path=os.path.join(new_dir_full_path, file_name)
            # save the file_path without the drive label
            #tmp_path =   file_path[3:]
            tmp_path = dir + "/" + file_name
            self.Files.append(tmp_path)
            #print "Deb1 " +tmp_path
            #if there is a dir rename need to save in this list FilesAfterDirRename
            for dir in self.NewDirs:
                new_dir_full_path=os.path.join(drive, dir)
                name = "file" + "-"
                file_name=name+str(i)+type
                file_path=os.path.join(new_dir_full_path, file_name)
                # save the file_path without the drive label
                #tmp_path1 =   file_path[3:]
                tmp_path1 = dir + "/" + file_name
                self.FilesAfterDirRename.append(tmp_path1)
            #if Subdir exists
            for dir in self.SubDirs:
                new_dir_full_path=os.path.join(drive, dir)
                name = "file" + "-"
                file_name=name+str(i)+type
                file_path=os.path.join(new_dir_full_path, file_name)
                # save the file_path without the drive label
                #tmp_path1 =   file_path[3:]
                tmp_path1 = dir + "/" + file_name
                self.FilesInSubDir.append(tmp_path1)
            #if NestedDir exists
            for dir in self.NestedDirs:
                new_dir_full_path=os.path.join(drive, dir)
                name = "file" + "-"
                file_name=name+str(i)+type
                file_path=os.path.join(new_dir_full_path, file_name)
                # save the file_path without the drive label
                #tmp_path1 =   file_path[3:]
                tmp_path1 = dir + "/" + file_name
                self.FilesInNestedDir.append(tmp_path1)
            #if NewNestedDir exists
            for dir in self.NewNestedDirs:
                new_dir_full_path=os.path.join(drive, dir)
                name = "file" + "-"
                file_name=name+str(i)+type
                file_path=os.path.join(new_dir_full_path, file_name)
                # save the file_path without the drive label
                #tmp_path1 =   file_path[3:]
                tmp_path1 = dir + "/" + file_name
                self.FilesInNewNestedDir.append(tmp_path1)

    def create_file_and_calculate_csm(self,drive,bytes,*threaded):
        for file in self.Files:
            try:
               if threaded:
                  if str(threaded[0]) in file:
                     file_full_path=os.path.join(drive, file)
                     fl = open(file_full_path,'w')
                     rand_bytes = self.randomBytes(bytes)
                     fl.write(str(rand_bytes))
                     fl.close()
                     md5checksum = self.md5(file_full_path)
                     self.Md5Csum [file_full_path] = md5checksum
               else:
                  file_full_path=os.path.join(drive, file)
                  fl = open(file_full_path,'w')
                  rand_bytes = self.randomBytes(bytes)
                  fl.write(str(rand_bytes))
                  fl.close()
                  md5checksum = self.md5(file_full_path)
                  self.Md5Csum [file_full_path] = md5checksum
                  print " Filename is " + file_full_path + " and md5_checksum is " + md5checksum
            except Exception as e:
                 print "Error creating file " +str(e)
                 print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                 sys.exit(0)
        for file in self.FilesAfterDirRename:
            try:
                 file_full_path=os.path.join(drive, file)
                 fl = open(file_full_path,'w')
                 rand_bytes = self.randomBytes(bytes)
                 fl.write(str(rand_bytes))
                 fl.close()
                 md5checksum = self.md5(file_full_path)
                 self.Md5Csum [file_full_path] = md5checksum
                 print " Filename is " + file_full_path + " and md5_checksum is " + md5checksum
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

    def create_large_size_file(self,drive,bytes):
        for file in self.Files:
            try:
               file_full_path=os.path.join(drive, file)
               with open(file_full_path, "wb") as out:
                    out.truncate(bytes)
               md5checksum = self.md5(file_full_path)
               self.Md5Csum [file_full_path] = md5checksum
               print " Filename is " + file_full_path + " and md5_checksum is " + md5checksum
            except Exception as e:
               print "Error creating file " +str(e)
               print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
               sys.exit(0)

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

    def rename_files(self,drive,file):
        try:
           file_full_path=os.path.join(drive, file)
           file_name_parts = file.split(".") #split actual filename and extension
           new_full_path=os.path.join(drive, file_name_parts[0]) + "_new." + file_name_parts[1] #constructing the new name
           os.rename(file_full_path,new_full_path)
           # save the file_path without the drive label
           tmp_path =   new_full_path[3:]
           self.NewFiles.append(tmp_path)
        except Exception as e:
           print "Error renaming the file {}".format(file)
           print str(e)
           print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
           sys.exit(0)

    def delete_files(self,drive,file):
        try:
           file_full_path=os.path.join(drive, file)
           os.remove(file_full_path)
        except Exception as e:
           print("Error deleting the file " + file_full_path)
           print(str(e))
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
