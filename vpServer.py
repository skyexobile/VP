import socket
import threading
import time, sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 8000

clients = {}

s.bind((ip, port))
s.listen()
print('Server Ready...')
print('Ip Address of the Server::%s'%ip)
def csv_writer(data, path):
    with open(path, "a", newline = '') as csv_file:
        #writer = csv.writer(csv_file, delimiter = ' ')
        csv_file.write(str(data) + '\n')
        csv_file.close()
    print('done')
#path = "DataFiles/" + str(subID)+ "/psycho_data.csv"
def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = 'Number of People Online\n'
            found = False
            print('this is the message im getting' + msg)
            if '**broadcast' in msg:
                ticks = time.time()
                msg = (uname + ',' + str(ticks))
                for k,v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '**quit' in msg:
                response = 'Stopping Session and exiting...'
                client.send(response.encode('ascii'))
                for i in clients:
                    clients.pop(uname)
                    print(uname + ' has been logged out')
                clientConnected = False
            else:
                for name in keys:
                    if('**'+name) in msg:
                        ticks = time.time()
                        msg = msg.replace('**'+name, '')
                        msg = msg + (',' + str(ticks))
                        print(msg)
                            #csv_writer(temp_msg, path)
                        #print('this name is ', name)
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if(not found):
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
        except:
            clients.pop(uname)
            print(uname + ' has been logged out')
            clientConnected = False

while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    print('%s connected to the server'%str(uname))
    client.send('Welcome to Messenger.'.encode('ascii'))

    if(client not in clients):
        clients[uname] = client
        threading.Thread(target = handleClient, args = (client, uname, )).start()
