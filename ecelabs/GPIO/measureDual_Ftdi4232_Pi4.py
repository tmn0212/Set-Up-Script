from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioAsyncController
import threading
#import cv2
#import time
#import asyncio

def getBinList(d): # int to binary list 8bits 
    d0=list('{0:08b}'.format(d))
    d1=[int(x) for x in d0]
    return d1[::-1]

class Dual_Ftdi4232: #  quad-chanels 32 gpio pins + dual channel 16 + single changel 8 =56 
    def __init__(self):
        Ftdi.show_devices() # print list of devices
        #devices = Ftdi.list_devices()
        #try:
        #        sn1 = devices[0][0][4]
        #        sn2 = devices[1][0][4]
        #except:
        #        print('Could not obtain serial number for device')
        self.dev0='1:3'
        #self.dev0='FT55LYXI'
        #self.dev1='FT55UB9R'
        self.gpio0=GpioAsyncController() # SS0
        self.gpio1=GpioAsyncController() # SS1
        self.gpio2=GpioAsyncController() # SS2
        self.gpio3=GpioAsyncController() # SS3
        #self.gpio4=GpioAsyncController() # SS4
        #self.gpio5=GpioAsyncController() # SS5
        #self.gpio6=GpioAsyncController() # SS6
        #self.gpio7=GpioAsyncController() # SS7

       	self.gpio0.configure('ftdi://ftdi:4232:'+self.dev0+'/1',direction=0x00) # 8 inputs 
        self.gpio1.configure('ftdi://ftdi:4232:'+self.dev0+'/2',direction=0x00) # 8 inputs 
        self.gpio2.configure('ftdi://ftdi:4232:'+self.dev0+'/3',direction=0x00) # 8 inputs 
        self.gpio3.configure('ftdi://ftdi:4232:'+self.dev0+'/4',direction=0x00) # 8 inputs

        #self.gpio4.configure('ftdi://ftdi:4232:'+self.dev1+'/1',direction=0x00) # 8 inputs
        #self.gpio5.configure('ftdi://ftdi:4232:'+self.dev1+'/2',direction=0x00) # 8 inputs
        #self.gpio6.configure('ftdi://ftdi:4232:'+self.dev1+'/3',direction=0x00) # 8 inputs
        #self.gpio7.configure('ftdi://ftdi:4232:'+self.dev1+'/4',direction=0x00) # 8 inputs


        self.leds=['0']*32; #8*8

        #self.leds=[self.leds0,self.leds1,self.leds2,self.leds3]
  
   
    def __del__(self):

        self.gpio0.close()
        self.gpio1.close()
        self.gpio2.close()
        self.gpio3.close()
        #self.gpio4.close()
        #self.gpio5.close()
        #self.gpio6.close()
        #self.gpio7.close()


    def detect_leds(self):
        try:
            data0=self.gpio0.read()
            data1=self.gpio1.read()
            data2=self.gpio2.read()
            data3=self.gpio3.read()
            #data4=self.gpio4.read()
            #data5=self.gpio5.read()
            #data6=self.gpio6.read()
            #data7=self.gpio7.read()
        except:
            data0=0
            data1=0
            data2=0
            data3=0
            #data4=0
            #data5=0
            #data6=0
            #data7=0

        self.SS0=list('{0:b}'.format(data0).zfill(8)[::-1])
        self.SS1=list('{0:b}'.format(data1).zfill(8)[::-1])
        self.SS2=list('{0:b}'.format(data2).zfill(8)[::-1])
        self.SS3=list('{0:b}'.format(data3).zfill(8)[::-1])
        #self.SS4=list('{0:b}'.format(data4).zfill(8)[::-1])
        #self.SS5=list('{0:b}'.format(data5).zfill(8)[::-1])
        #self.SS6=list('{0:b}'.format(data6).zfill(8)[::-1])
        #self.SS7=list('{0:b}'.format(data7).zfill(8)[::-1])

        self.leds=self.SS0+self.SS1+self.SS2+self.SS3 #+self.SS4+self.SS5+self.SS6+self.SS7
        print('leds=',self.leds)
        #print('SS0=',self.SS0)
        #print('SS1=',self.SS1)
        #print('SS2=',self.SS2)
        #print('SS3=',self.SS3)
        #print('SS4=',self.SS4)
        #print('SS5=',self.SS5)
        #print('SS6=',self.SS6)
        #print('SS7=',self.SS7)
	#print('gpio0=',gpio0)
        #print('gpio1=',gpio1)
        #print('gpio2=',gpio2)
        #print('gpio3=',gpio3)
        #self.leds0=gpio0[0:7]+gpio3[0:3]+gpio0[7:8]
        #self.leds1=gpio1[0:7]+gpio3[4:7]+gpio1[7:8]
        #self.leds2=gpio2[0:7]+gpio1[7]+gpio2[7]+gpio3[7]
        #self.leds=[self.leds0,self.leds1,self.leds2]

   

    def detect_leds_continous(self):
        self.detect_leds()
        t=threading.Timer(5e-3,self.detect_leds_continous) # 0.5e-3
        t.start()
        #while (cv2.waitKey(1 )&0xFF):# 20ms
        #while True:
        #    self.detect_leds()
        
        #    asyncio.sleep(1.0e-3) # every 1ms
        
            #print('leds=',self.LEDS)
            #print('daq: len of leds=48?',len(self.LEDS))
    
 
    def read_port(self,portNumber):
        if portNumber==0:
            data8=self.gpio0.read()
        elif portNumber==1:
            data8=self.gpio1.read()
        elif portNumber==2:
            data8=self.gpio2.read()
        elif portNumber==3:
            data8=self.gpio3.read()
        elif portNumber==4:
            data8=self.gpio4.read()
        elif portNumber==5:
            data8=self.gpio5.read()
        elif portNumber==6:
            data8=self.gpio6.read()
        elif portNumber==7:
            data8=self.gpio7.read()
        return data8

    def writeKEY_CLICK(self,keyNumber):#btn 4-0
        self.writeKEY1(keyNumber,0)
        self.writeKEY1(keyNumber,1)
        self.writeKEY1(keyNumber,0)
    
    def writeKEY1(self,keyNumber,data1): # single button
        d=self.read_port(2) # read
        d[keyNumber]=data1 # modify
        self.write_port(2,d) # write-back

   
    def writeSW1(self,swNumber,data):# single swtich
        if swNumber<8: # port1
            d=self.read_port(0)
            d[swNumber]=data
            self.write_port(0,d)
        else:
            d=self.read_port(1)
            d[swNumber-8]=data
            self.write_port(1,d)
    


    def write_portStr(self,portNo,dataStr):# '0/1x'*8
        #print('port number=',portNo)
        #print('port str=',dataStr)
        if dataStr!='x'*8: # do nothong if all 'x'
            d=list(dataStr)
            settingMask=int(''.join([str(int(x=='1')) for x in d]),2)
            resettingMask=~int(''.join([str(int(x=='0')) for x in d]),2)
            data0=self.read_port(portNo) # get exsiting data. should be faster than read_port
        #print('data0=',data0)
        #print('settingMask=',settingMask)
        #print('resettingMask=',resettingMask)
            data1=(data0 | settingMask ) & ( resettingMask )
            self.write_port(portNo,data1)
            

    def writeSW0_15(self,dataStr): #MSB for SW0
        dataStr0=dataStr[0:8][::-1]
        dataStr1=dataStr[8:16][::-1]
        self.write_portStr(0,dataStr0)
        self.write_portStr(1,dataStr1)

    def writeSW15_0(self,dataStr):#MSB for SW15
       dataStr=dataStr[::-1]
       self.writeSW0_15(dataStr)

    def writeKEY4_0(self,dataStr):#MSB for KEY4
        dataStr='x'*3+dataStr
        self.write_portStr(2,dataStr)

    def writeKEY0_4(self,dataStr):#MSB for KEY0
        dataStr=dataStr[::-1]
        self.writeKEY4_0(dataStr)

    def writeSW0_15KEY0_4(self,dataStr):
        swStr=dataStr[0:16]
        keyStr=dataStr[16:21]
        self.writeSW0_15(swStr)
        self.writeKEY0_4(keyStr)

    def writeSW15_0KEY4_0(self,dataStr):
        swStr=dataStr[0:16]
        keyStr=dataStr[16:21]
        self.writeSW15_0(swStr)
       	self.writeKEY4_0(keyStr)

    def writeSwitches(self,switches='x'*24):# LSB first
        if ('0' in switches  or '1' in switches): # otherwise do nothing
            l=len(switches)
        
            if l<24:
                switches=switches+'x'*(24-l) # make up 56 bits
            #print('write switches: switches=',switches)
            dataStr0=switches[0:8][::-1] # SW7_0
            dataStr1=switches[8:16][::-1] # SW15_8
            dataStr2=switches[16:24][::-1] # 
            #dataStr3=switches[24:32][::-1]
            #dataStr4=switches[32:40][::-1] # 
            #dataStr5=switches[40:48][::-1]
            #dataStr6=switches[48:56][::-1]
            #dataStr2[4:8]=~dataStr2[4:8] # pressed (1) to write ground(0)
            self.write_portStr(0,dataStr0)
            self.write_portStr(1,dataStr1)
            self.write_portStr(2,dataStr2)
            #self.write_portStr(3,dataStr3)
            #self.write_portStr(4,dataStr4)
            #self.write_portStr(5,dataStr5)
            #self.write_portStr(6,dataStr6)

    def writeBoardSwitches(self,boardNumber=0,switches='x'*32):# 1 out of 4 boards
        #print('inside daq writeBoardSWitches,boardNumber,swtiches=',boardNumber,switches)

        if ('0' in switches or '1' in switches): # otherwise do nothing
            l=len(switches)
            if l<16:
                switches=switches+'x'*(16-l)
            else:
                switches=switches[0:16] # remove extras
            dataStr0=switches[0:8][::-1]
            dataStr1=switches[8:16][::-1]
            #print('data str0=', dataStr0)
            #print('data str1=', dataStr1)
            if ('0' in dataStr0 or '1' in dataStr0):
            	self.write_portStr(boardNumber*2,dataStr0)
            if ('0' in dataStr1 or '1' in dataStr1):
                
                if boardNumber<=2:
                    self.write_portStr(boardNumber*2+1, dataStr1)
                else:# last board
                    dataStr1=dataStr1[::-1]
                    print('port1 2 bits!=xx',dataStr1[0:2]);
                    self.write_portStr(1,dataStr1[0:2][::-1]+'x'*6)
                    self.write_portStr(3,dataStr1[2:4][::-1]+'x'*6)
                    self.write_portStr(5,dataStr1[4:6][::-1]+'x'*6)
