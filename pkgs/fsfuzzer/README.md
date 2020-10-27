https://github.com/sughodke/fsfuzzer

The fsfuzzer is a filesystem fuzzer tool that does stress tests of 
various filesystems in a reproducible and logged way. 
This tool creates initial (valid) filesystem images and then manipulates 
their binary format and structure for detecting flaws/bugs/design problems 
in the parsing/handling code for that particular filesystem. 
The program expects that you have a /media directory. 
It uses that one for mounting test images in.

Introduction/Building
This is a quick start guide to fsfuzz. To get started run:
```shell script
./configure
make
```
You do not need to install the program anywhere, just use it right where you unpack it.

Background
```
I met LMH at the 2006 SE Linux Symposium. He showed me some file system errors that he discovered. After the conference we continued talking. He showed me a simple program that exercised corrupt file system images. I saw that he was on to something and we continued talking. From March 5 - 8 we collaborated on the first version of this program. Tests were improved, filesystem creation was automated, error checking improved. Since then I've added more file systems, made it easier to use, documented it, and improved the exercisor.
```

Usage
```
So, to get started fuzzing file systems, the program expects that you have a /media directory. It uses that one for mounting test images in. It will try to create mount points there, so if you don't have a /media directory, create one.

The main program is ./fsfuzz. If you do not give it arguments, it will cycle through all the file systems and test each one individually. You can also test a specific file system by passing its name on the command line. To see the supported file systems type "./fsfuzz --help". The file systems supported can vary based on the utilities you have installed.

The fsfuzz program uses ./run_test to actually exercise a file system image. When fsfuzz is running, it writes to syslog the command line for ./run_test. This is so that when it finally crashes, you can lookup what the command was and re-test. There should be an image in the ./cfs directory.

So, for example, you had a crash fuzzing iso9660. You might find this in syslog "./run_test iso9660 16" This tells run_test that you are fuzzing is09660 files and the 16th image is what was last run.

A simple program ./run_last will run the last image as long as there is only one image in the cfs directory...which is usually the case. If you find an image that you like and want to keep, move it out of the cfs directory because subsequent runs of ./fsfuzz will erase the files.

WARNING: This program can cause your kernel to oops. ITS WHOLE PURPOSE IS TO PROVOKE THE COMPUTER TO DO BAD THINGS. If you are using a journalling file system for all your important data, for the most part you will be OK running this on your machine. But its impossible to know what hole in the OS you will trigger and what its consequences are. If you don't run with a journalled file system and many processes are active and some writing to disk, there is a real good chance that you could screw up your computer. YOU HAVE BEEN WARNED!

```
Current File Systems
```
cramfs, ext2/3/4, gfs2, iso9660, jffs2, msdos, reiserfs, romfs, squashfs, swap, vfat, xfs, and ecryptfs over other file systems.
```
Extending
If you want to add support for a file system not already covered, this is what you want to do.
```
1. First, look for its filesystem creation program. In a lot of cases, its called mkfs.filesystem-name. Add an optional test for that program and include the filesystem's name in the list.
2. Next, does the filesystem have any minimum size requirements? If so, you may need to make an adjustment to prep_fs function. Look at xfs as an example.
3. After that comes the most important step, you need to create a file system creation scriptlet in the big switch/case block. Filesystems fall into 2 categories. The kind that can be created from a file and the kind that are created from a directory. For the kind that can be created from a file, use xfs as the recipe. For the kind that are created from a directory, use cramfs as a recipe.
4. In order for the tests to find more bugs, the file system should be populated with initial data. This happens naturally if the file system is created from a directory. However, if the file system is created from a file, you will have to add the file system name to a case statement at the bottom of the prep_fs function.
5. In the main loop, you may have to add a modprobe statement to make sure the module is loaded. Look at xfs again for the basic recipe.
```








