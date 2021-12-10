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
from PIL import Image, ImageTk
from tkinter import filedialog
#thu vien minh define
import customlog.cstLog as log
import func.HandlesString as Handles
import func.PortGRBL as PortGRBL
import func.wrFile as hFile
import func.mqtt as mqtt

mqttIPadd="broker.hivemq.com"
#mqttIPadd="127.0.0.1"
mqttPort=1883

file_path = 'data.txt'
log.SetLogMode("INFO")
# log.SetLogMode("DEBUG")

class GUI_grbl(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Controler GRBL - VIMESLAB")
		self.geometry('1250x650')
		self['bg'] = '#0099FF'
		#self['bg'] = '#3366CC'

		# LOGO IMAGE
		self.logoVimes_img = Image.open("logoVimes.png")
		self.logoVimes = ImageTk.PhotoImage(self.logoVimes_img)
		self.label_logoVimes = tk.Label(self,image = self.logoVimes,bg = '#0099FF')
		self.label_logoVimes.place(x=0,y=0)

		self.logoGrbl_img = Image.open("logoGRBL.png")
		self.logoGrbl = ImageTk.PhotoImage(self.logoGrbl_img)
		self.label_logoGrbl = tk.Label(self,image = self.logoGrbl,bg = '#0099FF')
		self.label_logoGrbl.place(x=1156,y=0)

		self.logo_start_img = Image.open("startBtn.png")
		self.logo_start = ImageTk.PhotoImage(self.logo_start_img)

		self.logo_pause_img = Image.open("pauseBtn.png")
		self.logo_pause = ImageTk.PhotoImage(self.logo_pause_img)

		self.logo_stop_img = Image.open("stopBtn.png")
		self.logo_stop = ImageTk.PhotoImage(self.logo_stop_img)

		self.logo_port_img = Image.open("portBtn.png")
		self.logo_port = ImageTk.PhotoImage(self.logo_port_img)

		self.logo_opc_img = Image.open("OPCUA.png")
		self.logo_opc = ImageTk.PhotoImage(self.logo_opc_img)

		self.firstName = tk.Label(self,text = 'VIMESLAB - Controller',font = ('candara', 40, 'bold'),bg = '#0099FF',fg = '#FFCC00')
		self.firstName.pack()

		self.language_text = tk.Label(self,text = 'Language:',font = ('arial', 10),bg = '#0099FF')
		self.language_text.place(x=100,y=73)

		self.VN_img = Image.open("vietnam.png")
		self.VN = ImageTk.PhotoImage(self.VN_img)
		self.label_VN = tk.Button(self,image = self.VN,bg = '#0099FF',width=22,height=16,command = lambda: self.handles.VietNamLanguage())
		self.label_VN.place(x=175,y=70)

		self.E_img = Image.open("english.png")
		self.E = ImageTk.PhotoImage(self.E_img)
		self.label_E = tk.Button(self,image = self.E,bg = '#0099FF',width=22,height=16,command = lambda: self.handles.EnglishLanguage())
		self.label_E.place(x=205,y=70)

		self.opc_data_text = tk.Label(self,text = 'OpcUA Data:',font = ('arial', 15), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_data_text.place(x = 1100,y=120)

		self.opc_x_text = tk.Label(self,text = 'X:',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_x_text.place(x = 1120,y=160)
		self.opc_x_ = tk.Label(self,text = '0',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_x_.place(x = 1160,y=160)


		self.opc_y_text = tk.Label(self,text = 'Y:',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_y_text.place(x = 1120,y=190)
		self.opc_y_ = tk.Label(self,text = '0',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_y_.place(x = 1160,y=190)

		self.opc_z_text = tk.Label(self,text = 'Z:',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_z_text.place(x = 1120,y=220)
		self.opc_z_ = tk.Label(self,text = '0',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_z_.place(x = 1160,y=220)

		self.opc_Vx_text = tk.Label(self,text = 'V_x:',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_Vx_text.place(x = 1120,y=250)
		self.opc_Vx_ = tk.Label(self,text = '0',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_Vx_.place(x = 1160,y=250)

		self.opc_Vy_text = tk.Label(self,text = 'V_y:',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_Vy_text.place(x = 1120,y=280)
		self.opc_Vy_ = tk.Label(self,text = '0',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_Vy_.place(x = 1160,y=280)

		self.opc_Vz_text = tk.Label(self,text = 'V_z:',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_Vz_text.place(x = 1120,y=310)
		self.opc_Vz_ = tk.Label(self,text = '0',font = ('arial', 10), bg= '#0099FF',fg = '#FFFFCC')
		self.opc_Vz_.place(x = 1160,y=310)

		# self.time_date = tk.Label(self,text = 'time - date',font = ('calibri', 10),bg = '#0099FF')
		# self.time_date.pack()
		# self.after(100, lambda: self.handles.th_update_time())


		# CHON PORT CONNECT GRBL
		#self.Port = tk.Button(self,text = 'PORT',width = 10,height=1,command = lambda: self.handles.connect_grbl(self.Port_entry.get()))
		self.Port = tk.Button(self,image=self.logo_port,width=70,command = lambda: self.handles.connect_grbl(self.Port_entry.get()))
		self.Port.place(x=25, y = 400)
		self.Port_entry = tk.Entry(self,font = ('calibri', 15),width = 10)
		self.Port_entry.place(x=115,y=400)

		# CHON FILE G-CODE
		self.File = tk.Button(self,text = 'FILE',bg='#FFFFFF',width = 10,height=1, command = lambda: self.handles.browseFiles())
		self.File.place(x=25, y = 520)
		self.File_entry = tk.Entry(self,font = ('calibri', 15),width = 17)
		self.File_entry.place(x=115,y=520)

		# THONG TIN TOA DO, FEEDRATE, SPEED
		self.text_xyz = tk.Label(self,text='--------------- Position ---------------',font = ('arial', 10), bg= '#0099FF',fg='#444444')
		self.text_xyz.place(x=600,y=370)

		self.X = tk.Label(self,text='X:',font= ('arial', 15),bg = '#0099FF')
		self.X.place(x=490,y=400)
		self.X_real = tk.Label(self,text='000.000',font= ('arial', 16),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.X_real.place(x=539,y=400)
		self.X_goc = tk.Label(self,text='001.000',font= ('arial', 13),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.X_goc.place(x=670,y=405)

		self.Y = tk.Label(self,text='Y:',font= ('arial', 15),bg = '#0099FF')
		self.Y.place(x=490,y=445)
		self.Y_real = tk.Label(self,text='000.000',font= ('arial', 16),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Y_real.place(x=539,y=445)
		self.Y_goc = tk.Label(self,text='001.000',font= ('arial', 13),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Y_goc.place(x=670,y=450)

		self.Z = tk.Label(self,text='Z:',font= ('arial', 15),bg = '#0099FF')
		self.Z.place(x=490,y=490)
		self.Z_real = tk.Label(self,text='000.000',font= ('arial', 16),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Z_real.place(x=539,y=490)
		self.Z_goc = tk.Label(self,text='001.000',font= ('arial', 13),width=10,borderwidth=2,relief='solid',fg='#444444',anchor ='w',justify = 'left')
		self.Z_goc.place(x=670,y=495)

		self.feedrate_text = tk.Label(self,text = 'Feed rate:',font = ('arial', 11), bg= '#0099FF')
		self.feedrate_text.place(x=800,y=430)
		self.feedrate_view = tk.Label(self,text = '0',font = ('arial', 11), bg= '#0099FF')
		self.feedrate_view.place(x=880,y=430)

		self.speed_text = tk.Label(self,text = 'Speed:',font = ('arial', 11), bg= '#0099FF')
		self.speed_text.place(x=800,y=480)
		self.speed_view = tk.Label(self,text = '0',font = ('arial', 11), bg= '#0099FF')
		self.speed_view.place(x=880,y=480)



		# NUT DIEU KHIEN
		self.text_control = tk.Label(self,text='---------------------------- Control --------------------------',font = ('arial', 10), bg= '#0099FF',fg='#444444')
		self.text_control.place(x=950,y=370)

		self.start = tk.Button(self,image = self.logo_start,bg='#0099FF',command = lambda: self.handles.button_start())
		self.start.place(x=970,y=400)

		self.pause = tk.Button(self,image = self.logo_pause,bg='#0099FF',command = lambda: self.handles.pause_button())
		self.pause.place(x=1060,y=400)

		self.stop = tk.Button(self,image = self.logo_stop,bg='#0099FF',command = lambda: self.handles.stop_button())
		self.stop.place(x=1150,y=400)

		self.text_line = tk.Label(self,text='-------------------------------------------------------------------',font = ('arial', 10), bg= '#0099FF',fg='#444444')
		self.text_line.place(x=950,y=455)

		#self.opcUA = tk.Button(self,text='Start OPC UA Server',font = ('arial', 15),width=28,height=1,command = lambda: self.handles.OpenOPC_UA_server())
		self.opcUA = tk.Button(self,image = self.logo_opc,bg='#EE0000',width =100,height=100,command = lambda: self.handles.OpenOPC_UA_server())
		self.opcUA.place(x=300,y=400)
		self.MQTT = tk.Button(self,text='MQTT',bg='#EE0000',width =14,height=2,command = lambda: self.handles.btn_MQTT())
		self.MQTT.place(x=300,y=510)

		self.X_plus = tk.Button(self,text='X+',width=6,height=2, command =lambda: self.handles.x_plus(self.unit_x.get()))
		self.X_plus.place(x=970,y=480)
		self.X_sub = tk.Button(self,text='X-',width=6,height=2, command = lambda: self.handles.x_sub(self.unit_x.get()))
		self.X_sub.place(x=970,y=580)
		self.unit_x = tk.Entry(self,font = ('arial', 12),width=5)
		self.unit_x.place(x=970,y=540)

		self.Y_plus = tk.Button(self,text='Y+',width=6,height=2, command =lambda: self.handles.y_plus(self.unit_y.get()))
		self.Y_plus.place(x=1060,y=480)
		self.Y_sub = tk.Button(self,text='Y-',width=6,height=2, command =lambda: self.handles.y_sub(self.unit_y.get()))
		self.Y_sub.place(x=1060,y=580)
		self.unit_y = tk.Entry(self,font = ('arial', 12),width=5)
		self.unit_y.place(x=1060,y=540)

		self.Z_plus = tk.Button(self,text='Z+',width=6,height=2, command =lambda: self.handles.z_plus(self.unit_z.get()))
		self.Z_plus.place(x=1150,y=480)
		self.Z_sub = tk.Button(self,text='Z-',width=6,height=2, command =lambda: self.handles.z_sub(self.unit_z.get()))
		self.Z_sub.place(x=1150,y=580)
		self.unit_z = tk.Entry(self,font = ('arial', 12),width=5)
		self.unit_z.place(x=1150,y=540)

		self.return_ = tk.Button(self,text='Return to 0',font = ('arial', 12),width=15,height=1, command = lambda: self.handles.return_0_button())
		self.return_.place(x=750,y=560)

		self.reset2zezo = tk.Button(self,text='Reset zezo',font = ('arial', 12),width=15,height=1,bg='#FF66CC', command = lambda: self.handles.reset2zezo())
		self.reset2zezo.place(x=550,y=560)

		# GUI COMMAND TRUC TIEP CHO GRBL
		self.text_command = tk.Label(self,text='minh',font = ('arial', 10),width=48,height=15,relief='solid',borderwidth=1,anchor ='sw', justify = 'left')
		self.text_command.place(x=25,y=120)

		self.graphic_test = tk.Label(self,font = ('arial', 10),width=70,height=15,relief='solid',borderwidth=1,anchor ='sw', justify = 'left')
		self.graphic_test.place(x=490,y=120)

		self.command_entry = tk.Entry(self,font = ('arial', 15),width=15)
		self.command_entry.place(x=115,y=467)
		self.send_command = tk.Button(self,text='Send',bg='#FFFFFF',width=10,command = lambda: self.handles.send_script2grbl_and_get_reponse(self.command_entry.get()))
		self.send_command.place(x=25,y=467)

		self.status = tk.Label(self,text = 'status',bg='#0099FF',font = ('arial', 11))
		self.status.place(x=25,y=570)


		self.handles = handles(self)
		log.LogInfo('//////////////////////   GUI IS ALREADY!!!   /////////////////////////')

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
		#
		# gia tri realtime vi tri toa do x y z fr theo goc may
		self.x = 0
		self.y = 0
		self.z = 0
		self.fr = 0
		self.sp = 0
		#
		# du lieu gui den OPC UA 
		self.x_opc=0
		self.y_opc=0
		self.z_opc=0
		self.frx_opc=100
		self.fry_opc=100
		self.frz_opc=100
		#
		# toa do goc phoi so voi goc may
		self.delta_x = 0
		self.delta_y = 0 
		self.delta_z = 0 

		#toa do theo goc phoi
		self.x_phoi = 0
		self.y_phoi = 0
		self.z_phoi = 0

		self.gobal_pause = 0

		# file
		self.line_n = 0
		self.run_in_file = 0
		# mqtt
		self.OpenMQTT_flag = 0
		self.MQTT_msg = ''

	def OpenOPC_UA_server(self):  
		th_opc = threading.Thread(target=self.OpenOPC_UA_server_())
		th_opc.start()
	def OpenOPC_UA_server_(self): # mở server opcUA
		log.LogInfo('MAIN:    Create OPC UA Server')
		self.server = Server()

		self.url = "opc.tcp://127.0.0.1:4840"
		self.server.set_endpoint(self.url)
		log.LogInfo('OPC IP:  opc.tcp://127.0.0.1')
		log.LogInfo('OPC PORT: 4840')

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
		log.LogInfo('OPC:    TAG - axis X, axis Y, axis Z, feed rate X, feed rate Y, feed rate Z')

		self.x_send2opc.set_writable()
		self.y_send2opc.set_writable()
		self.z_send2opc.set_writable()
		self.frx_send2opc.set_writable()
		self.fry_send2opc.set_writable()
		self.frz_send2opc.set_writable()

		self.server.start()
		log.LogInfo('MAIN:    OPC UA is started')
		self.gui.opcUA['bg'] = '#00FFFF'
		self.gui.status['text'] = self.gui.status['text'] + 'OPC UA Server is started (opc.tcp://127.0.0.1:4840)\n'

	def DisplayOpcData(self,x,y,z,frx,fry,frz): # hiển thị những dữ liệu được gửi lên OPC UA
		self.gui.opc_x_['text'] = str(x)
		self.gui.opc_y_['text'] = str(y)
		self.gui.opc_z_['text'] = str(z)
		self.gui.opc_Vx_['text'] = str(frx)
		self.gui.opc_Vy_['text'] = str(fry)
		self.gui.opc_Vz_['text'] = str(frz)

	def send2OPC(self,x,y,z,frx,fry,frz): # gửi dữ liệu lên opc server 
		if self.gui.opcUA['bg'] == '#00FFFF':
			self.x_send2opc.set_value(x)
			self.y_send2opc.set_value(y)
			self.z_send2opc.set_value(z)
			self.frx_send2opc.set_value(frx)
			self.fry_send2opc.set_value(fry)
			self.frz_send2opc.set_value(frz)
			
			# self.gui.text_command['text'] = 'OPC DATA: (x, y, z) = '+'('+str(x)+', '+str(y)+', '+str(z) +')'
			# self.gui.text_command['text'] = self.gui.text_command['text'] + '\nOPC DATA: (frx, fry, frz) = '+'('+str(frx)+', '+str(fry)+', '+str(frz)+')'
			# o
			#hFile.WriteGRBL(file_path, x, y, z,self.fr,frx,fry,frz)

			#mqtt.SendGRBLdataMQTT(self.mqtt,file_path)

			#mqtt.SendGRBLdataMQTT_ko_file(self.mqtt, x, y, z,self.fr,frx,fry,frz)  #mqtt
			self.DisplayOpcData(x,y,z,frx,fry,frz)
		else:
			log.LogInfo('OPC  : OPC UA server is not started!!!!')
			self.gui.notification("Chú ý!!!",'OPC UA server is not started!\n')

	def connect_grbl(self,ip): 				# connect đến ARDUINO qua cổng COM
		th_port = threading.Thread(target=self.connect_grbl_(ip))
		th_port.start()
	def connect_grbl_(self,inputPORT):		# connect đến ARDUINO qua cổng COM
		log.LogInfo('MAIN:    Connect to port ' + inputPORT)
		self.com2grbl = serial.Serial(inputPORT,115200,timeout = 1)
		log.LogInfo('MAIN:    Done connect port '+inputPORT )
		log.LogInfo('MAIN:    Baulrate: 115200 ')

		self.gui.Port['bg'] = '#00FFFF'
		self.gui.status['text'] = self.gui.status['text'] + 'Connect to GRBL is successfully\n'

		log.LogInfo('MAIN:    Send first script to start GRBL')
		self.com2grbl.write('\r'.encode('ASCII'))
		data = self.com2grbl.read_until()
		data = self.com2grbl.read_until()
		log.LogInfo('GRBL:    '+data.decode('ASCII'))
		self.gui.text_command['text'] = data.decode('ASCII')

		log.LogInfo('MAIN:    Run to function - get real time x,y,z,fr')
		self.get_reponse_xyz()
		log.LogInfo('MAIN:    Done handles PORT button')

	def get_file_gcode(self,file_path):   
		log.LogInfo('MAIN:    FILE PATH')
		if file_path == '':
			self.gui.notification("Chú ý!!!",'Nhập đường dẫn đến file Gcode\n')
			log.LogInfo('MAIN: "Chú ý!!! Nhập đường dẫn đến file Gcode')
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
		t2 = threading.Thread(target=self.send_script2grbl_and_get_reponse_(script,0))
		t2.start()
	def send_script2grbl_and_get_reponse_(self,script,mode):		# gửi lệnh gcode cho arduino 
		try:
			# self.com2grbl.write(bytes(script+"\r", encoding='ascii'))
			PortGRBL.SendScriptToGRBL(self.com2grbl,script)
			#print("send ok")
			if mode ==0:	# mode 0: mode xử lý các gcode gửi bằng script entry
				(g, x_opc, y_opc, z_opc) = Handles.HandlesGcodeLine(script)
				if x_opc != 10071999:
					self.x_opc = x_opc
				if y_opc != 10071999:
					self.y_opc = y_opc
				if z_opc != 10071999:
					self.z_opc = z_opc
				#self.send2OPC(self.x_opc+self.delta_x , self.y_opc+self.delta_y, self.z_opc+self.delta_z, self.frx_opc, self.fry_opc, self.frz_opc)
				#print("send OPC ok")
				self.gui.command_entry.delete(0,'end')
			# elif mode ==1:		# mode 1: mode xử lý các btn x+, x-,....
				#self.send2OPC(self.x_opc+self.delta_x , self.y_opc+self.delta_y, self.z_opc+self.delta_z, self.frx_opc, self.fry_opc, self.frz_opc)
			log.LogInfo('MAIN:    Send to grbl: '+script)
		except:
			log.LogInfo('MAIN:   FAIL to send script')
	# lay vi tri x, y, z, feed rate hien thi len HMI, ko xu ly phan gui qua OPC
	def get_reponse_xyz(self):
		t1 = threading.Thread(target=self.get_reponse_xyz_thread)
		t1.start()
	def get_reponse_xyz_thread(self):			# lấy dữ liệu gửi về từ arduino
		x = 0
		y = 0
		z = 0
		fr = 0
		sp = 0
		del_x = 0
		del_y = 0
		del_z = 0
		self.send2OPC(0,0,0,100,100,100)		# gui du lieu cho opc lan dau tien
		self.com2grbl.write('?'.encode('ASCII'))
		data = self.com2grbl.read_until()			# đọc dữ liệu từ cổng COM
		a = data.decode('ASCII')
		(self.x, self.y, self.z, self.fr, self.delta_x, self.delta_y, self.delta_z) = Handles.HandlesResponseGRBL(a)
		print('ok')
		self.x_opc = -self.delta_x
		self.y_opc = -self.delta_y
		self.z_opc = -self.delta_z
		while True:
			try:
				self.com2grbl.write('?'.encode('ASCII'))
				data = self.com2grbl.read_until()			# đọc dữ liệu từ cổng COM
				a = data.decode('ASCII')
				#log.LogInfo(a)
				#hFile.WriteFileContinue("log.txt",a)
				(x, y, z, fr, del_x, del_y, del_z) = Handles.HandlesResponseGRBL(a)
				# log.LogInfo(str(x)+" : "+str(y)+" : "+str(z)+"feed rate : "+str(fr)+" : "+str(del_x)+" : "+str(del_y)+" : "+str(del_z))	# xử lý dữ liệu từ arduino

				if x != -100000000 and y != -100000000 and z != -100000000:
					self.x = x
					self.y = y
					self.z = z
					self.fr=fr
					#self.sp = sp
				if del_x != -100000000:
					self.delta_x = del_x
					self.delta_y = del_y 
					self.delta_z = del_z

				if self.x != -100000000:
					self.view_xyz(self.x,self.y,self.z,self.fr,self.delta_x, self.delta_y, self.delta_z)	
					self.x_phoi = self.x - self.delta_x	# toa do goc may
					self.y_phoi = self.y - self.delta_y
					self.z_phoi = self.z - self.delta_z
				elif self.x == -100000000:
					self.view_xyz(self.x, self.y, self.z,0,self.delta_x, self.delta_y, self.delta_z)
				# log.LogInfo('Xu ly feedrate - 1')
				(self.frx_opc,self.fry_opc,self.frz_opc) = Handles.CalculatorFr(self.x_phoi, self.y_phoi, self.z_phoi, self.x_opc, self.y_opc, self.z_opc, self.fr)
				# log.LogInfo('Xu ly feedrate')
				# dữ liệu gửi sang opc phải là gốc theo gốc máy, nhưng self.x_opc,.. đang theo gốc phôi nên ta cong them delta
				self.send2OPC(self.x_opc+self.delta_x , self.y_opc+self.delta_y, self.z_opc+self.delta_z, self.frx_opc, self.fry_opc, self.frz_opc) 

				if self.run_in_file==1:
					if self.x_opc + self.delta_x == self.x and self.y_opc + self.delta_y == self.y and self.z_opc + self.delta_z == self.z:
						print('DK xu ly file dung')
						self.line_n = self.line_n+1
						self.control_gcode_file(self.line_n)
					else:
						log.LogInfo("Test chay băng file loi")
			except:
				log.LogDebug('THREAD 1 :Cannot get data with format, no display')
				continue
		log.LogInfo('THREAD 1 :ERROR - OUT MAINLOOP')

	# in gia tri ra GUI
	def view_xyz(self,x,y,z,fr,del_x,del_y,del_z):
		self.gui.X_real['text'] = str(x-del_x)
		self.gui.Y_real['text'] = str(y-del_y)
		self.gui.Z_real['text'] = str(z-del_z)
		self.gui.X_goc['text'] = str(x)
		self.gui.Y_goc['text'] = str(y)
		self.gui.Z_goc['text'] = str(z)
		self.gui.feedrate_view['text'] = str(fr)
		
		# self.gui.X_goc['text'] = str(x)

	def browseFiles(self):
		filename = filedialog.askopenfilename(initialdir = "./",
											title = "G-code file",
											filetypes = (("Text files",
															"*.*"),
														("all files",
															"*.*")))

		self.file_gcode = filename
		if self.file_gcode =='':
			self.gui.notification('Note!','No File')
			self.gui.File.configure(bg='#FFFFFF')
			self.gui.text_command.configure(text='')
		else:
			self.gui.notification('Note!','File: '+self.file_gcode)
			log.LogInfo(self.file_gcode)
			self.gui.File.configure(bg='#00FFCC')
			self.gui.text_command.configure(text=hFile.ReadGRBL(self.file_gcode))

	def button_start(self):
		# t2 = threading.Thread(target=self.control_gcode_file)
		# t2.start()
		self.run_in_file = 1
		self.line_n = 1
		self.control_gcode_file(self.line_n)

	def control_gcode_file(self,n):
		gcode_line = hFile.ReadLine_n(self.file_gcode,n)
		if gcode_line == '':
			self.run_in_file=0
			log.LogInfo("End File")
		else:
			self.send_script2grbl_and_get_reponse_(gcode_line,0)

	def x_plus(self,ip):
		thread_unit = threading.Thread(target=self.x_plus_(ip))
		thread_unit.start()
	def x_plus_(self,ip):
		script = '$J=G21G91 X' + ip + ' F25'
		#self.send2OPC(self.x+int(ip), self.y, self.z, 25, 0, 0)
		self.x_opc=self.x_opc+float(ip)
		self.send_script2grbl_and_get_reponse_(script,1)

	def x_sub(self,ip):
		thread_unit = threading.Thread(target=self.x_sub_(ip))
		thread_unit.start()
	def x_sub_(self,ip):
		script = '$J=G21G91 X-' + ip +  'F25'
		#self.send2OPC(self.x-int(ip), self.y, self.z, 25, 0, 0)
		self.x_opc=self.x_opc-float(ip)
		self.send_script2grbl_and_get_reponse_(script,1)

	def y_plus(self,ip):
		thread_unit = threading.Thread(target=self.y_plus_(ip))
		thread_unit.start()
	def y_plus_(self,ip):
		script = '$J=G21G91 Y' + ip + 'F25'
		# self.send2OPC(self.x, self.y+int(ip), self.z, 0, 25, 0)
		self.y_opc=self.y_opc+float(ip)
		self.send_script2grbl_and_get_reponse_(script,1)

	def y_sub(self,ip):
		thread_unit = threading.Thread(target=self.y_sub_(ip))
		thread_unit.start()
	def y_sub_(self,ip):
		script = '$J=G21G91Y-' + ip + 'F25'
		# self.send2OPC(self.x, self.y-int(ip), self.z, 0, 25, 0)
		self.y_opc=self.y_opc-float(ip)
		self.send_script2grbl_and_get_reponse_(script,1)

	def z_plus(self,ip):
		thread_unit = threading.Thread(target=self.z_plus_(ip))
		thread_unit.start()
	def z_plus_(self,ip):
		script = '$J=G21G91Z' + ip + 'F25'
		# self.send2OPC(self.x, self.y, self.z+int(ip), 0, 0, 25)
		self.z_opc=self.z_opc+float(ip)
		self.send_script2grbl_and_get_reponse_(script,1)

	def z_sub(self,ip):
		thread_unit = threading.Thread(target=self.z_sub_(ip))
		thread_unit.start()
	def z_sub_(self,ip):
		script = '$J=G21G91Z-' + ip + 'F25'
		# self.send2OPC(self.x, self.y, self.z-int(ip), 0, 0, 25)
		self.z_opc=self.z_opc-float(ip)
		self.send_script2grbl_and_get_reponse_(script,1)

	def return_0_button(self):
		t2 = threading.Thread(target=self.return_0_button_())
		t2.start()
	def return_0_button_(self):
		self.send_script2grbl_and_get_reponse_('G21G90 G0Z5 \nG90 G0 X0 Y0 \nG90 G0 Z0',1)

	def pause_button(self):
		t2 = threading.Thread(target=self.pause_button_())
		t2.start()

	def pause_button_(self):
		if self.gobal_pause == 0:	
			self.send_script2grbl_and_get_reponse_('!',1)
			self.gobal_pause = 1
		else:
			self.send_script2grbl_and_get_reponse_('~',1)
			self.gobal_pause = 0

	def stop_button(self):
		self.send_script2grbl_and_get_reponse_('$$',1)
    		
	def reset2zezo(self):
		t_zezo = threading.Thread(target=self.reset2zezo_())
		t_zezo.start()
	def reset2zezo_(self):
		self.send_script2grbl_and_get_reponse_('G10 P0 L20 X0 Y0 Z0',1)

	# mqtt server
	def on_message(self,client, userdata, message):
		data = message.payload.decode('ASCII')
		self.MQTT_msg = data
		#print(self.MQTT_msg)
		self.send_script2grbl_and_get_reponse_(self.MQTT_msg,0)
		return data

	def btn_MQTT(self):
		mqtt_th = threading.Thread(target=self.OpenMQTT())
		mqtt_th.start()
	def OpenMQTT(self):
		self.mqtt = mqtt.CreateClientMQTT(mqttIPadd, mqttPort, mqtt.on_connect, self.on_message) #mqtt
		self.OpenMQTT_flag = 1
		self.gui.MQTT.configure(bg='#00FFFF')
		
	#chuyen ngon ngu
	def VietNamLanguage(self):
		self.gui.send_command['text'] = 'Gửi'
		self.gui.reset2zezo['text'] = 'Đặt gốc phôi'
		self.gui.return_['text'] = 'Về gốc phôi'
		self.gui.text_xyz['text'] = '--------------- Vị Trí ---------------'
		self.gui.text_control['text'] = "---------------------------- Điều Khiển --------------------------"
		self.gui.feedrate_text['text'] = "Chạy dao:"
		self.gui.speed_text['text'] = 'Trục Chính:'
		self.gui.language_text['text'] = 'Ngôn ngữ:'
		self.gui.opc_data_text['text'] = 'Dữ liệu OpcUA'

	def EnglishLanguage(self):
		self.gui.send_command['text'] = 'Send'
		self.gui.reset2zezo['text'] = 'Reset zezo'
		self.gui.return_['text'] = 'Return to 0'
		self.gui.text_xyz['text'] = '--------------- Position ---------------'
		self.gui.text_control['text'] = "---------------------------- Control --------------------------"
		self.gui.feedrate_text['text'] = "Feed rate:"
		self.gui.speed_text['text'] = 'Speed:'
		self.gui.language_text['text'] = 'Language:'
		self.gui.opc_data_text['text'] = 'OpcUA Data'


if __name__ == "__main__":
    gui = GUI_grbl()
    gui.mainloop()