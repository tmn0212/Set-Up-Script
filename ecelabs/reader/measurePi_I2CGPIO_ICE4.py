# import pigpio  # Digital Input
#from threading import Timer
from therading import Thread
from setupIO import *
from readwriteIO import *
#from time import sleep
import smbus
from time import sleep

class ICE40_Pi4_I2CGPIO_DI:
    def __init__(self): # set up 22 output pins
        setIO()
        # #self.usb='210183B0379D' # Basys USB Port ID using Ftdi
        # self.pi=pi()
        # # print(self.pi.set_mode(14,pigpio.INPUT))
        # self.pin_list=tuple(range(28)) #tuple(range(24))+(27,26,25,24)
        # #for x in self.pin_list:
        # #    self.pi.set_mode(x,pigpio.INPUT) # need set_mode(14,pigpio.INPUT)
        # self.leds=[0]*19 # 8 RIGHT + 8 LEFT + RED,GREEN,BLUE
        # self.DI=[0]*19 # data
        # self.RIGHT=self.pin_list[0:8] #  8 right leds
        # self.LEFT=self.pin_list[8:16] #  8 left leds
        # self.RGB=self.pin_list[16:19] # 3 RGB leds
        #self.DIGCOUNT=[0]*4 # digit update count
    def __del__(self):
        pass #self.pi.stop()

    def decode_leds(self):
        print('DI=',self.DI)
        

    def update_DI(self):
        # try:
        DI0=self.pi.read_bank_1()
        # except:
        #     DI0=0 # 32 bits of 0
        DI1=DI0
        #DI1=self.pi.read_bank_1()
        #print('DI0=',bin(DI0))
        #print('DI1=',bin(DI1))
        if DI0==DI1:  # update only if no reliable data read
           DI=[int(x) for x in list(format(DI1,'#032b')[2:])[::-1][0:19]]
            #print('DI=',DI)
           #for n in  range(16, 28):
           #     DI[n]=1-DI[n] # low active data to on /off
        self.DI=DI

        #else:
           #print('unreliable data')
        #print('DI=',self.DI)
        #else:
        #   print('unreliable data')
        #for n in range (28):
        #    if n in self.SEG:
        #        DI[n]=1-GPIO.input(n) # low active data to on / off
        #    else:
        #        self.DI[n]=GPIO.input(n) # high active

    def detect_leds(self):
        D=read_all()
        print('D=',D)
        BLUE=D["BLUE"]
        GREEN=D["GREEN"]
        RED=D["RED"]
        RIGHT=D["RIGHT"][::-1]
        LEFT=D["LEFT"][::-1]
        SS7=D["SS7"][::-1]
        SS6=D["SS6"][::-1]
        SS5=D["SS5"][::-1]
        SS4=D["SS4"][::-1]
        SS3=D["SS3"][::-1]
        SS2=D["SS2"][::-1]
        SS1=D["SS1"][::-1]
        SS0=D["SS0"][::-1]
        self.leds=(RIGHT+LEFT+RED+GREEN+BLUE+SS0+SS1+SS2+SS3+SS4+SS5+SS6+SS7)
        #self.RGB = self.leds[16:19]

        #print('LED=',LED)
        #print('SEG=',SEG)
        #print('DIG=',DIG)
        #self.decode_leds()
        #print(self.leds)
        #return self.leds

    def mytimer(self):
        sleep(1.0e-3)
        self.detec_leds()

    def detect_leds_continous(self):
        #self.detect_leds()
        #t=Timer(1.0e-3, self.detect_leds_continous) # 0.5e-3 every 10ms
        #t.start()
        t=Thread(target=self.myTimer,args=())
        t.start()

