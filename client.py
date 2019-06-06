import socket
import threading
import sys, csv


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8000
uname = str(sys.argv[2])
ip = str(sys.argv[1])
s.connect((ip, port))
s.send(uname.encode('ascii'))
sync_steps = 2
delay_time = 0

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
