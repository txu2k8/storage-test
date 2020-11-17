### 1. LTP简介
LTP套件是由 Linux Test Project 所开发的一套系统测试套件。
它基于系统资源的利用率统计开发了一个测试的组合,为系统提供足够的压力。
通过压力测试来判断系统的稳定性和可靠性。压力测试是一种破坏性的测试,
即系统在非正常的、超负荷的条件下的运行情况。
用来评估在超越最大负载的情况下系统将如何运行,是系统在正常的情况下对某种负载强度的承受能力的考验 。
### 1. LTP安装步骤
```
1. yum install gcc
2. yum install gcc-c++ libstdc++-devel
3.http://ltp.sourceforge.net/
（1）选择LTP GitHub pages
（2）ltp-full-20180118.tar.bz2
4.tar -jxvf ltp-full-20180118.tar.bz2
5../configure && make && make install
6.不指定安装路径的话,将会默认安装到/opt/ltp目录（在这个目录运行文件就可以了）
```

### 2. LTP稳定性测试
```
2../runltp –f commands(测试常规命令)
3../runltp –f admin_tools(测试常用管理工具是否正常稳定运行)
4../runltp –f dio(测试直接IO是否正常稳定)
5../runltp –f  dma_thread_diotest(测试直接存储器访问线程直接IO是否正常稳定)
6../runltp –f  fcntl-locktests(测试NFS网络文件系统锁是否正常稳定)
7../runltp –f  filecaps(测试filecaps是否正常)
预制条件:在/etc/sysctl.conf文件中加一行：CONFIG_SECURITY_FILE_CAPABILITIES=y后重启电脑
8../runltp –f fs(测试文件系统是否正常)
9../runltp –f  fs_bind(测试fs_bind是否正常)
10../runltp –f fs_ext4(测试fs_ext4是否正常)
11../runltp –f fs_perms_simple(简单测试文件系统权限)
12../runltp –f  fs_readonly(测试文件系统只读)
13../runltp –f fsx(对文件系统进行压力测试)
14../runltp –f hyperthreading(CPU超线程技术测试)
15../runltp –f io(异步IO测试)
16../runltp –f  io_cd(对CD光驱进行压力测试)
预制条件:将光盘放入光驱
-t:指定测试的持续时间
          -t 60s = 60 seconds
          -t 45m = 45 minutes
          -t 24h = 24 hours
          -t 2d  = 2 days
17../runltp –f  io_floppy(对软盘进行压力测试)
预制条件:将软盘放入软驱中
18../runltp –f  lvm.part1(测试文件系统MSDOS、Reiserfs、EXT2、NFS、Ram Disk、MINIX)
19../runltp –f  math(数学库测试)
20../runltp –f  nfs(nfs网络文件系统测试)
预制条件:在本机配置nfs文件系统服务
21../runltp –f  lvm.part2(测试EXT3、JFS文件系统是否正常使用)
预制条件:安装EXT3、JFS文件系统
22../runltp –f pipes(对管道进行压力测试)
23../runltp –f syscalls(测试内核系统调用)
24../runltp –f syscalls-ipc(进程间通信测试)
25../runltp –f can(测试控制器区域网络的稳定性)
26../runltp –f connectors(测试Netlink Connector的功能性及稳定性)
27../runltp –f ipv6(测试IPv6环境下的基本网络功能)
28../runltp –f ipv6_lib(IPv6环境网络开发共享库)
预制条件:内核支持IPv6
29../runltp –f multicast（ 测试多播的稳定性）
预制条件：
（1）设置环境变量export RHOST=<多播目标地址>
（2）/root/.rhosts,/home/user/.rhosts 添加内容：多播目标主机地址，多播目标主机用户，有多少多播目标主机就写多少条。
30. ./runltp –f network_commands （ 测试ftp和ssh的稳定性）
预制条件：开启ftp和ssh
31. ./runltp –f network_stress.whole（ 网络各个功能的压力性测试 ）
预制条件：
（1）部署一台服务器
（2）服务器上运行的服务： ssh DNS http ftp
32. ./runltp –f nptl（ 测试本地POSIX线程库的稳定性 ）
预制条件：内核支持POSIX本地线程库
33../runltp –f nw_under_ns（测试网络命名空间的稳定性）
34../runltp –f power_management_tests（电源管理模块的稳定性）
预制条件：内核版本2.6.31以上
35../runltp –f pty（测试虚拟终端稳定性）
预制条件：内核支持VT console
36../runltp –f quickhit（测试系统调用的稳定性）
37../runltp –f rpc 和 ./runltp –f rpc_test（测试远程过程调用稳定性）
预制条件：内核支持远程过程调用
38../runltp –f scsi_debug.part1（测试SCSI的稳定性）
39../runltp –f sctp（测试SCTP协议的稳定性）
预制条件：内核支持SCTP协议
40../runltp –f tcp_cmds_expect（TCP命令的可用性和稳定性）
预制条件：内核支持TCP/IP协议
41../runltp –f controllers（内核资源管理的稳定性测试）
预制条件：内核版本必须等于或者高于2.6.24
42../runltp –f cap_bounds（POSIX功能绑定设置可用性)
预制条件：内核版本2.6.25以上
43../runltp –f containers（命名空间资源稳定性）
44../runltp –f cpuacct（测试不同cpu acctount控制器的特点）
45../runltp –f cpuhotplug（测试cpu热插拔功能的稳定性）
46../runltp –f crashme（测试crashme）
预制条件：做测试前，先备份系统
47../runltp –f hugetlb（测试 hugetlb）
48../runltp –f ima（测试ima）
49../runltp –f ipc（测试ipc）
50../runltp –f Kernel_misc（测试 Kernel_misc）
51../runltp –f ltp-aiodio.part1（测试 ltp-aiodio.part1）
52../runltp –f Ltp-aiodio.part2（测试 Ltp-aiodio.part2）
53../runltp –f ltp-aiodio.part3（测试 ltp-aiodio.part3）
54../runltp –f ltp-aiodio.part4（测试 ltp-aiodio.part4）
55../runltp –f ltp-aio-stress.part1（测试 io stress）
56../runltp –f ltp-aio-stress.part2（测试 io stress）
57../runltp –f mm（测试mm）
58../runltp –f modules（测试内核模块）
59../runltp –f numa（测试非统一内存访问）
60../runltp –f sched（测试调度压力）
61../runltp –f securebits（测试securebits）
62../runltp –f smack（smack安全模块测试）
63../runltp –f timers（测试posix计时器）
64../runltp –f tirpc_tests（测试Tirpc_tests）
65../runltp –f tpm_tools（测试 tpm_tools）
66../runltp –f tracing（跟踪测试）
```

