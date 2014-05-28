sudo apt-get -y install wget
sudo apt-get -y install libtool autoconf automake uuid-dev build-essential
cd ~
wget http://download.zeromq.org/zeromq-3.2.2.tar.gz
tar zxvf zeromq-3.2.2.tar.gz && cd zeromq-3.2.2
./configure
make && sudo make install
sudo apt-get -y install libzmq-dev python-zmq
cd ../
echo export LIBRARY_PATH=LIBRARY_PATH:/usr/local/lib >> ~/.bashrc
exec bash
