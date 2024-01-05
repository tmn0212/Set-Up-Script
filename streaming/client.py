import socket
from keyboard import is_pressed
from time import sleep
from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioAsyncController

Ftdi.show_devices()
gpio1 = GpioAsyncController()
gpio2 = GpioAsyncController()
gpio3 = GpioAsyncController()
gpio4 = GpioAsyncController()
gpio1.configure('ftdi://ftdi:4232:FT55U2OP/1', direction=0x00)
gpio2.configure('ftdi://ftdi:4232:FT55U2OP/2', direction=0x00)
gpio3.configure('ftdi://ftdi:4232:FT55U2OP/3', direction=0xFF)
gpio4.configure('ftdi://ftdi:4232:FT55U2OP/4', direction=0xFF)

HOST = "10.165.10.35"
PORT = 9571
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send(message):
    message = message.encode('utf-8')
    message_length = len(message)
    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (1024 - len(send_length))
    client.send(send_length)
    client.send(message)
    received_message_length = client.recv(1024).decode('utf-8')
    if(received_message_length):
        received_message_length = int(received_message_length)
        received_message = client.recv(received_message_length).decode('utf-8')
        #received_message = received_message.split()[2].split("-")
        #print(received_message[0] + " " + received_message[1])
        #print(f"[Received] {received_message}")
        gpio4.write(int(received_message, 2))

while True:  
    #numKey = [str(int(is_pressed(str(x)))) for x in range(7, -1, -1)]
    #numKey = ''.join(numKey)
    #print(numKey)

    if(is_pressed('x')):
        send("Disconnect!")
    
    data1 = gpio1.read()
    data1 = bin(data1)[2::].zfill(8)
    data2 = gpio2.read()
    data2 = bin(data2)[2::].zfill(8)
    print(f"[Sent] {data1}")
    send(data1)
    
    sleep(0.1)
send("Disconnect!")