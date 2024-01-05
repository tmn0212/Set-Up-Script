from setupIO import *
from readwriteIO import *
from time import sleep
import smbus

D = {}

# Expected Result for test 1
D1 = {"LED": '110', 
      "BLUE": '1', 
      "GREEN": '1',
      "RED": '0',
      "RIGHT": '10010110',
      "LEFT": '11110000',
      "SS0": '10010110',
      "SS1": '01001011',
      "SS2": '00100101',
      "SS3": '00010010',
      "SS4": '11111000',
      "SS5": '11111100',
      "SS6": '01111110',
      "SS7": '10111111'}

D2 = {"LED": '101', 
      "BLUE": '1', 
      "GREEN": '0',
      "RED": '1',
      "RIGHT": '10111110',
      "LEFT": '11100011',
      "SS0": '10111110',
      "SS1": '11011111',
      "SS2": '11101111',
      "SS3": '01110111',
      "SS4": '11110001',
      "SS5": '01111000',
      "SS6": '10111100',
      "SS7": '01011110'}

# zero_all_IO(is_setIO=True)
setIO()
while True:
      print(read_all())
      time.sleep(1)

# start_time = time.time()
# while True:
#      D = read_all()
#      print(D)
#      time.sleep(1)
#      if (D == D1):
#          # [print(f"{key}: {value}") for key, value in D.items()]
#          print(" Test 1 Passed in: ", time.time() - start_time)
#          print("--------------------------------------------------------------")
#          print(D)
#          break

# start_time = time.time()
# while True:
#     D = read_all()
#     if (D == D2):
#         # [print(f"{key}: {value}") for key, value in D.items()]
#         print(" Test 2 Passed in: ", time.time() - start_time)
#         print("--------------------------------------------------------------")
#         break
