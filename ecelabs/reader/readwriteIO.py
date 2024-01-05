import smbus
import time
import FuncTrans

# Edit By Minh on 1/3/2024: Change the code to match new FPGA PCB
"""
    write functions: write_port, write_bit, write_allports, write_bitstr, write_bitstr_fast
    read functions: read_port, read_port_pin, read_allports, read_all

    Important HW Info:
        There are 8 MCP23017 IO Expanders on the PCB to correspond to 103 FPGA IOs
        These devices are on I2C Bus 1 of the Pi4B (GPIO 2-3) which have addresses from 0x20 - 0x27
        Each MCP23017 has:
            - 2 ports: Port A and Port B
            - Each port has 8 GPIOs (Total of 16 IOs / MCP23017)
            - Before read/write IO, you need to set the direction of each port by:
                - Output Port: Write 0x00 to register with address 0x00 for port A (all pins)
                               Write 0x00 to register with address 0x01 for port B (all pins)
                - Input Port:  Write 0xFF to register with address 0x00 for port A (all pins)
                               Write 0xFF to register with address 0x01 for port B (all pins)
            - To read/write: Address of GPIO register of Port A: 0x12
                             Address of GPIO register of Port B: 0x13 

"""

# Global Variable 
B = 1 # Use bus 1 on Raspberry Pi (GPIO 2, 3)


# Function to write to all GPIOs of a port of a MCP23017
# mcp_addr (x20-x27), bit_str = 8 bit binary
def write_port(mcp_addr, port_addr, bit_str):
    # Write the new value back to GPIOA
    smbus.SMBus(B).write_byte_data(mcp_addr, port_addr, bit_str)
    return


# Function to write a specific GPIO of a port of a MCP23017
# mcp_addr (x20-x27), port_addr (A=x12, B=x13), pin (0-7), bit (0/1)
def write_bit(mcp_addr, port_addr, pin, bit):
    # Read to get 8-bit of port
    current_value = smbus.SMBus(B).read_byte_data(mcp_addr, port_addr)

    # Update the value for the desired pin
    if bit == 0:
        new_value = current_value & ~(1 << pin)  # Clear the bit
    else:
        new_value = current_value | (1 << pin)  # Set the b
    
    # write bit_str = new_value to the write function
    write_port(mcp_addr, port_addr, bit_str=new_value)
    return


# Function to write two ports at the same time, efficient since it sends only 1 i2c package
# value_portA = 8-bit binary int
# value_portB = 8-bit binary int
def write_allports(mcp_addr, value_portA, value_portB):
    smbus.SMBus(B).write_i2c_block_data(mcp_addr, 0x12, [value_portA, value_portB])
    return
    

""" Write Bit String of PB[0:19] (bitstr = {[PB[0], PB[1], ...PB[20]})
    bistr MSB / bistr[0] = PB[0] 
    Input should be 20 digits and default is all 0
    This method is slow since it needs to send multiple i2c packages
    However, it's better to implement into the current system as it uses LED(#).on() in FuncTrans"""
def write_bitstr(bitstr='0'*20):
    start_time = time.time()
    bitstr = bitstr + '0' * (20 - len(bitstr)) # Make sure there are 20 digits in bitstr
    
    D = {}
    for index, bitchar in enumerate(bitstr):
        D["PB " + str[index]] = int(bitchar)
        if bitchar == '0':
            FuncTrans.LED(index).off()
        elif bitchar == '1':
            FuncTrans.LED(index).on()
    
    end_time = time.time()
    print("Write Log: ", D)
    print("write_bitstr done in " + str(end_time-start_time) + "s")
    return


