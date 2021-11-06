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
from PIL import Image, ImageTk

server = Server()

url = "opc.tcp://127.0.0.1:4840"
server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

x = Param.add_variable(addspace, "axis X", 0)
y = Param.add_variable(addspace, "axis Y", 0)
z = Param.add_variable(addspace, "axis Z", 0)

x.set_writable()
y.set_writable()
z.set_writable()

x.set_value(10.5)
server.start()
print("opc.tcp://127.0.0.1:4840")