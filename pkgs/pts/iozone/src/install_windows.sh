#!/bin/sh

wget http://phoronix-test-suite.com/benchmark-files/iozone-windows-1.zip
unzip -o iozone-windows-1.zip

echo "#!/bin/sh
cd iozone-windows
./iozone.exe \$@ > \$LOG_FILE" > ~/iozone
chmod +x ~/iozone