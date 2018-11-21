#!/bin/sh

# get dependencies
sudo apt install scons

# get/build ledlib
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python3 setup.py install
cd ../..

# make link to ledlib
ln -s rpi_ws281x/python src/ledlib 

# blacklist sound pwm (this needs perms fix)
sudo echo "blacklist snd_bcm2835" >> /etc/modprobe.d/snd-blacklist.conf

# install lots of crap
sudo apt install python3
cp src/settings.ini.sample src/settings.ini
sudo pip3 install slackclient
sudo pip3 install git+https://github.com/Pithikos/python-websocket-server
sudo pip3 install websocket-server
sudo pip3 install websockets
