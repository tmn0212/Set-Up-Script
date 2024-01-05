from readwriteIO import *
from time import sleep

# Test 1
RIGHT = '10010110'
LEFT  = '11110000'
RED   = '0'
GREEN = '1'
BLUE  = '1'
PB19  = '1'

PB0_7 = RIGHT[::-1]
PB8_15 = LEFT[::-1]
PB16 = BLUE
PB17 = GREEN
PB18 = RED

bitstr = PB0_7 + PB8_15 + PB16 + PB17 + PB18 + PB19

write_bitstr_fast(bitstr)
time.sleep(1)

# Test 2
RIGHT = '10111110'
LEFT  = '11100011'
RED   = '1'
GREEN = '0'
BLUE  = '1'
PB19  = '0'

PB0_7 = RIGHT[::-1]
PB8_15 = LEFT[::-1]
PB16 = BLUE
PB17 = GREEN
PB18 = RED

bitstr = PB0_7 + PB8_15 + PB16 + PB17 + PB18 + PB19
write_bitstr_fast(bitstr)
time.sleep(0.004)