import serial
from serial import Serial
import os
import time
#os.system('cls')
# os.system('clear')

s = serial.Serial('COM6',115200,timeout = 1)
print('done')

def send_request(str_):
   s.write(str_.encode('ASCII'))
   print('run in def send_request')

def get_response(s):
   x_rt = ''
   y_rt = ''
   z_rt = ''
   feed_rate = ''
   flag = 0

   data = s.read_until()
   a = data.decode('ASCII')
   print(a)
   a = '<Run|MPos:1.376,3.000,4.000|FS:100,0>'
   for i in a:
      if i =='R':
         mode = 1
      elif i == 'I':
         mode = 0

      if i == ':' and flag == 0:
         flag = 1
      elif flag == 1 and i == ',':
         flag = 2
      elif flag == 1:
         x_rt = x_rt + i
      elif flag == 2 and i == ',':
         flag = 3
      elif flag == 2:
         y_rt = y_rt + i
      elif flag == 3 and i == '|':
         flag = 4
      elif flag == 3:
         z_rt = z_rt + i
      elif flag == 4 and i == ':':
         flag = 5
      elif flag == 5 and i ==',':
         flag = 0
      elif flag == 5:
         feed_rate = feed_rate + i
   print(x_rt)
   print(y_rt)
   print(z_rt)
   print(feed_rate)
   return (x_rt, y_rt, z_rt, feed_rate)

def send_gcode(gcode):
   s.write(bytes(gcode+"\r", encoding='ascii'))
   print('sent gcode done')
   get_response(s)

send_request('?')
get_response(s)
get_response(s)

print('log 1')
send_request('?')
get_response(s)

send_request('?')
get_response(s)

send_gcode('g01 f100 x100')

for i in range(100):
   send_request('?')
   (a,b,c,d) = get_response(s)
   print(a)
   print(b)
   print(c)
   print(d)

get_response(s)

