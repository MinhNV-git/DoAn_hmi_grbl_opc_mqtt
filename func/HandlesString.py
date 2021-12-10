import customlog.cstLog as log
import math
# Xu ly phan hoi nhan tu GRBL, lọc lấy dữ liệu: vị trí x, y, z(tương đối và tuyệt đối), feed rate
def HandlesResponseGRBL(a):		# xử lý dữ liệu từ arduino
		x_rt = ''
		y_rt = ''
		z_rt = ''
		feed_rate = ''
		speed = ''
		delta_x = '-100000000'
		delta_y = '-100000000'
		delta_z = '-100000000'
		flag = 0
		#log.LogInfo(a)
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
			log.LogDebug('THREAD 1:  du lieu loi, khong theo format')
			return (float(-100000000),float(-100000000),float(-100000000),float(-100000000), float(-100000000),float(-100000000),float(-100000000))#, float(-100000000),float(-100000000),float(-100000000)		

def HandlesResponseGRBL_new(a): ### ko the su dung ###
	try:
		x = 0
		y = 0
		z = 0
		fr = 0
		sp = 0
		del_x = -100000000
		del_y = -100000000
		del_z = -100000000
		a = a.strip('<>\r\n')
		# print(a)
		a = a.split('|')
		n= len(a)
		# print(n)
		if n>2:
			xyz_ = a[1].split(':')
			# print(xyz_)
			xyz = xyz_[1].split(',')
			# print(xyz)
			frandsp_ = a[2].split(':')
			# print(frandsp_)
			frandsp = frandsp_[1].split(',')
			# print(frandsp)
			fr = float(frandsp[0])
			sp = float(frandsp[1])
			x = float(xyz[0])
			y = float(xyz[1])
			z = float(xyz[2])
			# print(str(x)+' '+str(y)+' '+str(z)+' '+str(fr)+' '+str(sp)+"->goc-phoi: "+str(del_x)+' '+str(del_y)+' '+str(del_z))
	except:
		log.LogInfo('OK')	

	
	if n == 4:
		delta_ = a[3].split(':')
		if delta_[0] == 'WCO':
			delta = delta_[1].split(',')
			del_x=delta[0]
			del_y=delta[1]
			del_z=delta[2]
			#print("goc-phoi: "+str(del_x)+' '+str(del_y)+' '+str(del_z))

	return (x,y,z,fr,sp,del_x,del_y,del_z)
		

# xử lý từng dòng Gcode trong file Gcode
def HandlesGcodeLine(script_line):
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
		print(str_X)
		print(str_Y)
		print(str_Z)
		return (float(str_G), float(str_X), float(str_Y), float(str_Z))

def CalculatorFr(x_old, y_old, z_old, x_opc, y_opc, z_opc, fr):
	dx = x_opc - x_old
	dy = y_opc - y_old
	dz = z_opc - z_old

	tong = math.sqrt(dx*dx + dy*dy + dz*dz)
	if tong != 0:
		ratio = fr/tong

		frx = abs(dx)*ratio
		fry = abs(dy)*ratio
		frz = abs(dz)*ratio
	else:
		frx = 0
		fry = 0 
		frz = 0

	return (frx,fry,frz)	
    	
    