### 2. LTP初始测试
```
1. # ./runltp -p -l /tmp/resultlog.20180421 -d /tmp/ -o /tmp/ltpscreen.20180421 -t 1h 
或者 ./runalltests.sh
  -p:人为指定日志格式,保证日志为可读格式    
  -l:记录测试日志的文件
  -d:指定临时存储目录,默认为/tmp
  -o:直接打印测试输出到/tmp/ltpscreen.20180421
  -t:指定测试的持续时间
        -t 60s = 60 seconds
        -t 45m = 45 minutes
        -t 24h = 24 hours
        -t 2d  = 2 days
2. # vi resultlog.20180421（进来这里面查看结果）
```
### 3. LTP压力测试
```
1. # cd /opt/ltp/testscripts（进入这个目录）

2. # yum install -y sysstat（执行ltpstress时需要添加”sar”或”top”工具）

3. # ./ltpstress.sh -d /tmp/ltpstress.data -l /tmp/ltpstress.log -I /tmp/ltpstress.iostat  -i 5 -m 128 -t 1 -S

            -d:指定sar或top记录文件,默认/tmp/ltpstress.data
            -l:记录测试结果到/tmp/ltpstress.log
            -I:记录"iostat"结果到iofile,默认是/tmp/ltpstress.iostat
            -i:指定sar或top快照时间间隔,默认为10秒
            -m: 指定最小的内存使用,默认为: RAM + 1/2 swap
            -n:不对网络进行压力测试
            -S :用sar捕捉数据
            -T:利用LTP修改过的top工具捕捉数据
            -t: 指定测试时间，默认为小时
4. 默认情况下，测试结果放在 /tmp
    ltpstress.log ---- 记录相关日志信息，主要是测试是否通过(pass or fail)
    ltpstress.data ---- sar工具记录的日志文件，包括cpu,memory,i/o等
    ltpstress.5010.output1 ---- 对应stress.part1，测试命令的一些输出信息  
    ltpstress.5010.output2 ---- 对应stress.part2，测试命令的一些输出信息
    ltpstress.5010.output3 ---- 对应stress.part3，测试命令的一些输出信息
5. 测试cpu 平均使用率：# sar -u -f ltpstress.data
6. 测试memory 平均使用率：# sar -r -f ltpstress.data
7. # grep FAIL ltpstress.log | sort | uniq >failcase.txt
在ltpstress.log里面检索FAIL关键字，再用sort进行排序，用uniq去除重复项，将信息重定向到failcase.txt中
```
### 3. LTP性能测试