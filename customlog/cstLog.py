import datetime

LOGMODE = "info"

def SetLogMode(text):
	if text == "INFO":
		LOGMODE = "info"
	elif text == "DEBUG":
		LOGMODE =  "debug"
	else:
		LOGMODE = '0'

def LogInfo(text):
	time = str(datetime.datetime.now().time())
	if(LOGMODE=="info" or LOGMODE == "debug"):
		print('['+time+']: '+text)

def LogDebug(text):
	time = datetime.datetime.now().time()
	if LOGMODE=="debug":
		print('['+time+']: '+text)

