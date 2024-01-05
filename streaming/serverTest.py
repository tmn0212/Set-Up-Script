from pyftdi.gpio import GpioAsyncController
from enum import IntEnum
import socket
from threading import Thread
from time import sleep, time

left = GpioAsyncController()
right = GpioAsyncController()
ssd7 = GpioAsyncController()
ssd6 = GpioAsyncController()
leftn = 8 * 0
rightn = 8 * 3
ssd7n = 8 * 2
ssd6n = 8 * 1
left.open_from_url('ftdi://ftdi:4232:/3', direction=0xFF)
right.open_from_url('ftdi://ftdi:4232:/4', direction=0xFF)
ssd7.open_from_url('ftdi://ftdi:4232:/1', direction=0xFF)
ssd6.open_from_url('ftdi://ftdi:4232:/2', direction=0xFF)
GPIO_InputMaskInt = 0xFFFFFFFF
GPIO_OutputMaskInt = 0x00000000


HOST = '0.0.0.0'
PORT = 9571

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

class Packet_ID(IntEnum):
    DATA = 0x00
    INDIR = 0x01
    OUTDIR = 0x02
    CFGACK = 0x03
    CFGERROR = 0x04

    DISC = 0x7F

    INVALID = 0xFF

def send(conn: socket.socket, pid: Packet_ID, message: int = None) -> bool:
    pid_byte = pid.to_bytes(1, 'big')
    message_word = 0xFFFFFFFF.to_bytes(4, 'big')
    if pid == Packet_ID.DATA:
        if message is None:
            return False
        message_word = message.to_bytes(4, 'big')
    elif pid == Packet_ID.INDIR:
        if message is None:
            return False
        message_word = message.to_bytes(4, 'big')
    elif pid == Packet_ID.OUTDIR:
        if message is None:
            return False
        message_word = message.to_bytes(4, 'big')
    elif pid == Packet_ID.CFGACK:
        message_word = 0x00000000.to_bytes(4, 'big')
    elif pid == Packet_ID.CFGERROR:
        message_word = 0xFFFFFFFF.to_bytes(4, 'big')
    elif pid == Packet_ID.DISC:
        message_word = 0x00000000.to_bytes(4, 'big')
    else:
        return False

    print(f'SEND time()={time()} pid={pid} message={message}')
    conn.send(pid_byte + message_word)
    return True

def recv(conn: socket.socket) -> tuple:
    packet = conn.recv(5)
    if len(packet) != 5:
        return (Packet_ID.INVALID, 0xFFFFFFFF)
    pid = Packet_ID(packet[0])
    message = int.from_bytes(packet[1:], 'big')
    print(f'RECV time()={time()} pid={pid} message={message}')
    return (pid, message)

def receivePortDir(conn: socket.socket) -> bool:
    global GPIO_InputMaskInt, GPIO_OutputMaskInt
    pid1, message1 = recv(conn)
    if pid1 != Packet_ID.INDIR:
        send(conn, Packet_ID.CFGERROR)
        return False
    send(conn, Packet_ID.CFGACK)
    pid2, message2 = recv(conn)
    if pid2 != Packet_ID.OUTDIR:
        send(conn, Packet_ID.CFGERROR)
        return False
    if message1 & message2 != 0:
        send(conn, Packet_ID.CFGERROR)
        return False
    GPIO_OutputMaskInt = message1
    GPIO_InputMaskInt = message2
    left.set_direction(0xFF, (GPIO_OutputMaskInt >> leftn) & 0xFF)
    right.set_direction(0xFF, (GPIO_OutputMaskInt >> rightn) & 0xFF)
    ssd7.set_direction(0xFF, (GPIO_OutputMaskInt >> ssd7n) & 0xFF)
    ssd6.set_direction(0xFF, (GPIO_OutputMaskInt >> ssd6n) & 0xFF)
    send(conn, Packet_ID.CFGACK)
    return True

def send_loop(conn: socket.socket, addr) -> None:
    sleep(1e-3)
    data = ((left.read(peek=True) << leftn) + (right.read(peek=True) << rightn) + (ssd7.read(peek=True) << ssd7n) + (ssd6.read(peek=True) << ssd6n)) & GPIO_InputMaskInt
    lastData = data
    lastPacketSentTime = time()
    while True:
        if not recv_thread.is_alive():
            break

        try:
            data = ((left.read(peek=True) << leftn) + (right.read(peek=True) << rightn) + (ssd7.read(peek=True) << ssd7n) + (ssd6.read(peek=True) << ssd6n)) & GPIO_InputMaskInt
            if data != lastData or time() - lastPacketSentTime > 10:
                send(conn, Packet_ID.DATA, data)
                lastData = data
                lastPacketSentTime = time()
        except TimeoutError:
            print(f'[Timeout] {addr[0]} timed out')
            send(conn, Packet_ID.DISC)
            break

def recv_loop(conn: socket.socket, addr) -> None:
    sleep(1e-3)
    while True:
        if not send_thread.is_alive():
            break

        try:
            pid, message = recv(conn)
            if pid == Packet_ID.DATA:
                left.write(((message & GPIO_OutputMaskInt) >> leftn) & 0xFF)
                right.write(((message & GPIO_OutputMaskInt) >> rightn) & 0xFF)
                ssd7.write(((message & GPIO_OutputMaskInt) >> ssd7n) & 0xFF)
                ssd6.write(((message & GPIO_OutputMaskInt) >> ssd6n) & 0xFF)
            if pid == Packet_ID.DISC:
                break
        except TimeoutError:
            print(f'[Timeout] {addr[0]} timed out')
            send(conn, Packet_ID.DISC)
            break


print('[Starting] Starting server')
server.listen()
socket.setdefaulttimeout(60)
print(f'[Listening] Listening on {HOST}')
while True:
    conn, addr = server.accept()
    print(f'[Connected] Connected to {addr[0]}')
    if not receivePortDir(conn):
        print(f'[Port Error] Bad port configuration received from {addr[0]}')
    else:
        send_thread = Thread(target=send_loop, args=(conn, addr))
        recv_thread = Thread(target=recv_loop, args=(conn, addr))
        for t in (send_thread, recv_thread):
            t.start()
        print('Threads started')
        for t in (send_thread, recv_thread):
            t.join()
        print('Threads ended')
    conn.close()
    print(f'[Disconnected] Disconnected from {addr[0]}')
    conn = addr = None
