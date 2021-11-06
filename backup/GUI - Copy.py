import tkinter as tk
from functools import partial
import threading
import socket
from tkinter import messagebox
from opcua import Server
from random import randint
import datetime 
import time
import serial
from serial import Serial
import os
import math
import logging

#logging.basicConfig(level= logging.DEBUG, format='%(levelname)s:\t''%(message)s')
#logging.basicConfig(level= logging.ERROR, format='%(levelname)s:\t''%(message)s')
logging.basicConfig(level= logging.INFO, format='%(levelname)s:\t''%(message)s')

class GUI_grbl(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Controler GRBL - VIMESLAB")
		self.geometry('1280x700')

		self.firstName = tk.Label(self,text = 'VIMESLAB - CNC',font = ('arial', 15, 'bold'))
		self.firstName.pack()

		# CHON PORT CONNECT GRBL
		self.Port = tk.Button(self,text = 'PORT',width = 10,height=1,command = lambda: self.handles.connect_grbl(self.Port_entry.get()))
		self.Port.place(x=10, y = 50)
		self.Port_entry = tk.Entry(self,font = ('calibri', 15),width = 20)
		self.Port_entry.place(x=100,y=50)

		# CHON FILE G-CODE
		self.File = tk.Button(self,text = 'FILE',width = 10,height=1, command = lambda: self.handles.get_file_gcode(self.File_entry.get()))
		self.File.place(x=400, y = 50)
		self.File_entry = tk.Entry(self,font = ('calibri', 15),width = 35)
		self.File_entry.place(x=490,y=50)

		# THONG TIN TOA DO, FEEDRATE, SPEED
		self.text_xyz = tk.Label(self,text='--------------- Position ---------------',font = ('arial', 10),fg='#444444')
		self.text_xyz.place(x=500,y=105)

		self.X = tk.Label(self,text='X:',font= ('arial', 15))
		self.X.place(x=420,y=150)
		self.X_real = tk.Label(self,text='000.000',font= ('arial', 15),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.X_real.place(x=449,y=150)
		self.X_goc = tk.Label(self,text='001.000',font= ('arial', 15),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.X_goc.place(x=570,y=150)

		self.Y = tk.Label(self,text='Y:',font= ('arial', 15))
		self.Y.place(x=420,y=190)
		self.Y_real = tk.Label(self,text='000.000',font= ('arial', 15),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Y_real.place(x=449,y=190)
		self.Y_goc = tk.Label(self,text='001.000',font= ('arial', 15),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Y_goc.place(x=570,y=190)

		self.Z = tk.Label(self,text='Z:',font= ('arial', 15))
		self.Z.place(x=420,y=230)
		self.Z_real = tk.Label(self,text='000.000',font= ('arial', 15),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Z_real.place(x=449,y=230)
		self.Z_goc = tk.Label(self,text='001.000',font= ('arial', 15),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Z_goc.place(x=570,y=230)

		self.feedrate_text = tk.Label(self,text = 'Feed rate:',font = ('arial', 11))
		self.feedrate_text.place(x=700,y=170)
		self.feedrate_view = tk.Label(self,text = '0',font = ('arial', 11))
		self.feedrate_view.place(x=780,y=170)

		self.speed_text = tk.Label(self,text = 'Speed:',font = ('arial', 11))
		self.speed_text.place(x=700,y=200)
		self.speed_view = tk.Label(self,text = '0',font = ('arial', 11))
		self.speed_view.place(x=780,y=200)

		# NUT DIEU KHIEN
		self.start = tk.Button(self,text='START',font = ('arial', 12),width=35,height=1,command = lambda: self.handles.button_start())
		self.start.place(x=10,y=250)

		self.opcUA = tk.Button(self,text='Start OPC UA Server',font = ('arial', 15),width=28,height=1,command = lambda: self.handles.OpenOPC_UA_server())
		self.opcUA.place(x=10,y=120)

		self.X_plus = tk.Button(self,text='X+',width=10,height=2, command =lambda: self.handles.x_plus(self.unit_x.get()))
		self.X_plus.place(x=20,y=295)
		self.X_sub = tk.Button(self,text='X-',width=10,height=2, command = lambda: self.handles.x_sub(self.unit_x.get()))
		self.X_sub.place(x=20,y=375)
		self.unit_x = tk.Entry(self,font = ('arial', 12),width=8)
		self.unit_x.place(x=20,y=345)

		self.Y_plus = tk.Button(self,text='Y+',width=10,height=2, command =lambda: self.handles.y_plus(self.unit_y.get()))
		self.Y_plus.place(x=130,y=295)
		self.Y_sub = tk.Button(self,text='Y-',width=10,height=2, command =lambda: self.handles.y_sub(self.unit_y.get()))
		self.Y_sub.place(x=130,y=375)
		self.unit_y = tk.Entry(self,font = ('arial', 12),width=8)
		self.unit_y.place(x=130,y=345)

		self.Z_plus = tk.Button(self,text='Z+',width=10,height=2, command =lambda: self.handles.z_plus(self.unit_z.get()))
		self.Z_plus.place(x=240,y=295)
		self.Z_sub = tk.Button(self,text='Z-',width=10,height=2, command =lambda: self.handles.z_sub(self.unit_z.get()))
		self.Z_sub.place(x=240,y=375)
		self.unit_z = tk.Entry(self,font = ('arial', 12),width=8)
		self.unit_z.place(x=240,y=345)

		self.return_ = tk.Button(self,text='Return to 0',font = ('arial', 12),width=15,height=1, command = lambda: self.handles.return_0_button())
		self.return_.place(x=10,y=430)

		self.pause = tk.Button(self,text='PAUSE',font = ('arial', 12),width=15,height=1,command = lambda: self.handles.pause_button())
		self.pause.place(x=190,y=430)

		self.stop = tk.Button(self,text='STOP',font = ('arial', 12),width=35,height=1,bg='#EE0000',command = lambda: self.handles.stop_button())
		self.stop.place(x=10,y=482)

		# GUI COMMAND TRUC TIEP CHO GRBL
		self.text_command = tk.Label(self,text='minh',font = ('arial', 10),width=48,height=14,relief='solid',borderwidth=1,anchor ='sw', justify = 'left')
		self.text_command.place(x=400,y=270)

		self.command_entry = tk.Entry(self,font = ('arial', 12),width=40)
		self.command_entry.place(x=400,y=495)
		self.send_command = tk.Button(self,text='Send',width=10,command = lambda: self.handles.send_script2grbl_and_get_reponse(self.command_entry.get()))
		self.send_command.place(x=765,y=495)

		self.status = tk.Label(self,font = ('arial', 11))
		self.status.place(x=10,y=165)

		self.reset2zezo = tk.Button(self,text='Reset zezo',font = ('arial', 12),width=15,height=1,bg='#FF66CC', command = lambda: self.handles.reset2zezo())
		self.reset2zezo.place(x=10,y=522)

		self.handles = handles(self)
		logging.info('//////////////////////   GUI IS ALREADY!!!   /////////////////////////')

	def notification(self, title, msg):
		messagebox.showinfo(str(title), str(msg))

		


class handles():
	def __init__(self,gui):
		super().__init__()
		self.gui =gui
		self.name = ""
		self.file_gcode= ''
		self.com2grbl = ''
		self.server = ''
		self.x_send2opc = ''
		self.y_send2opc = ''
		self.z_send2opc = ''
		self.frx_send2opc = ''
		self.fry_send2opc = ''
		self.frz_send2opc = ''
		
		self.x = 0
		self.y = 0
		self.z = 0
		self.fr = 0

		self.x_opc=0
		self.y_opc=0
		self.z_opc=0

		self.delta_x = 0
		self.delta_y = 0 
		self.delta_z = 0 

		self.gobal_pause = 0
		self.line_gcode = ''

	def OpenOPC_UA_server(self):
		th_opc = threading.Thread(target=self.OpenOPC_UA_server_())
		th_opc.start()
	def OpenOPC_UA_server_(self):
		logging.info('MAIN:    Create OPC UA Server')
		self.server = Server()

		self.url = "opc.tcp://127.0.0.1:4840"
		self.server.set_endpoint(self.url)
		logging.info('OPC IP:  opc.tcp://127.0.0.1')
		logging.info('OPC PORT: 4840')

		self.name_opc = "OPCUA_SIMULATION_SERVER"
		self.addspace = self.server.register_namespace(self.name_opc)

		self.node = self.server.get_objects_node()

		self.Param = self.node.add_object(self.addspace, "Parameters")

		self.x_send2opc = self.Param.add_variable(self.addspace, "axis X", 0)
		self.y_send2opc = self.Param.add_variable(self.addspace, "axis Y", 0)
		self.z_send2opc = self.Param.add_variable(self.addspace, "axis Z", 0)
		self.frx_send2opc = self.Param.add_variable(self.addspace, "feed rate X", 0)
		self.fry_send2opc = self.Param.add_variable(self.addspace, "feed rate Y", 0)
		self.frz_send2opc = self.Param.add_variable(self.addspace, "feed rate Z", 0)
		logging.info('OPC:    TAG - axis X, axis Y, axis Z, feed rate X, feed rate Y, feed rate Z')

		self.x_send2opc.set_writable()
		self.y_send2opc.set_writable()
		self.z_send2opc.set_writable()
		self.frx_send2opc.set_writable()
		self.fry_send2opc.set_writable()
		self.frz_send2opc.set_writable()

		self.server.start()
		logging.info('MAIN:    OPC UA is started')
		self.gui.opcUA['bg'] = '#00FFFF'
		self.gui.status['text'] = self.gui.status['text'] + 'OPC UA Server is started (opc.tcp://127.0.0.1:4840)\n'

	def send2OPC(self,a,b,c,d,e,f):
		if self.gui.opcUA['bg'] == '#00FFFF':
			self.x_send2opc.set_value(a)
			self.y_send2opc.set_value(b)
			self.z_send2opc.set_value(c)
			self.frx_send2opc.set_value(d)
			self.fry_send2opc.set_value(e)
			self.frz_send2opc.set_value(f)

			self.gui.text_command['text'] = 'OPC DATA: (x, y, z) = '+'('+str(a)+', '+str(b)+', '+str(c) +')'
			self.gui.text_command['text'] = self.gui.text_command['text'] + '\nOPC DATA: (frx, fry, frz) = '+'('+str(d)+', '+str(e)+', '+str(f)+')'
			# o
		else:
			logging.info('OPC  : OPC UA server is not started!!!!')
			self.gui.notification("Chú ý!!!",'OPC UA server is not started!\n')

	def connect_grbl(self,ip):
		th_port = threading.Thread(target=self.connect_grbl_(ip))
		th_port.start()
	def connect_grbl_(self,inputPORT):
		logging.info('MAIN:    Connect to port ' + inputPORT)
		self.com2grbl = serial.Serial(inputPORT,115200,timeout = 1)
		logging.info('MAIN:    Done connect port '+inputPORT )
		logging.info('MAIN:    Baulrate: 115200 ')

		self.gui.Port['bg'] = '#00FFFF'
		self.gui.status['text'] = self.gui.status['text'] + 'Connect to GRBL is successfully\n'

		logging.info('MAIN:    Send first script to start GRBL')
		self.com2grbl.write('\r'.encode('ASCII'))
		data = self.com2grbl.read_until()
		data = self.com2grbl.read_until()
		logging.info('GRBL:    '+data.decode('ASCII'))
		self.gui.text_command['text'] = data.decode('ASCII')

		logging.info('MAIN:    Run to function - get real time x,y,z,fr')
		self.get_reponse_xyz()
		logging.info('MAIN:    Done handles PORT button')

	def get_file_gcode(self,file_path):
		logging.info('MAIN:    FILE PATH')
		if file_path == '':
			self.gui.notification("Chú ý!!!",'Nhập đường dẫn đến file Gcode\n')
			logging.info('MAIN: "Chú ý!!! Nhập đường dẫn đến file Gcode')
		else:
			for i in file_path:
				if i == '\\':
					i = '/'
			print(file_path)
			self.file_gcode = file_path
			self.gui.File['bg'] = '#00FFFF'
			self.gui.start['bg'] = '#00FFFF'
			self.gui.return_['bg'] = '#00FFFF'
			self.gui.pause['bg'] = '#00FFFF'

	def send_script2grbl_and_get_reponse(self,script):
		t2 = threading.Thread(target=self.send_script2grbl_and_get_reponse_(script))
		t2.start()
	def send_script2grbl_and_get_reponse_(self,script):
		try:
			#print('Run in send_script2grbl')
			self.com2grbl.write(bytes(script+"\r", encoding='ascii'))
			# print('send done')
			# data = self.com2grbl.read_until()
			# a = data.decode('ASCII')
			self.gui.command_entry.delete(0,'end')
			logging.info('MAIN:    Send to grbl: '+script)
		except:
			logging.warning('MAIN:   FAIL to send script')
	# lay vi tri x, y, z, feed rate 
	def get_reponse_xyz(self):
		t1 = threading.Thread(target=self.get_reponse_xyz_thread)
		t1.start()
	def get_reponse_xyz_thread(self):
		x = 0
		y = 0
		z = 0
		fr = 0
		del_x = 0
		del_y = 0
		del_z = 0
		self.send2OPC(0,0,0,100,100,100)
		while True:
			while self.gobal_pause ==1:
				logging.info('THREAD 1:  PAUSE read x,y,z.fr ')
			try:
				self.com2grbl.write('?'.encode('ASCII'))
				data = self.com2grbl.read_until()
				a = data.decode('ASCII')
				#print(a)

				(self.x, self.y, self.z, self.fr, del_x, del_y, del_z) = self.handles_string(a)

				if del_x != -100000000:
					self.delta_x = del_x
					self.delta_y = del_y 
					self.delta_z = del_z


				#(self.x, self.y, self.z, self.fr) = self.handles_string(a)
				if self.x != -100000000:
					self.view_xyz(self.x,self.y,self.z,self.fr,self.delta_x, self.delta_y, self.delta_z)
					x = self.x
					y = self.y
					z = self.z
				elif self.x == -100000000:
					self.view_xyz(x,y,z,0,self.delta_x, self.delta_y, self.delta_z)


			except:
				logging.warning('THREAD 1 :Cannot get data with format, no display')
				continue
		logging.error('THREAD 1 :ERROR - OUT MAINLOOP')

	# xu ly chuoi 
	def handles_string(self,a):
		x_rt = ''
		y_rt = ''
		z_rt = ''
		feed_rate = ''
		speed = ''
		delta_x = '-100000000'
		delta_y = '-100000000'
		delta_z = '-100000000'
		flag = 0

		if a[0] != 'o':
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
				elif flag == 4 and i == 'F':
					flag = 5
				elif flag == 5 and i ==':':
					flag = 6
				elif flag == 6 and i ==',':
					flag = 7 
					#break
				elif flag == 6:
					feed_rate = feed_rate + i
				elif flag == 7  and i == '>':
					flag = 0
					break
				elif flag == 7 and i == '|':
					flag = 8
				elif flag == 7:
					speed = speed + i
				elif flag == 8 and i =='W':
					flag =9
					delta_x = ''
					delta_y = ''
					delta_z = ''
				elif flag ==9 and i ==':':
					flag = 10
				elif flag == 10 and i == ',':
					flag = 11
				elif flag == 10:
					delta_x = delta_x + i
				elif flag == 11 and i ==',':
					flag = 12		
				elif flag ==11:
					delta_y = delta_y + i	
				elif flag ==12 and i == '>':
					flag = 0
					break
				elif flag ==12 :
					delta_z = delta_z+i 
    					
			# print(x_rt)
			# print(y_rt)
			# print(z_rt)
			# print(feed_rate)
			# print(delta_x)
			# print(delta_y)
			# print(delta_z)
			return (float(x_rt), float(y_rt), float(z_rt), float(feed_rate), float(delta_x), float(delta_y), float(delta_z)) #, float(delta_x), float(delta_y), float(delta_z)
		else:
			logging.debug('THREAD 1:  du lieu loi, khong theo format')
			return (float(-100000000),float(-100000000),float(-100000000),float(-100000000), float(-100000000),float(-100000000),float(-100000000))#, float(-100000000),float(-100000000),float(-100000000)			

	# in gia tri ra GUI
	def view_xyz(self,x,y,z,fr,del_x,del_y,del_z):
		# self.gui.x_send2opc.set_value(x)
		# self.gui.y_send2opc.set_value(y)
		# self.gui.z_send2opc.set_value(z)

		self.gui.X_real['text'] = str(x-del_x)
		self.gui.Y_real['text'] = str(y-del_y)
		self.gui.Z_real['text'] = str(z-del_z)
		self.gui.X_goc['text'] = str(x)
		self.gui.Y_goc['text'] = str(y)
		self.gui.Z_goc['text'] = str(z)
		self.gui.feedrate_view['text'] = str(fr)
		# self.gui.X_goc['text'] = str(x)


	def read_script_line(self,n,file_path):
		file_open = open(file_path,'r')
		for i in range(n):
			str_ = file_open.readline()
		return str_

	def handles_script_line(self, script_line):
		flag = 0
		str_G = ''
		str_X = ''
		str_Y = ''
		str_Z = ''
		for i in script_line:
			if i == 'G' or i == 'g':
			    flag = 1;
			elif flag == 1 and i == ' ':
			    flag = 0
			elif flag == 1:
			    str_G = str_G + i
			elif i == 'X' or i == 'x':
			    flag = 2
			elif flag == 2 and i == ' ':
			    flag = 0
			elif flag == 2:
			    str_X = str_X + i
			elif i == 'Y' or i == 'y':
			    flag = 3
			elif flag == 3 and i == ' ':
			    flag = 0
			elif flag == 3:
			    str_Y = str_Y + i
			elif i =='z' or i == 'Z':
			    flag = 4
			elif flag == 4 and i == ' ':
			    flag =0
			elif flag == 4:
			    str_Z = str_Z + i
			else:
			    flag = 0
		if str_G == '':
		    str_G = '10071999'
		if str_X == '':
		    str_X = '10071999'
		if str_Y == '':
		    str_Y = '10071999'
		if str_Z == '':
		    str_Z = '10071999'
		return (float(str_G), float(str_X), float(str_Y), float(str_Z))


	def button_start(self):
		t2 = threading.Thread(target=self.control_gcode_file)
		t2.start()
	def control_gcode_file(self):
		#self.gui.X_goc['text'] = 'button'
		n = 2
		frx_opc = 0
		fry_opc = 0
		frz_opc = 0
		x_opc = -self.delta_x
		y_opc = -self.delta_y
		z_opc = -self.delta_z
		flag_n = 1
		fr_opc = 0
		v = -1


		while True:
			while self.gobal_pause ==1:
				logging.info('MAIN:    PAUSE RUN via file')

			if flag_n == 1:
				line_from_gcode_file = self.read_script_line(n,self.file_gcode)
				# self.gui.X_goc['text'] = line_from_gcode_file
				self.send_script2grbl_and_get_reponse(line_from_gcode_file)
				flag_n = 0

			# self.gui.X_goc['text'] = 'ok'

			if line_from_gcode_file == '':
				break
			self.line_gcode = line_from_gcode_file
			(g_file, x_file, y_file, z_file) = self.handles_script_line(line_from_gcode_file)

			if x_file != x_opc and x_file != 10071999:
			    x_old = x_opc
			    x_opc = x_file
			if y_file != y_opc and y_file != 10071999:
			    y_old = y_opc
			    y_opc = y_file
			if z_file != z_opc and z_file != 10071999:
			    z_old = z_opc
			    z_opc = z_file

			# self.gui.Y_goc['text'] = 'ok'

			if x_file == 10071999 and y_file ==10071999:
			    v = 1           # z
			elif x_file ==10071999 and z_file ==10071999:
			    v =2            # y
			elif y_file ==10071999 and z_file ==10071999:
			    v =3            # x
			elif x_file == 10071999:
			    v = 4           # yz
			elif y_file == 10071999:
			    v =5            # xz
			elif z_file == 10071999:
			    v = 6           # xy

			# self.x , self.y, self.z , self.fr
			# fr_opc = fr_opc/60
			# self.fr = self.fr/60

			if fr_opc != self.fr:
				fr_opc = self.fr

			# self.gui.Z_goc['text'] = 'ok'
			
			if v == 1:
				frz_opc = fr_opc
				frx_opc = 0
				fry_opc = 0
			elif v ==2:
				fry_opc = fr_opc
				frx_opc = 0
				frz_opc = 0
			elif v ==3:
				frx_opc = fr_opc
				fry_opc = 0
				frz_opc = 0
			elif v == 4:
				y_ = abs(y_old - y_opc)
				z_ = abs(z_old - z_opc)
				fry_opc = math.sqrt(y_*y_ + z_ * z_)/math.sqrt(1+(z_/y_)*(z_/y_))
				frz_opc =  math.sqrt(y_*y_ + z_ * z_)/ math.sqrt(1+(y_/z_)*(y_/z_))
				frx_opc = 0
			elif v ==5:
				x_ = abs(x_old - x_opc)
				z_ = abs(z_old - z_opc)
				frz_opc =  math.sqrt(x_*x_ + z_ * z_)/ math.sqrt(1+(x_/z_)*(x_/z_))
				frx_opc =  math.sqrt(x_*x_ + z_ * z_)/ math.sqrt(1+(z_/x_)*(z_/x_))
				fry_opc = 0
			elif v ==6:
				x_ = abs(x_old - x_opc)
				y_ = abs(y_old - y_opc)
				fry_opc =  math.sqrt(x_*x_ + y_ * y_)/ math.sqrt(1+(x_/y_)*(x_/y_))
				frx_opc =  math.sqrt(x_*x_ + y_ * y_)/ math.sqrt(1+(y_/x_)*(y_/x_))
				frz_opc = 0
			else:
				x_ = abs(x_old - x_opc)
				y_ = abs(y_old - y_opc)
				z_ = abs(z_old - z_opc)
				tong =  math.sqrt(x_*x_ + y_*y_ + z_*z_)
				frx_opc = tong/ math.sqrt(1 + (y_/x_)*(y_/x_) + (z_/x_)*(z_/x_))
				fry_opc = tong/ math.sqrt(1 + (x_/y_)*(x_/y_) + (z_/y_)*(z_/y_))
				frz_opc = tong/ math.sqrt(1 + (x_/z_)*(x_/z_) + (x_/z_)*(x_/z_))

			# self.gui.X_goc['text'] = str(x_opc)
			# self.gui.Y_goc['text'] = str(y_opc)
			# self.gui.Z_goc['text'] = str(z_opc)
			#self.send2OPC(x_opc, y_opc, z_opc, frx_opc, fry_opc, frz_opc)
			self.send2OPC(x_opc/1000, y_opc/1000, -z_opc/1000, frx_opc/60000, fry_opc/60000, frz_opc/60000)
			#self.send2OPC(x_opc, y_opc, z_opc, frx_opc, fry_opc, frz_opc)

			if x_opc + self.delta_x == self.x and y_opc + self.delta_y == self.y and z_opc + self.delta_z == self.z:
				n = n + 1
				flag_n = 1
				#self.gui.text_command['text'] = str(n) + '   chay sang dong moi'





	def x_plus(self,ip):
		thread_unit = threading.Thread(target=self.x_plus_(ip))
		thread_unit.start()
	def x_plus_(self,ip):
		script = '$J=G21G91X' + ip + 'F25'
		self.send2OPC(self.x+int(ip), self.y, self.z, 25, 0, 0)
		self.send_script2grbl_and_get_reponse_(script)

	def x_sub(self,ip):
		thread_unit = threading.Thread(target=self.x_sub_(ip))
		thread_unit.start()
	def x_sub_(self,ip):
		script = '$J=G21G91X-' + ip + 'F25'
		self.send2OPC(self.x-int(ip), self.y, self.z, 25, 0, 0)
		self.send_script2grbl_and_get_reponse_(script)

	def y_plus(self,ip):
		thread_unit = threading.Thread(target=self.y_plus_(ip))
		thread_unit.start()
	def y_plus_(self,ip):
		script = '$J=G21G91Y' + ip + 'F25'
		self.send2OPC(self.x, self.y+int(ip), self.z, 0, 25, 0)
		self.send_script2grbl_and_get_reponse_(script)

	def y_sub(self,ip):
		thread_unit = threading.Thread(target=self.y_sub_(ip))
		thread_unit.start()
	def y_sub_(self,ip):
		script = '$J=G21G91Y-' + ip + 'F25'
		self.send2OPC(self.x, self.y-int(ip), self.z, 0, 25, 0)
		self.send_script2grbl_and_get_reponse_(script)

	def z_plus(self,ip):
		thread_unit = threading.Thread(target=self.z_plus_(ip))
		thread_unit.start()
	def z_plus_(self,ip):
		script = '$J=G21G91Z' + ip + 'F25'
		self.send2OPC(self.x, self.y, self.z+int(ip), 0, 0, 25)
		self.send_script2grbl_and_get_reponse_(script)

	def z_sub(self,ip):
		thread_unit = threading.Thread(target=self.z_sub_(ip))
		thread_unit.start()
	def z_sub_(self,ip):
		script = '$J=G21G91Z-' + ip + 'F25'
		self.send2OPC(self.x, self.y, self.z-int(ip), 0, 0, 25)
		self.send_script2grbl_and_get_reponse_(script)

	def return_0_button(self):
		t2 = threading.Thread(target=self.return_0_button_())
		t2.start()
	def return_0_button_(self):
		self.send_script2grbl_and_get_reponse_('G21G90 G0Z5 \nG90 G0 X0 Y0 \nG90 G0 Z0')


	def pause_button(self):
		t2 = threading.Thread(target=self.pause_button_())
		t2.start()

	def pause_button_(self):
		if self.gui.pause['text'] == 'PAUSE':	
			self.send_script2grbl_and_get_reponse_('!')
			self.gobal_pause = 1
			self.gui.X_real['text'] = str(self.x-self.delta_x)
			self.gui.Y_real['text'] = str(self.y-self.delta_y)
			self.gui.Z_real['text'] = str(self.z-self.delta_z)
			self.send_script2grbl_and_get_reponse_('!')
			self.gui.pause['text'] = 'Continue'
			self.gui.pause['bg'] = '#3399FF'
			#self.send2OPC(float(self.gui.X_goc['text']), float(self.gui.Y_goc['text']), float(self.gui.Z_goc['text']), 0,0,0)
			self.send2OPC(self.x,self.y,self.z,0,0,0)
		elif self.gui.pause['text'] == 'Continue':
			self.gobal_pause = 0
			# print(self.x)
			# print(self.y)
			# print(self.z)
			self.send_script2grbl_and_get_reponse_('~')
			self.gui.pause['text'] = 'PAUSE'
			self.gui.pause['bg'] = '#00FFFF'

	def reset2zezo(self):
		t_zezo = threading.Thread(target=self.reset2zezo_())
		t_zezo.start()
	def reset2zezo_(self):
		self.send_script2grbl_and_get_reponse_('G10 P0 L20 X0 Y0 Z0')
if __name__ == "__main__":
    gui = GUI_grbl()
    gui.mainloop()