import datetime, csv, sys

def csv_writer(data, path):
    with open(path, "w", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = "\n", quoting=csv.QUOTE_NONE)
        writer.writerow(data)
        csv_file.close()
def csv_reader(header, path):
    with open(header+path, newline='\n') as csvfile:
        counter=0
        data=[]
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in spamreader:
            if counter ==0:
                for j in i:
                    j = float(str(j))
                    a=(datetime.datetime.fromtimestamp(int(j)).strftime('%H:%M:%S'))
                    list= a.split(':')
                    hour = int(list[0])
                    minute = int(list[1])
                    second = int(list[2])
                    a = datetime.timedelta(hours = hour, minutes = minute, seconds = second)
            if counter == 1:
                for j in i:
                    divider = float(str(j))
            if counter >1:
                for j in i:
                    data.append( str(a) + ','+ j)
                    a = a+datetime.timedelta(seconds=(float(1)/divider))
            counter+=1
        csvfile.close()
        path = header+path
        #print('data is ', data)
        csv_writer(data, path)

count=5
while count< 23:
    header=('../VP/B'+ str(count)+'/SessionA/')

    csv_reader(header,'HR.csv')
    csv_reader(header,'EDA.csv')

    csv_reader(header,'BVP.csv')
    csv_reader(header,'TEMP.csv')
    header=('../VP/B'+ str(count)+'/SessionB/')

    csv_reader(header,'HR.csv')
    csv_reader(header,'EDA.csv')

    csv_reader(header,'BVP.csv')
    csv_reader(header,'TEMP.csv')
    print('done with ', count)
    count+=1
