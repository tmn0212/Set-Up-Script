#from gpiozero import LED  # Digital Output
from readwriteIO import *
#from threading import Timer
class ICE40_I2CGPIO_DO:
    def __init__(self): # set up 28 output pins
        #self.usb='210183B0379D' # Basys USB Port ID using Ftdi
        #self.SW=[]
        #for n in range(28):
        #    self.SW.append(LED(n))
        #print(self.pi.set_mode(14,pigpio.INPUT))
        #self.pin_list=tuple(range(28)) #tuple(range(24))+(27,26,25,24)
        #for x in self.pin_list:
        #    self.pi.set_mode(x,pigpio.INPUT) # need set_mode(14,pigpio.INPUT)
        #self.leds=[0]*19 # 8 RIGHT + 8 LEFT + RED,GREEN,BLUE
        self.DO=[0]*20 # data
        FuncTrans.resetIO()
        print('DO=',self.DO)
        #self.RIGHT=self.pin_list[0:8] #  8 right leds
        #self.LEFT=self.pin_list[8:16] #  8 left leds
        #self.RGB=self.pin_list[16:19] # 3 RGB leds
        #self.DIGCOUNT=[0]*4 # digit update count
    def __del__(self):
        pass
        #self.pi.stop()

    #def update_DO(self):
    #    #print('DI=',self.DI)
    #    self.pi.set_bank_1(int("".join(str(x) for x in self.DO[::-1]),2))

    def writeSwitches(self,sw='x'*20):
        print('inside DO, switches=',sw)
        N=len(sw)
        if N>20:
            N=20
        for n in range(N):
            x=sw[n]
            if x=='0':
               FuncTrans.LED(n).off()
               self.DO[n]=x
            elif x=='1':
               FuncTrans.LED(n).on()
               self.DO[n]=x
        #self.update_DO
        #DI0=self.pi.read_bank_1()
        #DI1=DI0
        #DI1=self.pi.read_bank_1()
        #print('DI0=',bin(DI0))
        #print('DI1=',bin(DI1))
      

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

        #for n in range (28):
        #    if n in self.SEG:
        #        self.DI[n]=1-GPIO.input(n) # low active data to on / off
        #    else:
        #        self.DI[n]=GPIO.input(n) # high active

       	self.update_DI()
        self.leds=self.DI
        
        #print('LED=',LED)
        #print('SEG=',SEG)
        #print('DIG=',DIG)
        #self.decode_leds()
        print(self.leds)
        #return self.leds

    def detect_leds_continous(self):
        self.detect_leds()
        #self.decode_leds()
        t=Timer(0.5e-3, self.detect_leds_continous) # every 10ms
        t.start()

