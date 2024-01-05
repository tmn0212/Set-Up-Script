from pyftdi import eeprom
from pyftdi.ftdi import Ftdi
Ftdi.show_devices()
eprom=eeprom.FtdiEeprom()
url=input('Enter url to open: ')
eprom.open(url)
sn=input('Enter new SN: ')

eprom.set_serial_number(sn)

eprom.commit(dry_run=False)

Ftdi.show_devices()


