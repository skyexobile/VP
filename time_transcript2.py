import datetime, csv, sys, numpy,pandas as pd
time_data = []
touch_data = []

def process(header,type,df):
    touch = ''
    t_time= ''
    temptouch = ''
    data= []
    timeflag = False
    initial = True
    for i in range(0, len(df)):
        if timeflag is False:
            temptime = df.iloc[i][0]
            if initial is False:
                ediff = temptime - datetime.timedelta(seconds = 10)
                print( 'edfiff is ', ediff)
            else:
                ediff = temptime - datetime.timedelta(seconds = 10)
                initial = False
            t_time=('['+str(ediff)[7:-4]+']')
            print(t_time)
            timeflag = True
        if df.iloc[i][1] == 'release':
            touch = temptouch
            difference = df.iloc[i][0]-temptime
            d_time=(' /d '+str(difference)[11:-4]+' d/')
            data.append(t_time + ' ' + touch + d_time )
            timeflag = False
        temptouch = df.iloc[i][1]
    #df2 = pd.DataFrame(temptouch)
    print(data)
    file = open(header+ type+'_TimeStamps.txt','w')
    for i in data:
        file.write(i)
        file.write('\n')
    file.close()#print(df2)



    #df2.to_csv((header + 'RawTimeStamps.csv'), index=None, header=True)

def csv_reader(header, path, type):
    tag=[]
    touch_data = []
    time_data = []
    elapsed = []
    count = 0

    df = pd.read_csv(header+path, names = ["ElapsedTime", "Touch"])
    t_value2 = datetime.timedelta(hours = 0.0, minutes = 0.0, seconds =0.0)
    for i in range(0,len(df)):
        e_time = df.iloc[i][0]
        esum = datetime.timedelta(seconds = float(e_time))
        elapsed2 = t_value2 + esum
        time_data.append([elapsed2,df.iloc[i][1]] )
        #print('adding', elapsed2)

    df2 = pd.DataFrame(time_data)
    process(header,type, df2)
    return df2

for i in range(1,15):
    print('ID',i)
    header=('../VP/A' +str(i) + '/')

    rt_combined = csv_reader(header, 'received_data.csv', 'R')
    #st_combined = csv_reader(header, 'sent_data.csv', 'S')
