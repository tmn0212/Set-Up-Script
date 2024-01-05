import socket
import threading
#from keyboard import is_pressed
from time import sleep
from pyftdi.gpio import GpioAsyncController
import json

gpio = GpioAsyncController()
url = 'ftdi://ftdi:4232:1:4/1'
GPIO_DIRECTION = 0xF0 # write to FPGA GPIO7-4  upon receiving from client GPIO7-4,
GPIO_InputMask=0x0F
GPIO_OutputMask=0xF0 # Global variables to be overwritten

print('default gpio port direction=', GPIO_DIRECTION)
#read from FPGA GPIO3_0, send to client GPIO3_0
gpio.open_from_url(url, direction=GPIO_DIRECTION)

HOST = '0.0.0.0'
PORT = 9571


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse the port
server.bind((HOST, PORT))

def receivePortDir(conn):
    global GPIO_InputMask,GPIO_OutputMask
    try:
        message_length = conn.recv(1024).decode('utf-8')
        if(message_length):
            message_length = int(message_length)
            try:
                message = conn.recv(message_length).decode('utf-8')
                if '_dir_' in message:
                    print('port direction message=',message)
                    gpio_dir_redefined=int(json.loads(message)['_dir_'])
                    GPIO_InputMask=int(json.loads(message)['_in_'])
                    GPIO_OutputMask=int(json.loads(message)['_out_'])
                    print('redefined port_dir=',gpio_dir_redefined)
                    print('new input mask=',GPIO_InputMask)
                    print('new output mask=',GPIO_OutputMask)
                    gpio.set_direction(0xFF, gpio_dir_redefined) # reset all port directions
                    print("updated gpio directon (0=input, 1=output)=",gpio.direction)
                    return gpio.direction
            except:
                print('not receiving port direction msg')
                return GPIO_DIRECTION
    except:
        print('not receiving dir len')
        return GPIO_DIRECTION

def handle_client(conn: socket.socket, addr) -> None:



    def send(conn: socket.socket,message: str) -> None:
        message = message.encode('utf-8')
        message_length = len(message)
        send_length = str(message_length).encode('utf-8')
        send_length += b' ' * (1024 - len(send_length))
        print('send msg=',message)
        print('send_length=',send_length)
        conn.send(send_length)
        conn.send(message)


    def send_loop(conn: socket.socket, addr) -> None:
        sleep(20e-3)
        # Send data to ECELabs
        read_data_output = gpio.read(peek=True) & ~gpio.direction#GPIO_DIRECTION
        messageOld = bin(read_data_output)[2::].zfill(8)
        while True:
            if not recv_thread.is_alive():
                print("receive thread is not alive, getting out of send")
                #conn.send('Disconnect!')
                break

            try:
                # Read FPGA
                #print('inside read from fpga')
                read_data_output = gpio.read(peek=True) & GPIO_InputMask #~gpio.direction#GPIO_DIRECTION
                message = bin(read_data_output)[2::].zfill(8)

                # Send
                if (not message==messageOld):# send new data only
                    send(conn, message)
                    messageOld=message
                # message = message.encode('utf-8')
                # message_length = len(message)
                # send_length = str(message_length).encode('utf-8')
                # send_length += b' ' * (1024 - len(send_length))
                # print('send message=',message)
                # print('send message length=',send_length)
                # conn.send(send_length)
                # conn.send(message)
            except TimeoutError:
                print('sender timeout')
            sleep(30e-3)

    def recv_loop(conn: socket.socket, addr) -> None:
        sleep(20e-3)
        print('inside receive loop gpio direction=',gpio.direction)
        print('GPIO OUTPUT Mask=',GPIO_OutputMask)
        print('before while loop inside receive loop, GPIO Input mask=',GPIO_InputMask)
        while True:
            # if(is_pressed('x')):
            #     exit()
            
            if not send_thread.is_alive():
                print("send thread is not alive, getting out of receive")
                conn.send('Disconnect!')
                break

            try:
                # Read data
                # print('receving from client')
                try:
                    message_length = conn.recv(1024).decode('utf-8')
                except:
                    pass # print('not receiving data len')
                if(message_length):
                    message_length = int(message_length)
                    try:
                        message = conn.recv(message_length).decode('utf-8')
                        print('received message=',message)
                        print('received message length=',message_length)
                        if message=='Disconnect!':
                            break
                        print('inside receive while loop GPIO output mask=',GPIO_OutputMask)
                        print('data to be write to fpga=',int(message,2)&GPIO_OutputMask)
                        if all((True if x == '1' or x == '0' else False for x in message)):
                            gpio.write(int(message, 2) & GPIO_OutputMask) #gpio.direction) #GPIO_DIRECTION)
                        else:
                            print(f'[Warning] Receiving messages from {addr[0]} out of order, resyncing')
                            conn.recv(1024)

                    except:
                        pass #print('not receiving data msg')
 
                # Write to FPGA
            except:# TimeoutError:
                pass # print('receiver error')
            sleep(30e-3)
        print(f'[Disconnected] Disconnected from {addr[0]}')
    print(f'[Connected] Connected to {addr[0]}')

    print('inside handle client, new gpio direction=',gpio.direction)
    print('GPIO OUTPUT Mask=',GPIO_OutputMask)
    print('before send/receive loop thread, GPIO Input mask=',GPIO_InputMask)

    send_thread = threading.Thread(target=send_loop, args=(conn, addr))
    recv_thread = threading.Thread(target=recv_loop, args=(conn, addr))
    for t in (send_thread, recv_thread):
        t.start()
    for t in (send_thread, recv_thread):
        t.join()
    conn.close()
    print(f'[Disconnected] Disconnected from {addr[0]}')

def connection_accepter_loop() -> None:
    server.listen()
    socket.setdefaulttimeout(1)
    print(f'[Listening] Listening on {HOST}')
    while True:
        conn, addr = server.accept()
        receivePortDir(conn)
        print('inside main loop after receive port dir, new gpio direction=',gpio.direction)
        print('GPIO OUTPUT Mask=',GPIO_OutputMask)
        print('before handle client thread, GPIO Input mask=',GPIO_InputMask)
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        sleep(5.0e-3)
        print(f'[Active Connections] {(threading.active_count() - 1)/3}')
        
print('[Starting] Starting server')
connection_accepter_loop()