# Faster and more efficient of write bit string
# Please use this rather than write_bitstr
def write_bitstr_fast(bitstr='0'*20):
    start_time = time.time()
    bitstr = bitstr + '0' * (20 - len(bitstr)) # Make sure there are 20 digits in bitstr

    D = {}
    PB0_7 = int(bitstr[0:8], 2)
    PB8_13 = int(bitstr[8:14], 2)
    PB14_19 = int(bitstr[14:20], 2) << 2

    D["PB[0:7]"] = bitstr[0:8]
    D["PB[8:13]"] = bitstr[8:14]
    D["PB[14:19]"] = bitstr[14:20]
    write_allports(mcp_addr=0x20, value_portA=PB8_13, value_portB=PB14_19)
    write_port(mcp_addr=0x21, port_addr=0x13, bit_str=PB0_7)

    end_time = time.time()
    # print("Write Log: ", D)
    # print("write_bitstr done in " + str(end_time-start_time) + "s")
    return


def read_port(mcp_addr, port_addr):
    return smbus.SMBus(B).read_byte_data(mcp_addr, port_addr)


def read_port_pin(mcp_addr, port_addr, pin):
    value = read_port(mcp_addr, port_addr)
    pin_value = (value >> pin) & 1
    return pin_value


# Return a list [8bit PortA, 8bit PortB]
# This is quicker to read each port since it condenses into 1 i2c package
def read_allports(mcp_addr):
    ports = smbus.SMBus(B).read_i2c_block_data(mcp_addr, 0x12, 2) # 0x12=read from portA, 2=2 bytes
    portA = ports[0]
    portB = ports[1]
    return [portA, portB]


"""This function reads all read IO of FPGA (LED, RIGHT, LEFT, SS)
    Return a dictionary represents each read input
    This function is prioritized on efficient. It sends out 6 consecutive packages of i2c.
    Reserve the format MSB - LSB (i.e. RIGHT = RIGHT[7]...RIGHT[0])"""
def read_all():
    start_time = time.time()

    D = {}
    portA = 0
    portB = 1
    
    mcp_x20_GPB0 = read_port_pin(0x20, 0x13, 0)
    # print("mcp_x20_GPB0 = " + str(mcp_x20_GPB0))
    
    mcp_x26_allports = read_allports(0x26)
    mcp_x26_allports[portB] = (mcp_x26_allports[portB] & 0b11011111) | (mcp_x20_GPB0 << 5) 

    mcp_x26 = [format(port, '08b') for port in mcp_x26_allports]
    LED = mcp_x26[portA][5:] # LED = 0x26 portA {pin0=RED, pin1=GREEN, pin2=BLUE}
    BLUE = LED[0]   # this is string index, not pin #
    GREEN = LED[1]  # this is string index, not pin #
    RED = LED[2]    # this is string index, not pin #
    RIGHT = mcp_x26[portB][::-1] # order is swapped in hw, pin0=RIGHT[7] ...
    
    mcp_x25 = [format(port, '08b') for port in read_allports(0x25)]
    LEFT = mcp_x25[portA][::-1] # order is swapped in hw, pin0=LEFT[7]
    SS7 = mcp_x25[portB]

    mcp_x24 = [format(port, '08b') for port in read_allports(0x24)]
    SS6 = mcp_x24[portA]
    SS5 = mcp_x24[portB]

    mcp_x23 = [format(port, '08b') for port in read_allports(0x23)]
    SS4 = mcp_x23[portA]
    SS3 = mcp_x23[portB]

    mcp_x22 = [format(port, '08b') for port in read_allports(0x22)]
    SS2 = mcp_x22[portA]
    SS1 = mcp_x22[portB]

    # SS0 is on port A of a chip that has both read / write function
    SS0 = format(read_port(mcp_addr=0x21, port_addr=0x12), '08b')

    D["LED"] = LED
    D["BLUE"] = BLUE
    D["GREEN"] = GREEN
    D["RED"] = RED
    D["RIGHT"] = RIGHT
    D["LEFT"] = LEFT
    D["SS7"] = SS7
    D["SS6"] = SS6
    D["SS5"] = SS5
    D["SS4"] = SS4
    D["SS3"] = SS3
    D["SS2"] = SS2
    D["SS1"] = SS1
    D["SS0"] = SS0

    end_time = time.time()
    # print("read_all done in " + str(end_time-start_time) + "s")
    return D

    