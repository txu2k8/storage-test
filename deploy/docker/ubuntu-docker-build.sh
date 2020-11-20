#!/bin/bash

# Ensure Docker on system
rm -rf storage-test
git clone https://github.com/txu2k8/storage-test.git
cd storage-test || exit
rm -rf .git
wget https://sourceforge.net/projects/filebench/files/1.5-alpha3/filebench-1.5-alpha3.tar.gz
cd ../
tar -zcvf storage-test.tar storage-test


cat > Dockerfile << EOF
FROM ubuntu:20.04
MAINTAINER tao.xu <tao.xu2008@outlook.com>
ADD storage-test.tar /

WORKDIR /storage-test
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y apt-utils apt-file git-core
RUN apt-file update
RUN apt-get install -y python3-pip fio attr
RUN pip3 install -r requirements.txt
RUN apt-get install -y flex bison
RUN tar -zxvf filebench-1.5-alpha3.tar.gz -C ./
RUN cd filebench-1.5-alpha3; ./configure; make; make install

#ENTRYPOINT ["python3"]
#CMD ["storage_test.py", "mnt stress -d /mnt -h"]
EOF

docker build -t storage-test:`date "+%Y-%m-%d-%H-%M-%S"` .

# docker tag storage-test registry/storage-test:v1
# docker push registry/storage-test:v1
# docker run -it storage-test

# clean up
rm -rf Dockerfile
rm -rf storage-test
