import datetime, csv, sys, numpy,pandas as pd
counter = 0
time_data = []
touch_data = []


def csv_convert(header, path, subjectid):
    tag=[]
    touch_data = []
    time_data = []
    current = 0
    count = 0
    df = pd.read_csv(header+path)
    df['SubjectID'] = subjectid #This is the interval
    print('subject id  ', subjectid)
    print(df.max())
    return df
Partner = 'B'
df1 = csv_convert('../VP/'+Partner+'1/', 'Complete_EDATime_reformat.csv',Partner +'1')
for i in range(1,23):
    if i == 2:
        continue
    else:
        header=('../VP/'+Partner+str(i)+'/')
        df2 = csv_convert(header, 'Complete_EDATime_reformat.csv',Partner+str(i))
        df1 = pd.concat([df1,df2], ignore_index = True)
#print(df1)
#df1.to_csv(('../VP/'+Partner+'_CombinedEDA.csv'), index=None, header=True)
