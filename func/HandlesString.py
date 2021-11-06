import customlog.cstLog as log
import math
# Xu ly phan hoi nhan tu GRBL, lọc lấy dữ liệu: vị trí x, y, z(tương đối và tuyệt đối), feed rate
## <Idle|MPos:100.000,100.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>
## <Idle|MPos:100.000,100.000,0.000|FS:0,0>
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
		log.LogDebug(a)
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

def OPCdataFromScript(x_opc,y_opc,z_opc,fr,script):
	v=-1
	(g_file, x_file, y_file, z_file) = HandlesGcodeLine(script)
	if x_file != x_opc and x_file != 10071999:
			x_old = x_opc
			x_opc = x_file
	if y_file != y_opc and y_file != 10071999:
		y_old = y_opc
		y_opc = y_file
	if z_file != z_opc and z_file != 10071999:
		z_old = z_opc
		z_opc = z_file

	if x_file == 10071999 and y_file ==10071999:
		v = 1           # z
	elif x_file ==10071999 and z_file ==10071999:
		v = 2            # y
	elif y_file ==10071999 and z_file ==10071999:
		v = 3            # x
	elif x_file == 10071999:
		v = 4           # yz
	elif y_file == 10071999:
		v = 5            # xz
	elif z_file == 10071999:
		v = 6           # xy
	
	# if fr_opc != fr:
	fr_opc = fr

	if v == 1:
		frx_opc = 0
		fry_opc = 0
		frz_opc = fr_opc
	elif v ==2:
		frx_opc = 0
		fry_opc = fr_opc
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

	return (float(x_opc), float(y_opc), float(z_opc), float(frx_opc), float(fry_opc), float(frz_opc))


def CalculatorFr(x_old, y_old, z_old, x_opc, y_opc, z_opc, fr):
	dx = x_opc - x_old
	dy = y_opc - y_old
	dz = z_opc - z_old

	tong = math.sqrt(dx*dx + dy*dy + dz*dz)

	ratio = fr/tong

	frx = abs(dx)*ratio
	fry = abs(dy)*ratio
	frz = abs(dz)*ratio

	return (frx,fry,frz)	
    	
    
