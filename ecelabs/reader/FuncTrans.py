from readwriteIO import *
from setupIO import *
import readwriteIO

# Edit By Minh on 1/3/2024: Change the code to match new FPGA PCB
"""
    These functions are meant to replicate the current SW setup using gpiozero and pigpio library.
    They are aimed to make implementation onto the current setup easier.
    However, they haven't been fully tested (about 80% done) and verified the design. 
"""

# Function to replace LED(#).on() of Pi Zero (gpiozero)
class LED:
    def __init__(self, index):
        self.index = index

    def on(self):
        if 0 <= self.index <= 20:
            pin = self.index

            if 0 <= pin <= 7:
                pin = 7 - self.index
                mcp_addr = 0x21
                port_addr = 0x13
                
            
            elif 8 <= pin <= 13:
                pin = 13 - self.index
                mcp_addr = 0x20
                port_addr = 0x12
                
            elif 14 <= pin <= 20:
                pin = 21 - self.index
                mcp_addr = 0x20
                port_addr = 0x13

        readwriteIO.write_bit(mcp_addr, port_addr, pin, bit=1)

    def off(self):
        if 0 <= self.index <= 20:
            pin = self.index

            if 0 <= pin <= 7:
                pin = 7 - self.index
                mcp_addr = 0x21
                port_addr = 0x13
            
            elif 8 <= pin <= 13:
                pin = 13 - self.index
                mcp_addr = 0x20
                port_addr = 0x12
                
            elif 14 <= pin <= 20:
                pin = 21 - self.index
                mcp_addr = 0x20
                port_addr = 0x13

        readwriteIO.write_bit(mcp_addr, port_addr, pin, bit=0)


# Function to replace Pi4B (pigpio)
class pi:
    def read_bank_1(self):
        # Swapping HWCLK with the correct RIGHT[2]
        mcp_x20_GPB0 = read_port_pin(0x20, portB, 0) # Read the "correct" RIGHT[2]
        mcp_x26_portB = read_port(mcp_addr=0x26, port_addr=0x13)
        mcp_x26_portB = (mcp_x26_portB & 0b11011111) | (mcp_x20_GPB0 << 5)
        
        right_pins = format(mcp_x26_portB, '08b')[::-1]
        left_pins = format(read_port(mcp_addr=0x25, port_addr=0x12), '08b')[::-1]
        LED_pins = format(read_port(mcp_addr=0x26, port_addr=0x12), '03b')[::-1]

        return int("".join([LED_pins, left_pins, right_pins]), 2)
    
    def stop(self):
        return