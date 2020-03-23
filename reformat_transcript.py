import datetime, csv, sys, numpy,pandas as pd
for i in range(4,23):
    print('User ', i)
    header=('../VP/B' +str(i) + '/')
    type = 'S'
    file = csv.reader(open(header+ type+'_TimeStamps.txt','r'), delimiter  = ' ')
    time_data = []
    touch_data = []
    duration_data = []
    for i in file:
        print('length is ', len(i))
        if len(i)>0:
            timestamp = i[0]
            print(timestamp)
            list = str(timestamp[0:-1]).split(':')
            print(list)

            t_minute = float(list[1])
            t_second = float(str(list[2]))

            t_value= datetime.timedelta(hours = 0, minutes = t_minute, seconds =t_second)
            #print('t_value is ' , t_value)
            if t_minute >0 or t_second >3:
                t_value = t_value - datetime.timedelta(seconds =3.00)

                #print(str(t_value)[:-4])
            else:
                t_value= datetime.timedelta(hours = 0, minutes = 0, seconds =0.00)
            list = str(t_value).split(':')
            t_minute = int(list[1])
            t_second = float(str(list[2]))
            if t_minute <10:
                t_value= '00:' + '0'+str(t_minute)+':'
            else:
                t_value= '00:' +str(t_minute)+':'
            if t_second <10:
                t_value= t_value+ '0'+str(t_second)
            else:
                t_value=t_value+str(t_second)
            time_data.append(t_value)
            #print(str(t_value))
            touch_data.append(i[1])
            duration = i[3]
            duration_data.append(duration)
    with open(header+ 'NEW_' + type+'_TimeStamps.txt','w') as tfile:
        twriter = csv.writer(tfile)
        for i in range(0,len(time_data)):
            twriter.writerow(['['+str(time_data[i])+']', touch_data[i],str(duration_data[i])])
    tfile.close()
