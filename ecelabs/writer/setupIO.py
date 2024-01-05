import smbus
import time

# Edit By Minh on 1/3/2024: Change the code to match new FPGA PCB
"""
    Setup Functions: setIO, resetIO, zero_all_IO

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


# setIO: setting IO direction (out/in) for each GPIO on each port of each MCP23017
# This function sends out 7 i2c packages
def setIO():
    start_time = time.time()
    
    # Create an SMBus object
    bus = smbus.SMBus(B)
    
    """ Function Definitions:
        write_i2c_block_data(mcp_addr, port_readfrom, [value_A, value_B])
            mcp_addr = MCP23017 Address on I2C (0x20 - 0x27)
            port_readfrom = what port's register to start block read, always use port A (0x00) to set IODIR for both ports
            valueA = 8bit IODIR values of portA (0=Output, 1=input) i.e. 00000001 means only pin0 is input, 0xFF=all input pins, 0x00=all output pins
            valueB = same as valueA but for portB

        write_byte_data(mcp_addr, port_readfrom, value)
            this function is for writing to a port
            port_readform: IODIR registers - portA=0x00 and portB=0x01
            value: 8bit integer like above
    """
    # In the bracket, we need to set 4 registers [IODIRA, IODIRB, IPOLA, IPOLB] which represents from 0x00 - 0x03
    bus.write_i2c_block_data(0x20, 0x00, [0x00, 0x03, 0x00, 0x00]) # 0x03 since we use PB[20] and HWCLK as inputs
    bus.write_i2c_block_data(0x21, 0x00, [0xFF, 0x00, 0x00, 0x00]) # PortA for input, portB for output
    bus.write_i2c_block_data(0x23, 0x00, [0xFF, 0xFF, 0x00, 0x00])
    bus.write_i2c_block_data(0x24, 0x00, [0xFF, 0xFF, 0x00, 0x00])
    bus.write_i2c_block_data(0x25, 0x00, [0xFF, 0xFF, 0x00, 0x00])
    bus.write_i2c_block_data(0x26, 0x00, [0xFF, 0xFF, 0x00, 0x00])

    bus.write_i2c_block_data(0x27, 0x01, [0x00, 0x00, 0x00]) # Set x27=addr, x01=IODIRB, x00=set IODIRn as output


    end_time = time.time()
    print("setIO done in " + str(end_time-start_time) + "s")
    return


# Reset all the PB[0:20] push buttons to 0
def resetIO():
    start_time = time.time()

    # Create an SMBus object
    bus = smbus.SMBus(B)

    bus.write_i2c_block_data(0x20, 0x12, [0x00, 0x00])
    bus.write_byte_data(0x21, 0x13, 0x00)

    end_time = time.time()
    print("resetIO done in " + str(end_time-start_time) + "s")
    return


# set all IO of all MCP23017 to 0s and then do setIO (Default = True)
def zero_all_IO(is_setIO=True):
    start_time = time.time()
    # Select all mcp devices
    for mcp_addr in [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]:
        # set all IO ports to write (no read)
        for iodir in [0x00, 0x01]:
            smbus.SMBus(B).write_byte_data(mcp_addr, iodir, 0x00)

        # Set all IO to 0
        for port_addr in [0x12, 0x13]:
            smbus.SMBus(B).write_byte_data(mcp_addr, port_addr, 0x00)

    if (is_setIO):
        setIO()

    end_time = time.time()
    print("zero_all_IO done in " + str(end_time-start_time) + "s")
    return