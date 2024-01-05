import socket
from threading import Thread
from keyboard import is_pressed
from time import sleep
from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioAsyncController

Ftdi.show_devices()
gpio1 = GpioAsyncController()
# gpio2 = GpioAsyncController()
# gpio3 = GpioAsyncController()
# gpio4 = GpioAsyncController() 
gpio1.configure('ftdi://ftdi:232h:1/1', direction=0x0F) # 0=input, 1=output
# gpio2.configure('ftdi://ftdi:4232:FT82N6OI/2', direction=0x00)
# gpio3.configure('ftdi://ftdi:4232:FT82N6OI/3', direction=0xFF)
# gpio4.configure('ftdi://ftdi:4232:FT82N6OI/4', direction=0xFF)

HOST = "10.165.10.35"
PORT = 9571
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send(message):
    message = message.encode('utf-8')
    message_length = len(message)
    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (1024 - len(send_length))
    #print('msg=',message)
    #print('send_length=',send_length)
    client.send(send_length)
    client.send(message)
    received_message_length = client.recv(1024).decode('utf-8')
    if(received_message_length):
        received_message_length = int(received_message_length)
        received_message = client.recv(received_message_length).decode('utf-8')
        #print(received_message)
        #received_message = received_message.split()[2].split("-")
        #print(received_message[0] + " " + received_message[1])
        #print(f"[Received] {received_message}")
        gpio1.write(int(received_message, 2)&0x0f) # keep only low 4 bits
        #print(f'client receiving {received_message}')
        #print(f"[Write] {received_message}")


def mytimer():
    while True:
        
        read_send()
        sleep(5.0e-3) #5ms
    

def read_send_continous():
    #self.detect_leds()
    #self.decode_leds()
    #t=Timer(1.0e-3, self.detect_leds_continous) # 0.5e-3 every 10ms
    t=Thread(target=mytimer,args=())
    t.start()

def read_send(): #while True: # 
    if(is_pressed('x')):
        send("Disconnect!")
   
    data1 = gpio1.read()>>4 # shift upper 4 bits 
    #print(f'read data1 {data1}')
    data1 = bin(data1)[2::].zfill(8)
    #print(f'read data1 {data1}')
    # data2 = gpio2.read()
    # data2 = bin(data2)[2::].zfill(8)
    #print(f"client read {data1} from gpio")
    #print(f"[Sent] {data1}")
    send(data1)

t=Thread(target=mytimer,args=())
t.start()
   
#mytimer() #read_send()
#send("Disconnect!")