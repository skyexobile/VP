import socket
import threading
import sys, csv, time
from subprocess import Popen, PIPE, time

sent = []
received = []

recording_time = 0
def record():
    scpt = '''
    tell application "System Events"
    	keystroke "%" using command down
    	delay 1.0
    	keystroke return
    end tell'''


    args = ['2', '2']


    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(scpt)
    recording_time = time.time()
    s.send('**time'.encode('ascii'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8000
uname = str(sys.argv[2])
ip = str(sys.argv[1])
s.connect((ip, port))
s.send(uname.encode('ascii'))

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
            if '**send' in msg:
                msg = msg[(msg.find('**send')+6):]
                received.append(msg)
                print('this is the list: ',received)
            elif '**vtime' in msg:
                msg = msg[msg.find('**vtime')+8:]
                recording_time = float(msg) + 4
                print('video recording time is ', recording_time)
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
        if '**vtime' in msg:
            record()
        elif '**rtime' in msg:
            print('recording time is ', datetime.datetime.now())
        s.send(msg.encode('ascii'))
