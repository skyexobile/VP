import datetime, csv, sys, numpy,pandas as pd
time_data = []
touch_data = []

def process(header,type,df):
    touch = ''
    t_time= ''
    temptouch = ''
    data= []
    timeflag = False
    for i in range(0, len(df)):
        if timeflag is False:
            temptime = df.iloc[i][0]
            ediff = temptime - datetime.timedelta(seconds = 2)

            t_time=('['+str(ediff)[7:]+']')
            timeflag = True
        if df.iloc[i][1] == 'release':
            touch = temptouch
            data.append(t_time + ' ' + touch )
            timeflag = False
        temptouch = df.iloc[i][1]
    #df2 = pd.DataFrame(temptouch)
    file = open(header+ type+'_TimeStamps.txt','w')
    for i in data:
        file.write(i)
        file.write('\n')
    file.close()#print(df2)



    #df2.to_csv((header + 'RawTimeStamps.csv'), index=None, header=True)

def csv_reader(header, path, type, r_time):
    tag=[]
    touch_data = []
    time_data = []
    elapsed = []
    count = 0
    list = str(r_time).split(':')
    t_hour = int(list[0])
    t_minute = float(list[1])
    t_second = float(list[2])
    df = pd.read_csv(header+path, names = ["ElapsedTime", "Touch"])
    print('t time is ')
    print(t_hour + t_minute+  t_second)
    t_value2 = datetime.timedelta(hours = t_hour, minutes = t_minute, seconds =t_second)
    for i in range(0,len(df)):
        e_time = df.iloc[i][0]
        esum = datetime.timedelta(seconds = float(e_time))
        elapsed2 = t_value2 + esum
        time_data.append([elapsed2,df.iloc[i][1]] )

    df2 = pd.DataFrame(time_data)
    process(header,type, df2)
    return df2

for i in range(22,23):
    print('ID',i)
    header=('../VP/B' +str(i) + '/')

    with open(header+ 'recordingtime.csv', newline='\n') as csvfile:
        counter=0
        data=[]
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i in spamreader:
            j = i
        r_time = (j[1])
        csvfile.close()
    print('rercording tim is ', r_time)
    rt_combined = csv_reader(header, 'received_data.csv', 'R', r_time)
    st_combined = csv_reader(header, 'sent_data.csv', 'S', r_time)
