
import tkinter as tkin

import serial, datetime, time, re

import os, select, sys, csv, threading
from time import gmtime, strftime
import socket


import csv
from subprocess import Popen, PIPE


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8000

uname = 'PartnerA'

ip = str(sys.argv[1])
s.connect((ip, port))
s.send(uname.encode('ascii'))
print("Connecting to Touch Input")
input_serial = serial.Serial('/dev/cu.usbmodem14201')
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
root = tkin.Tk()
soft_flag = False
medium_flag = False
hard_flag = False
released_flag = False
previous_value = 0
offset = 0
touch_record = []
raw_send =[]
raw_receive = []
playing = False
sent_list=[]
final_count=0
recv_record = []
recording_time = time.time()
sent_dict = {}
sent_count=1
replay_count = 1
touch_tuple =[]
sent_record = []
videoRecording = False
sent_list=[]
recv_list= []
def record():
    global recording_time
    global videoRecording
    scpt = '''
    tell application "System Events"
    	keystroke "%" using command down
    	delay 1.0
    	keystroke return
    end tell'''


    args = ['2', '2']


    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(scpt)
    recording_time = float(time.time())
    #s.send('**time'.encode('ascii'))
    videoRecording = True
    print('recording time is ', recording_time)


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
    global medium_value
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
    medium_value = sum(max_list)/len(max_list)
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
    global soft_value, hard_value, PID_value, medium_value

    print("Your settings have been saved!")
    print("soft is ", soft_value)
    print("medium is ", medium_value)
    print("hard is ", hard_value)

def save_sent():
    global sent_list
    csv_writer(sent_list, 'sent_data.csv')
    print('done')
def save_recv():
    global recv_list
    csv_writer(recv_list, 'received_data.csv')
    print('done')
reset_button =  tkin.Button(root, text = "Reset Sensor", command = reset)
soft_button =  tkin.Button(root, text = "Define Soft", command = set_soft)
medium_button =  tkin.Button(root, text = "Define Medium", command = set_medium)
hard_button  =  tkin.Button(root, text = "Define Hard", command = set_hard)
save_button  =  tkin.Button(root, text = "Save Settings", command = save_settings)
#replay_instance = tkin.Button(root, text = "Instance Replay", command = replay)
record_video = tkin.Button(root, text = "Record", command = record)
save_sTouch = tkin.Button(root, text = 'Save Sent', command = save_sent)
save_rTouch = tkin.Button(root, text = 'Save Received', command = save_recv)
save_rTouch.pack()
record_video.pack()
#replay_instance.pack()
save_sTouch.pack()
reset_button.pack(side = tkin.BOTTOM)
soft_button.pack(side = tkin.BOTTOM)
medium_button.pack(side = tkin.BOTTOM)
hard_button.pack(side = tkin.BOTTOM)
save_button.pack(side = tkin.BOTTOM)

#root.update()
def csv_writer(data, path):
    with open(path, "a", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = '\n')
        writer.writerow(data)
        csv_file.close()
    print('done')
clientRunning = True
#path = "DataFiles/" + str(subID)+ "/touch_data.csv"
#f = open(path,'a')

def receiveMsg(sock):
    global recording_time, recv_list
    serverDown = False
    while clientRunning and (not serverDown):

        try:
            msg = sock.recv(1024).decode('ascii')
            if '**send' in msg:
                msg = msg[(msg.find('**send')+6):]
                received.append(msg)
                #print('this is the list: ',received)
            elif '**vtime' in msg:
                msg = msg[msg.find('**vtime')+8:]
                recording_time = float(msg) + 4
                #print('video recording time is ', recording_time)
            #csv_writer(msg, path)
            elif 'soft' in msg:
                #print("soft squeeze REceived")
                #output_serial.write(str('B').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)
                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord) + ',soft')
                #print("touch record is ", touch_record)
                touch_record.append(msg)
            elif 'medium' in msg:
                #print("medium squeeze Received")
                #output_serial.write(str('E').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)
                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord)+ ',medium')
                #print("touch record is ", touch_record)
                touch_record.append(msg)
            elif 'hard' in msg:
                #print("hardsqueeze received")
                #output_serial.write(str('H').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)
                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord)+ ',hard')
                touch_record.append(msg)
                #print("touch record is ", touch_record)
            elif 'release' in msg:
                #print("release received")
                #output_serial.write(str('H').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)
                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord)+ ',release')
                touch_record.append(msg)
                #print("touch record is ", touch_record)

        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            serverDown = True

threading.Thread(target = receiveMsg, args = (s,)).start()
tempMsg = ''
while clientRunning:
    root.update()
    #print('video recording is ', videoRecording)
    while videoRecording is True:
        root.update()
        value = (input_serial.readline().decode())
        input_value = float(value)
        if  abs(input_value) - abs(previous_value) >0:
            if input_value >= soft_value and input_value < medium_value:
                if soft_flag is False:
                    tempMsg = 'soft'
                    tempRecord = float(time.time())-(recording_time)
                    sent_list.append(str(tempRecord)+ ','+ tempMsg)
                    sent_count+=1
                    released_flag=False
                else:
                    tempMsg = ''
                soft_flag = True
                medium_flag = False
                hard_flag = False
            elif input_value >= medium_value and input_value < hard_value:
                if medium_flag is False:
                    tempMsg = 'medium'
                    tempRecord =  float(time.time())-(recording_time)
                    sent_list.append(str(tempRecord)+ ','+ tempMsg)
                    sent_count+=1
                    released_flag=False

                else: tempMsg = ''
                medium_flag = True
                soft_flag = False
                hard_flag = False
            elif input_value >= hard_value:
                if hard_flag is False:
                    tempMsg = 'hard'
                    tempRecord =  float(time.time())-(recording_time)
                    sent_list.append(str(tempRecord)+ ','+ tempMsg)

                    sent_count+=1
                    released_flag=False

                else:
                    tempMsg = ''
                hard_flag = True
                soft_flag = False
                medium_flag = False
            else:
                tempMsg = ''

        else:
            #check for if released
            if released_flag is False:
                if soft_flag is True:
                    if input_value < soft_value:
                        tempMsg = 'release'
                        tempRecord =  float(time.time())-(recording_time)
                        sent_list.append(str(tempRecord)+ ','+ tempMsg)

                        sent_count+=1
                        soft_flag=False
                        released_flag=True
                    else:

                        tempMsg = ''
                if medium_flag is True:
                    if input_value < medium_value:
                        tempMsg = 'release'
                        tempRecord = float(time.time())-(recording_time)
                        sent_list.append(str(tempRecord)+ ','+ tempMsg)

                        sent_count+=1
                        medium_flag=False
                        released_flag=True
                    else:
                        tempMsg = ''
                if hard_flag is True:
                    if input_value < hard_value:
                        hard_flag = False
                        tempMsg = 'release'
                        tempRecord = float(time.time())-(recording_time)
                        sent_list.append(str(tempRecord)+ ','+ tempMsg)
                        sent_count+=1
                        hard_flag=False
                        released_flag=True
                    else:
                        tempMsg = ''


        #print(input_value)
        msg = '**' +'PartnerA' + '>>' + tempMsg
        if '**quit' in msg:
            clientRunning = False
            s.send('**quit'.encode('ascii'))
        else:
            if '**vtime' in msg:
                record()
            elif '**rtime' in msg:
                print('recording time is ', datetime.datetime.now())
            s.send(msg.encode('ascii'))
            tempMsg = ''
        previous_value = input_value
