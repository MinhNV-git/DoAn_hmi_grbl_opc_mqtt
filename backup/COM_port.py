import serial
from serial import Serial
import os
os.system('cls')
# os.system('clear')

s = serial.Serial('COM5',115200)
# for i in range(50):
#     data = s.read(1)
#     x = data.decode('ASCII')
#     print(type(x))

flag_ = 0
flag_1 = 0
flag_2 = 0
str_data = ''
axis_x = ''
axis_y = ''
axis_z = ''


while True:
    data = s.read(50)
    a = data.decode('ASCII')
    print(a)
    # if a == '<' and flag_ == 0:
    #     flag_ = 1
    # elif (a == 'F' or a == 'L') and flag_ == 1:
    #     os.system('cls')
    #     print('**************      KQ      **************')
    #  #   print(str_data)
    #     print(axis_x)
    #     print(axis_y)
    #     print(axis_z)

    #     str_data = ''
    #     axis_x = ''
    #     axis_y = ''
    #     axis_z = ''
    #     flag_ = 0
    # elif flag_ == 1:
    #     str_data = str_data + a 
    #     if a == 'I':
    #         mode = 1
    #     elif a == 'R':
    #         mode = 2
        
    #     if a == ':' and flag_1 == 0:
    #         flag_1 = 1
    #     elif a == ',' and flag_1 == 1:
    #         flag_1 = 2
    #     elif flag_1 == 1:
    #         axis_x = axis_x + a 
    #     elif flag_1 == 2 and a == ',':
    #         flag_1 = 3
    #     elif flag_1 == 2:
    #         axis_y = axis_y + a
    #     elif flag_1 == 3 and a == '|':
    #         flag_1 = 0
    #     elif flag_1 == 3:
    #         axis_z = axis_z + a 
    