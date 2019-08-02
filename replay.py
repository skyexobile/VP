
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
click_count=0
release_count = 0
release_count2 = 0
start_time = 0
end_time = 0
def sent_replay():
    import moviepy.editor as me
    global s_counter, s_dict, splay_counter, smcounter, touch_counter, f_name, release_count, start_time, end_time
    generated = False
    global click_count
    starting = int(release_count/4)
    while generated is False:

        while starting >0:
            if(splay_counter < (len(s_dict))) :
                val = s_dict[str(splay_counter)][1]
                if 'release' in val:
                    starting-=1
                    splay_counter+=1
                else:
                    while 'release' not in val:
                        splay_counter+=1
                        val = s_dict[str(splay_counter)][1]
        while click_count <7:
            num = touch_counter %4
            if (num == 0):
                if(splay_counter < (len(s_dict))) :
                    start_time = s_dict[str(splay_counter)][0]
                    print('start time is ', start_time)
                    #print(dict[str(play_counter-1)][1])
                    val = s_dict[str(splay_counter)][1]

                    if 'release' in val:
                        end_time = s_dict[str(splay_counter)][0]

                    else:
                        while 'release' not in val:

                            if 'release' in val:
                                print('found release in while')
                                print(s_dict[str(splay_counter)][1])
                                break
                            elif (splay_counter >= len(s_dict)):
                                print('reached the end of the list')
                                break
                            else:
                                splay_counter+=1
                                val = s_dict[str(splay_counter)][1]


                        end_time = s_dict[str(splay_counter)][0]
                        print('end time is ', end_time)
                    if start_time == end_time:
                        print('No more clips')
                        generated = True
                    else:
                        if click_count >1:
                            for f_name in os.listdir('../VP'):
                                if f_name.endswith('.mov'):
                                    print(f_name)
                                    clip = me.VideoFileClip(f_name)
                            #clip = clip.resize(0.5)
                            #clip = clip.subclip(float(start_time)-1.0, float(stop_time) +1.0)
                                    st = float(start_time)
                                    et = float(end_time)
                                    clip = clip.subclip((st - 2), (et+ 2))
                                    clip.write_videofile(("Sent/Smovie" + str(smcounter) +".webm"), audio=True) # default codec: 'libx264', 24 fps
                            print('Clip#'+ str(click_count)+' Generated')
                        click_count+=1
                        smcounter+=1
                        splay_counter+=1
                        touch_counter+=1
                else:
                    print('Done')
                    generated = True

            else:
                if(splay_counter < (len(s_dict))) :
                    start_time = s_dict[str(splay_counter)][0]
                    val = s_dict[str(splay_counter)][1]

                    while 'release' not in val:
                        if 'release' in val:
                            print(s_dict[str(splay_counter)][1])
                            break
                        elif splay_counter == len(s_dict):
                            print(s_dict[str(splay_counter)][0])
                            break
                        else:
                            splay_counter+=1
                            val = s_dict[str(splay_counter)][1]
                            if 'release' in val:
                                break
                        splay_counter+=1
                    splay_counter+=1
                    touch_counter+=1
                else:
                    print('All Done.')
                    generated = True
        generated = True

def recv_replay():
    import moviepy.editor as me
    global r_counter, r_dict, rplay_counter, rmcounter, touch_counter2, f_name,release_count2
    generated = False
    starting = int(release_count2/4)

    global click_count
    while generated is False:
        while starting >0:
            if(rplay_counter < (len(r_dict))) :
                val = r_dict[str(rplay_counter)][1]
                if 'release' in val:
                    starting-=1
                    rplay_counter+=1
                else:
                    while 'release' not in val:
                        rplay_counter+=1
                        val = r_dict[str(rplay_counter)][1]
        while click_count <7:
            if ((touch_counter2 % 4) != 0):
                if(rplay_counter < (len(r_dict))) :

                    start_time = r_dict[str(rplay_counter)][0]
                    print('start time is ', start_time)
                    #print(dict[str(play_counter-1)][1])
                    val = r_dict[str(rplay_counter)][1]

                    if 'release' in val:
                        end_time = r_dict[str(rplay_counter)][0]

                    else:
                        while 'release' not in val:

                            if 'release' in val:
                                print('found release in while')
                                print(r_dict[str(rplay_counter)][1])
                                break
                            elif rplay_counter== len(r_dict):
                                print('reached the end of the list')

                                break
                            else:
                                rplay_counter+=1
                                val = r_dict[str(rplay_counter)][1]


                        end_time = r_dict[str(rplay_counter)][0]
                        print('end time is ', end_time)
                    if start_time == end_time:
                        print('No more clips')
                        generated = True
                    else:
                        if click_count >1:
                            for f_name in os.listdir('../VP'):
                                if f_name.endswith('.mov'):
                                    print(f_name)
                                    clip = me.VideoFileClip(f_name)
                            #clip = clip.resize(0.5)
                            #clip = clip.subclip(float(start_time)-1.0, float(stop_time) +1.0)
                                    st = float(start_time)
                                    et = float(end_time)
                                    clip = clip.subclip((st - 2), (et+ 2))
                                    clip.write_videofile(("Received/Rmovie" + str(rmcounter) +".webm"), audio=True) # default codec: 'libx264', 24 fps
                            print('Clip#'+ str(click_count)+' Generated')
                        click_count+=1
                        rmcounter+=1
                        rplay_counter+=1
                        touch_counter2+=1
                else:
                    print('Done')
                    generated = True

            else:

                if(rplay_counter < (len(r_dict))) :
                    start_time = r_dict[str(rplay_counter)][0]
                    val = r_dict[str(rplay_counter)][1]

                    while 'release' not in val:

                        if 'release' in val:
                            print('found release in while')
                            break
                        elif rplay_counter==len(r_dict):
                            print('reached the end of the list')

                            break
                        else:
                            rplay_counter+=1
                            val = r_dict[str(rplay_counter)][1]

                            if 'release' in val:
                                print('found release')#rplay_counter+=1
                                break
                        rplay_counter+=1
                    rplay_counter+=1
                    touch_counter2+=1
                else:
                    print('All Done.')
                    generated = True
        generated=True

with open('Sent/sent_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if 'release' in row:
                release_count +=1
            s_dict[str(s_counter)]=row
            s_counter+=1
        print('this is the count ',release_count)
        csvfile.close()

with open('Received/received_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if 'release' in row:
                release_count2 +=1
            r_dict[str(r_counter)]=row
            r_counter+=1
        csvfile.close()

#sent_replay()
click_count =0
recv_replay()
print('All Done.')
