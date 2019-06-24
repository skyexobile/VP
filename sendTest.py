import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk
from tkinter import*
import csv

print("Connecting to Touch Input")
input_serial = serial.Serial('/dev/cu.usbmodem14101')
input_serial.baudrate =115200
input_serial.setDTR(False)
input_serial.setRTS(False)



print("Connected!")

#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))

soft_value = 100
medium_value = 500
hard_value = 1000
root = tk.Tk()
acquired_flag = False
previous_read = -100
offset = 0

while True:
    #root.update()
    # a.encode('utf-8').strip()
    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset

    if input_value <-3:
        offset = offset -input_value
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
    print(input_value)
