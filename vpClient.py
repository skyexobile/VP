import serial, datetime, time, re, pickle, os, select, sys, csv
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk
from tkinter import*
import csv


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8000


uname = str(sys.argv[2])

ip = str(sys.argv[1])
s.connect((ip, port))
s.send(uname.encode('ascii'))

print("Connecting to Touch Input")
input_serial = serial.Serial('/dev/cu.usbmodem1421')
input_serial.setBaudrate(115200)
input_serial.setDTR(False)
input_serial.setRTS(False)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)

output_serial.setDTR(False)
output_serial.setRTS(False)



print("Connected!")
soft_value = 100
medium_value = 500
hard_value = 1000
root = tk.Tk()
acquired_flag = False
previous_read = -100
offset = 0
def reset():
    global offset
    input_serial.write(str("0").encode())
    offset = 0
    print("Reset Complete")
def set_soft():
    print('Please provide three 2-second soft squeezes')
    global offset
    value_list = []
    max_list = []
    global soft_value
    counter = 0
    previous = -100
    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        #print(input_value)
        if input_value > 50:
            while (previous - input_value) < 20:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    new_input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    new_input_value = float(value) + offset
                #print(new_input_value)
                previous = input_value
                input_value = new_input_value
                #print(new_input_value)

            index = value_list.index(max(value_list))
            for i in range(0, index):
                max_list.append(value_list[i])
            counter = counter +1

            print("Trial " + str(counter) + " completed!")
            value = (input_serial.readline().decode())
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                input_value = float(value) + offset
            while (previous - input_value) >5:
                previous = input_value
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
        elif input_value < -3:
            offset = offset - input_value
    soft_value = sum(max_list)/len(max_list)
    print("Soft touches have been trained")
def set_medium():
    print('Please provide three 2-second medium squeezes')

    global offset
    value_list = []
    max_list = []
    global med_value
    counter = 0
    previous = -100
    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        #print(input_value)
        if input_value > 200:
            while (previous - input_value) < 30:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    new_input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    new_input_value = float(value) + offset
                #print(new_input_value)
                previous = input_value
                input_value = new_input_value

            index = value_list.index(max(value_list))
            for i in range(0, index):
                max_list.append(value_list[i])
            counter = counter +1
            print("Trial " + str(counter) + " completed!")
            value = (input_serial.readline().decode())
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                input_value = float(value) + offset
            while (previous - input_value) >5:
                previous = input_value
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
        elif input_value < -3:
            offset = offset - input_value
    med_value = sum(max_list)/len(max_list)
    print("Medium touches have been trained")
def set_hard():
    global offset, hard_value
    value_list = []
    max_list = []
    counter = 0
    previous = -10
    print('Please provide three 2-second hard squeezes')

    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        #print(input_value)
        if input_value > 400:
            while (previous - input_value) < 30:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    new_input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    new_input_value = float(value) + offset
                #print(new_input_value)
                previous = input_value
                input_value = new_input_value
            index = value_list.index(max(value_list))
            for i in range(0, index):
                max_list.append(value_list[i])
            counter = counter +1
            print("Trial " + str(counter) + " completed!")
            value = (input_serial.readline().decode())
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                input_value = float(value) + offset
            while (previous - input_value) >5:
                previous = input_value
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
        elif input_value < -3:
            offset = offset - input_value
    hard_value = sum(max_list)/len(max_list)
    print("Hard touches have been trained")
def save_settings():
    global soft_value, med_value, hard_value, PID_value, medium_value
    if soft_value > med_value:
        temp = soft_value
        soft_value = med_value
        med_value = temp
    if med_value > hard_value:
        temp = med_value
        med_value = hard_value
        hard_value = temp
    medium_value = med_value
    print("Your settings have been saved!")
    '''print("soft is ", soft_value)
    print("medium is ", medium_value)
    print("hard is ", hard_value)
    '''

reset_button =  tk.Button(root, text = "Reset Sensor", command = reset)
soft_button =  tk.Button(root, text = "Define Soft", command = set_soft)
medium_button =  tk.Button(root, text = "Define Medium", command = set_medium)
hard_button  =  tk.Button(root, text = "Define Hard", command = set_hard)
save_button  =  tk.Button(root, text = "Save Settings", command = save_settings)
playback_button  =  tk.Button(root, text = "Activate Device", command = generate)
sample_button= tk.Button(root, text = "Sample Squeezes", command = sample)

reset_button.pack(side = tk.BOTTOM)
soft_button.pack(side = tk.BOTTOM)
medium_button.pack(side = tk.BOTTOM)
hard_button.pack(side = tk.BOTTOM)
save_button.pack(side = tk.BOTTOM)
playback_button.pack()
sample_button.pack()

root.update()
def csv_writer(data, path):
    with open(path, "a", newline = '') as csv_file:
        #writer = csv.writer(csv_file, delimiter = ' ')
        csv_file.write(str(data) + '\n')
        csv_file.close()
    print('done')
clientRunning = True
#path = "DataFiles/" + str(subID)+ "/touch_data.csv"
#f = open(path,'a')
def receiveMsg(sock):
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            msg = sock.recv(1024).decode('ascii')
            print('messaged receive is ' +msg)
            #csv_writer(msg, path)
        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            serverDown = True

threading.Thread(target = receiveMsg, args = (s,)).start()
while clientRunning:
    tempMsg = input()
    msg = uname + '>>' + tempMsg
    if '**quit' in msg:
        clientRunning = False
        s.send('**quit'.encode('ascii'))
    else:
        s.send(msg.encode('ascii'))

    
