import customlog.cstLog as log
def SendScriptToGRBL(port, script):
	try:
		port.write(bytes(script+"\r", encoding='ascii'))
	except:
		log.LogInfo("Can not send script")