
import tkinter as tkin

import serial, datetime, time, re

import os, select, sys, csv, threading
from time import gmtime, strftime
import socket


import csv
from subprocess import Popen, PIPE
r_counter = 0
s_counter = 0
s_dict = {}
r_dict = {}
start_time = 0
end_time = -1
splay_counter = 0
rplay_counter = 0
root = tkin.Tk()
rmcounter = 0
smcounter = 0
touch_counter=1
touch_counter2=1
f_name = ''
def sent_replay():
    import moviepy.editor as me
    global s_counter, s_dict, splay_counter, smcounter, touch_counter, f_name
    if ((touch_counter % 2) != 0):
        if(splay_counter < (len(s_dict))) :

            start_time = s_dict[str(splay_counter)][0]

            #print(dict[str(play_counter-1)][1])
            if s_dict[str(splay_counter)][1] is 'release':
                end_time = s_dict[str(splay_counter)][1]

            else:
                while s_dict[str(splay_counter)][1] is not 'release':

                    if s_dict[str(splay_counter)][1] == 'release':
                        break
                    elif s_dict[str(splay_counter)][0] is s_dict[str(s_counter-1)][0]:
                        break
                    else:
                        splay_counter+=1

                end_time = s_dict[str(splay_counter)][0]
            if start_time == end_time:
                print('No more clips')
            else:
                for f_name in os.listdir('../VP'):
                    if f_name.endswith('.mov'):
                        print(f_name)
                        clip = me.VideoFileClip(f_name)
                #clip = clip.resize(0.5)
                #clip = clip.subclip(float(start_time)-1.0, float(stop_time) +1.0)
                        st = float(start_time)
                        et = float(end_time)
                        clip = clip.subclip((st - 0.5), (et+ 0.5))
                        clip.write_videofile(("Sent/Smovie" + str(smcounter) +".webm"), audio=True) # default codec: 'libx264', 24 fps
                print('New Clip Generated')
                smcounter+=1
                splay_counter+=1
                touch_counter+=1

    else:
        if(splay_counter < (len(s_dict))) :
            while s_dict[str(splay_counter)][1] is not 'release':

                if s_dict[str(splay_counter)][1] == 'release':
                    break
                elif s_dict[str(splay_counter)][0] is s_dict[str(s_counter-1)][0]:
                    break
                else:
                    splay_counter+=1
                    if s_dict[str(splay_counter)][1] == 'release':
                        splay_counter+=1
                        break
                splay_counter+=1
            touch_counter+=1
        else:
            print('All Done.')
def recv_replay():
    import moviepy.editor as me
    global r_dict, r_counter, rplay_counter, rmcounter, touch_counter2, f_name
    if ((touch_counter2 % 2) != 0):
        if(rplay_counter < (len(r_dict))) :

            start_time = r_dict[str(rplay_counter)][0]

            #print(dict[str(play_counter-1)][1])
            if r_dict[str(rplay_counter)][1] is 'release':
                end_time = r_dict[str(rplay_counter)][1]

            else:
                while r_dict[str(rplay_counter)][1] is not 'release':

                    if r_dict[str(rplay_counter)][1] == 'release':
                        break
                    elif r_dict[str(rplay_counter)][0] is r_dict[str(r_counter-1)][0]:
                        break
                    else:
                        rplay_counter+=1

                end_time = r_dict[str(rplay_counter)][0]
            if start_time == end_time:
                print('No more clips')
            else:
                for f_name in os.listdir('../VP'):
                    if f_name.endswith('.mov'):
                        print(f_name)
                        clip = me.VideoFileClip(f_name)
                #clip = clip.resize(0.5)
                #clip = clip.subclip(float(start_time)-1.0, float(stop_time) +1.0)
                        st = float(start_time)
                        et = float(end_time)
                        clip = clip.subclip((st - 0.5), (et+ 0.5))
                        clip.write_videofile(("Received/Rmovie" + str(rmcounter) +".webm"), audio=True) # default codec: 'libx264', 24 fps
                print('New Clip Generated')
                rmcounter+=1
                rplay_counter+=1
                touch_counter2+=1

    else:
        if(rplay_counter < (len(r_dict))) :
            while r_dict[str(rplay_counter)][1] is not 'release':

                if r_dict[str(rplay_counter)][1] == 'release':
                    break
                elif r_dict[str(rplay_counter)][0] is r_dict[str(r_counter-1)][0]:
                    break
                else:
                    rplay_counter+=1
                    if r_dict[str(rplay_counter)][1] == 'release':
                        rplay_counter+=1
                        break
                rplay_counter+=1
            touch_counter2+=1
        else:
            print('All Done.')


replay_instance = tkin.Button(root, text = "Sent Replay", command = sent_replay)
replay_instance.pack()

replay_instance2= tkin.Button(root, text = "Receive Replay", command = recv_replay)
replay_instance2.pack()

with open('Sent/sent_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            s_dict[str(s_counter)]=row
            s_counter+=1
        csvfile.close()

with open('Received/received_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            r_dict[str(r_counter)]=row
            r_counter+=1
        csvfile.close()

while True:
    root.update()
