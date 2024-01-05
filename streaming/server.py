import socket
import threading
from time import sleep
from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioAsyncController

gpio1 = GpioAsyncController()
#gpio2 = GpioAsyncController()
#gpio3 = GpioAsyncController()
#gpio4 = GpioAsyncController()
url= 'ftdi://ftdi:4232:1:4' #ftdi:4232:1:4
print('url=',url)
Ftdi.show_devices()
gpio1.configure( url+'/1',direction=0x0F) #0=input, 1=output  #'ftdi://ftdi:4232:FT4PWTIZ/1', direction=0x00)
#gpio2.configure(url+'/2',direction=0xFF) #'ftdi://ftdi:4232:FT4PWTIZ/2', direction=0x00)
#gpio3.configure(url+'/3',direction=0xFF) #'ftdi://ftdi:4232:FT4PWTIZ/3', direction=0xFF)
#gpio4.configure(url+'/4',direction=0xFF) #'ftdi://ftdi:4232:FT4PWTIZ/4', direction=0xFF)

HOST = "0.0.0.0"
#socket.gethostbyname(socket.gethostname())
PORT = 9571

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(conn, addr):
    print(f"[Connected] Connected to {addr[0]}")
    while True:
        message_length = conn.recv(1024).decode('utf-8')
        if(message_length):
            message_length = int(message_length)
            message = conn.recv(message_length).decode('utf-8')
            print('received msg=',message)
            print('received msg len=',message_length)
            #message=message&0x0f # keep only the low 4 bits
            if(message == "Disconnect!"):
                break
            #print(f"Received data from [{addr[0]}] {message}")
            received_data_input=int(message, 2)&0x0f
            read_data_output = gpio1.read() & 0xf0 # keep only high 4 bits
            msg_output = bin(read_data_output)[2::].zfill(8)
            gpio1.write(received_data_input|read_data_output) # low 4 bits
            msg_output = bin(read_data_output>>4)[2::].zfill(8) # shift right 4 bits before sending
            #print(f"[Sent] {msg_output}")
            send(conn, msg_output)
        sleep(1.0) #1ms
    print(f"[Disconnected] {addr[0]}")
    conn.close()

def send(conn, message):
    message = message.encode('utf-8')
    message_length = len(message)
    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (1024 - len(send_length))
    print('send message=',message)
    print('send msg len=',send_length)
    conn.send(send_length)
    conn.send(message)

def start():
    server.listen()
    print(f"[Listening] Listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")
        
print("[Starting] Starting server")
start()
