#!/bin/sh


for i in {1..4}
do
	echo $i
done


HOSTNAME=$(hostname | awk {'print $1'})

mkdir -p /mnt/1/"${HOSTNAME}"1
mkdir -p /mnt/2/"${HOSTNAME}"2
mkdir -p /mnt/3/"${HOSTNAME}"3
mkdir -p /mnt/4/"${HOSTNAME}"4

./fsstress -l 0 -d /mnt/1/"${HOSTNAME}"1 -n 1000 -p 50 -r > 1.log 2>&1 &
./fsstress -l 0 -d /mnt/2/"${HOSTNAME}"2 -n 1000 -p 50 -r > 2.log 2>&1 &
./fsstress -l 0 -d /mnt/3/"${HOSTNAME}"3 -n 1000 -p 50 -r > 3.log 2>&1 &
./fsstress -l 0 -d /mnt/4/"${HOSTNAME}"4 -n 1000 -p 50 -r > 4.log 2>&1 &
