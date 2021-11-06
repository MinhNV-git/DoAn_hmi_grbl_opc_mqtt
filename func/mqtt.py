import paho.mqtt.client as mqttClient
import time
import os
import func.wrFile as hFile

def CreateClientMQTT(IP, PORT):
    broker_address= IP  #Broker address
    port = PORT                         #Broker port
    # user = "me"                    #Connection username
    # password = "abcdef"            #Connection password
    client = mqttClient.Client("Python_Publish")               #create new instance
    # client.username_pw_set(user, password=password)    #set username and password
    # client.on_connect= on_connect                      #attach function to callback
    # client.on_message= on_message                      #attach function to callback
    client.connect(broker_address,port,60) #connect
    client.subscribe("/DoAn/CNC/data") #subscribe
    return client

def SendGRBLdataMQTT(client, file):
    data = hFile.ReadGRBL(file)
    client.publish("/DoAn/CNC/data",data)#publish

def SendGRBLdataMQTT_ko_file(client, x,y,z,fr,frx,fry,frz):
    data = "{"+str(x)+", "+str(y)+", "+str(z)+"}"+", "+str(fr)+", "+str(frx)+", "+str(fry)+", "+str(frz)
    client.publish("/DoAn/CNC/data",data)#publish