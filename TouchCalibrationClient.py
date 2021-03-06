
import tkinter as tkin
from tkinter import messagebox

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
input_serial = serial.Serial('/dev/cu.usbmodem14101')
input_serial.baudrate =115200
input_serial.setDTR(False)
input_serial.setRTS(False)

output_serial = serial.Serial('/dev/cu.usbmodem14201')

output_serial.baudrate =115200
output_serial.setDTR(False)
output_serial.setRTS(False)


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
time_list = []
flag_save_sent = False
flag_save_recv = False
def record():
    global recording_time
    global videoRecording, time_list
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

    with open('Data/recordingtime.csv', "a", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = '\n')
        now = datetime.datetime.now()
        time_list.append(now.strftime("%m-%d-%y %H:%M:%S"))
        writer.writerow(time_list)
        csv_file.close()


def reset():
    global offset
    input_serial.write(str("0").encode())
    offset = 0
    print("Reset Complete")
def set_soft():
    global offset
    global soft_value

    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset

    soft_value = input_value
    print("Soft has been defined ", soft_value)
def set_medium():
    global medium_value, offset
    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset
    medium_value = input_value
    print("Medium has been defined ", medium_value)
def set_hard():
    global offset, hard_value
    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset
    hard_value = input_value
    print("Hard has been defined ", hard_value)
def save_settings():
    global soft_value, hard_value, PID_value, medium_value

    print("Your settings have been saved!")
    print("soft is ", soft_value)
    print("medium is ", medium_value)
    print("hard is ", hard_value)

def save_sent():
    global sent_list
    csv_writer(sent_list, 'Sent/sent_data.csv')
    flag_save_recv = True
    print('Saved Sent Touches')
def save_recv():
    global recv_list
    csv_writer(recv_list, 'Received/received_data.csv')
    flag_save_recv = True
    print('Saved Received Touches')


def out_soft():
    output_serial.write(str('a').encode())
def out_med():
    output_serial.write(str('b').encode())
def out_hard():
    output_serial.write(str('c').encode())
def releasebtn():
    output_serial.write(str('K').encode())
def estop():
    output_serial.write(str('s').encode())
def loosen():
    output_serial.write(str('J').encode())
def tighten():
    output_serial.write(str('M').encode())
def resetout():
    output_serial.write(str('r').encode())
    print('Reset Complete')

def on_closing():
    global clientRunning, flag_save_recv, flag_save_sent
    if messagebox.askokcancel("Quit", "Sent and Received already saved"):
        if flag_save_sent is not True:
            save_sent()
        if flag_save_recv is not True:
            save_recv()
        root.destroy()
        clientRunning = False

root.protocol("WM_DELETE_WINDOW", on_closing)
calisoft =  tkin.Button(root, text = "Set Soft Output", command = out_soft)
calimed = tkin.Button(root, text = "Set Med. Output", command = out_med)
calihard = tkin.Button(root, text = "Set Hard Output", command = out_hard)
calirel = tkin.Button(root, text = "Release Output", command = releasebtn)
emerstop = tkin.Button(root, text = "Emergency Stop", command = estop)
loosenbtn = tkin.Button(root, text = "Loosen", command = loosen)
tightenbtn = tkin.Button(root, text = "Tighten", command = tighten)
resetoutbtn = tkin.Button(root, text = "Reset Output", command = resetout)

reset_button =  tkin.Button(root, text = "Reset Sensor", command = reset)
soft_button =  tkin.Button(root, text = "Define Soft", command = set_soft)
medium_button =  tkin.Button(root, text = "Define Medium", command = set_medium)
hard_button  =  tkin.Button(root, text = "Define Hard", command = set_hard)
save_button  =  tkin.Button(root, text = "Save Settings", command = save_settings)
#replay_instance = tkin.Button(root, text = "Instance Replay", command = replay)
record_video = tkin.Button(root, text = "Record", command = record)
save_sTouch = tkin.Button(root, text = 'Save Sent', command = save_sent)
save_rTouch = tkin.Button(root, text = 'Save Received', command = save_recv)
record_video.pack(side = tkin.TOP)

save_rTouch.pack(side = tkin.RIGHT)
save_sTouch.pack(side = tkin.RIGHT)
reset_button.pack(side = tkin.LEFT)
soft_button.pack(side = tkin.LEFT)
medium_button.pack(side = tkin.LEFT)
hard_button.pack(side = tkin.LEFT)
save_button.pack(side = tkin.LEFT)
resetoutbtn.pack(side = tkin.BOTTOM)

emerstop.pack(side = tkin.BOTTOM)
loosenbtn.pack(side = tkin.BOTTOM)
tightenbtn.pack(side = tkin.BOTTOM)
calirel.pack(side = tkin.BOTTOM)

calihard.pack(side = tkin.BOTTOM)

calimed.pack(side = tkin.BOTTOM)
calisoft.pack(side = tkin.BOTTOM)
#root.update()
def csv_writer(data, path):
    with open(path, "a", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = '\n')
        writer.writerow(data)
        csv_file.close()
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
                print("soft squeeze Received")
                output_serial.write(str('B').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)

                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord) + ',soft')
                #print("touch record is ", touch_record)
                touch_record.append(msg)
            elif 'medium' in msg:
                print("medium squeeze Received")

                output_serial.write(str('E').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)

                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord)+ ',medium')
                #print("touch record is ", touch_record)
                touch_record.append(msg)
            elif 'hard' in msg:
                print("hardsqueeze received")

                output_serial.write(str('H').encode())
                #output_serial.readline().decode()
                print('message received is ' +msg)

                tempRecord =  float(time.time())-(recording_time)
                recv_list.append(str(tempRecord)+ ',hard')
                touch_record.append(msg)
                #print("touch record is ", touch_record)
            elif 'release' in msg:
                print("release received")

                output_serial.write(str('K').encode())
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
    value = (input_serial.readline().decode())
    input_value = float(value)
    while videoRecording is True:
        root.update()
        value = (input_serial.readline().decode())
        input_value = float(value)
        if abs(input_value) - abs(previous_value) >0:
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

                else:
                    tempMsg = ''
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
                        tempMsg = 'release'
                        tempRecord = float(time.time())-(recording_time)
                        sent_list.append(str(tempRecord)+ ','+ tempMsg)
                        sent_count+=1
                        hard_flag=False
                        released_flag=True
                    else:
                        tempMsg = ''


        #print(input_value)f
        msg = '**' +'PartnerB' + '>>' + tempMsg
        if '**quit' in msg:
            clientRunning = False
            s.send('**quit'.encode('ascii'))
        else:
            if '**vtime' in msg:
                record()
            elif '**rtime' in msg:
                now = datetime.datetime.now()
                print ("Recording date and time : ")
                print (now.strftime("%Y-%m-%d %H:%M:%S"))
            elif tempMsg == '':
                tempMsg = ''
                #print('stuck in here')
            else:
                print('sending ', tempMsg)
                s.send(msg.encode('ascii'))

            tempMsg = ''
        previous_value = input_value
