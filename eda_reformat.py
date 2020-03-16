import datetime, csv, sys, numpy,pandas as pd
time_data = []
touch_data = []

sublist = [5, 7, 12, 13, 19, 20, 21]
def csv_reader(header, path, session, r_time):
    tag=[]
    touch_data = []
    time_data = []
    elapsed = []
    count = 0
    #EDA
    df = pd.read_csv(header+session+path, names = ["Time", "Measurement"])
    df=df[(df['Time']>=str(r_time))]
    #This is the interval
    #df2=df[(df['Time']>=recording_time) & (df['Time']<'12:29:08')]
    eda_time = df.iloc[0][0]
    temp = str(eda_time).split(':')
    t_hour = int(temp[0])
    t_minute = float(temp[1])
    t_second = float(temp[2])
    t_value = datetime.timedelta(hours =t_hour, minutes =t_minute, seconds =t_second)
    eda2 = t_value + datetime.timedelta(seconds = float(0.25))
    elapsed.append(str(eda2))
    for i in range(1,len(df)):
        t_value = eda2
        eda2 = t_value + datetime.timedelta(seconds = float(0.25))
        elapsed.append(str(eda2))

    #print('eda time is ', eda_time)
    df['EDA_Time'] = elapsed
    df = df.drop(columns = "Time")
    df = df[["EDA_Time", "Measurement"]]
    return df

def edacombine(header,eda_df, recording_time):
    tag=[]
    touch_data = []
    time_data = []
    current = 0
    count = 0
    numtouch=0
    df = eda_df
    df2 = pd.read_csv(header+'received_data.csv', names = ["Time", "Touch"])

    for i in range(0,len(df2)):
        second = df2.iloc[i][0]
        temp = str(recording_time).split(':')
        r_hour = int(temp[0])
        r_minute = float(temp[1])
        if len(temp)>2:
            r_second = float(temp[2])
        else:
            r_second = 0
        r_time = datetime.timedelta(hours =r_hour, minutes =r_minute, seconds =r_second)

        time2 = (r_time + datetime.timedelta(seconds = float(second)))
        time_data.append(time2)
        touch_data.append(df2.iloc[i][1])
    touch_time = time_data.pop(0)
    touch_type = touch_data.pop(0)
    list = str(touch_time).split(':')
    t_hour = int(list[0])
    t_minute = float(list[1])
    t_second = float(list[2])
    #print(df)
    #print('length is ', len(df))
    for i in range(0,len(df)):
        e_value = df.iloc[i][0]
        #print('evalue is', e_value)
        temp_evalue= str(e_value).split(':')
        eda_hour = int(temp_evalue[0])
        eda_minute = int(temp_evalue[1])
        eda_second = float(temp_evalue[2])
        t_value2 = datetime.timedelta(hours = eda_hour, minutes = eda_minute, seconds =eda_second)
        eda2 = t_value2 + datetime.timedelta(seconds = float(0.25))
        temp_evalue2= str(eda2).split(':')
        eda_hour2 = int(temp_evalue[0])
        eda_minute2= int(temp_evalue[1])
        eda_second2 = float(temp_evalue[2])

        if len(touch_data)>0:
            if (t_hour == eda_hour2 and t_minute == eda_minute2 and t_second>=eda_second2) or (t_hour == eda_hour and t_minute > eda_minute):
                current = 0
                #print('appending 0 to ', touch_time)
                #print(e_value)
            elif eda_hour2 >= t_hour and eda_minute2 >=t_minute and t_second<=eda_second2:
                if touch_type in 'soft':
                    #print('soft')
                    #tag.append(2)
                    current = 2
                elif touch_type in 'medium':
                    #print('medium')
                    #tag.append(3)
                    current = 3
                elif touch_type in 'hard':
                    #print('hard')
                    #tag.append(4)
                    current = 4
                elif touch_type in 'release':
                    #print('release')
                    #tag.append(1)
                    current = 1
                touch_type = touch_data.pop(0)
                touch_time = time_data.pop(0)
            else:
                if current == 1:
                    current = 0
            tag.append(current)
            numtouch+=2
        else:
            tag.append(0)


    df['TouchTag'] = tag
    print(numtouch)

    df.to_csv((header + 'Complete_EDATime_reformat.csv'), index=None, header=True)
for i in range(1,3):
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
    eda_df = csv_reader(header, 'EDA.csv', 'SessionB/', r_time)
    edacombine(header, eda_df,r_time)
        #csv_reader(header, 'EDA.csv', 'SessionB/')
        #print('data is ', data)
