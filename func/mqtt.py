import paho.mqtt.client as mqttClient
import time
import os
import func.wrFile as hFile
import customlog.cstLog as log

MQTT_msg = ''
def CreateClientMQTT(IP, PORT, on_connect, on_message):
    broker_address= IP  #Broker address
    port = PORT                         #Broker port
    # user = "me"                    #Connection username
    # password = "abcdef"            #Connection password
    client = mqttClient.Client("Python_GRBL")               #create new instance
    client.on_connect= on_connect                      #attach function to callback
    client.on_message= on_message                      #attach function to callback
    client.connect(broker_address,port,60) #connect
    client.subscribe("/DoAn/CNC/data") #subscribe   
    client.loop_start() #then keep listening forever
    return client

def on_message(client, userdata, message):
    data = message.payload.decode('ASCII')
    print(data)
    return data

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        log.LogInfo("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        log.LogInfo("Connection failed")

def SendGRBLdataMQTT(client, file):
    data = hFile.ReadGRBL(file)
    #print("run in >>>>>>>>>>>>>>>>")
    client.publish("/DoAn/CNC/data",data,0)#publish

def SendGRBLdataMQTT_ko_file(client, x,y,z,fr,frx,fry,frz):
    data = "{"+str(x)+", "+str(y)+", "+str(z)+"}"+", "+str(fr)+", "+str(frx)+", "+str(fry)+", "+str(frz)
    client.publish("/DoAn/CNC/data",data,0,False)#publish