sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip -y
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
pip3 install cherrypy -y
pip3 install pyftdi -y
sudo apt install fpga-icestorm -y
sudo apt install tmux -y
sudo apt install lsof -y
pip3 install smbus
sftp ice40New.local
sudo cp etc_udev_rules.d/* /etc/udev/rules.d
iceprog -S testICE40.bin
sudo raspi-config nonint do_i2c 0
sudo reboot
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           