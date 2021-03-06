import datetime,csv

data = []
deltaData = []
def csv_writer(data, path):
    with open(path, "w", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = "\n", quoting=csv.QUOTE_NONE)
        writer.writerow(data)
        csv_file.close()
counter=3
while counter<23:
    path = "../VP/A" + str(counter)+"/"
    with open(path+'recordingtime.csv', newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in spamreader:
            for j in i:
                val = j.find(' ')
                dates = j[:val]
                list = dates.split('-')
                month = int(list[0])
                day = int(list[1])
                year = int(list[2])+2000
                times=(j[val+1:])
                list= times.split(':')
                hour = int(list[0])
                minute = int(list[1])
                second = int(list[2])
        csvfile.close()

    a = datetime.timedelta(hours = hour, minutes = minute, seconds = second)
    print(a)

    with open(path+'received_data.csv', newline='\n') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
            for i in spamreader:
                for j in i:
                    val = j.find(',')
                    delta = j[:val]
                    squeeze = j[val+1:]
                    data.append( str(a+datetime.timedelta(seconds=(float(delta)))) + ','+ squeeze)
                    quotient = float(delta)/60.0
                    print('quotient ', quotient)
                    b = datetime.timedelta(hours = 0, minutes = 0, seconds = 0)

                    deltaData.append( str(b+datetime.timedelta(seconds=(float(delta)))) + ','+ squeeze)
            csvfile.close()

    csv_writer(data, path+'received_touch.csv')
    csv_writer(deltaData, path+'received_touch_delta.csv')

    print('done', counter)

    counter+=1
