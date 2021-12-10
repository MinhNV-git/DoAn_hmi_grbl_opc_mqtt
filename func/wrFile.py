import customlog.cstLog as log

def WriteFileContinue(file, data):
    with open(file,'a') as f:
        f.write(data)
    f.close()
    log.LogInfo("Write in: "+file)

def WriteFileReplace(file, data):
    with open(file,'w') as f:
        f.write(data + "\n")
    f.close()
    log.LogDebug("Write in: "+file)

def WriteGRBL(file, x, y, z, fr, frx, fry, frz):
    data = str(x)+", "+str(y)+", "+str(z)+", "+str(fr)+", "+str(frx)+", "+str(fry)+", "+str(frz)
    WriteFileReplace(file, data)
    
def ReadGRBL(file):
    with open(file,'r') as f:
        data = f.read()
    f.close()
    return data

def ReadLine_n(file_path,n): # đọc dòng gcode từ file Gcode
    file_open = open(file_path,'r')
    for i in range(n):
        str_ = file_open.readline()
    file_open.close()
    return str_

