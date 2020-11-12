#!/bin/sh

wget http://archive.debian.org/debian/pool/main/p/postmark/postmark_1.51.orig.tar.gz
tar -zxvf postmark_1.51.orig.tar.gz
cd postmark-1.51/
cc -O3 $CFLAGS postmark-1.51.c -o postmark
echo $? > ~/install-exit-status
cd ~/

echo "#!/bin/sh
cd postmark-1.51/
echo \"set transactions \$1
set size \$2 \$3
set number \$4
show
run
quit\" > benchmark.cfg
./postmark benchmark.cfg > ./postmark.result 2>&1" > postmark
chmod +x postmark