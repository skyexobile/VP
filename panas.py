import pandas as pd
import os
import openpyxl
import csv as csv
header='../VP/B'
def convert(fn,count):
    filename = header+str(count)+'/'+fn+'.xlsx'

    ## opening the xlsx file
    xlsx = openpyxl.load_workbook(filename)

    ## opening the active sheet
    sheet = xlsx.active

    ## getting the data from the sheet
    data = sheet.rows

    ## creating a csv file
    csv = open(header+str(count)+'/'+fn+' - Sheet1.csv', "w+")
    writing = True
    for row in data:
        l = list(row)
        for i in range(len(l)):
            val = str(l[i].value)
            if val in "None":
                writing = False
            elif i == len(l) - 1:
                val = str(l[i].value)
                if val.endswith('.0'):
                    val = val[:-2]
                csv.write(val)
                writing = True

            else:
                val = str(l[i].value)

                if val.endswith('.0'):
                    val = val[:-2]
                csv.write(val + ',')
                writing = True

            if writing == True:
                csv.write('\n')

    ## close the csv file
    csv.close()

def reversal(val):
    array=[0,4,3,2,1]
    return(array[val])
def csv_writer(data, path):
    with open(path, "w", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',', quoting =csv.QUOTE_NONE)
        writer.writerows(data)
        csv_file.close()
negative = ['afraid', 'scared', 'nervous', 'jittery', 'guilty', 'ashamed', 'irritable', 'hostile', 'upset', 'distressed']
fear=['afraid', 'scared', 'frightened', 'nervous', 'jittery', 'shaky']
sadness=['sad', 'blue','downhearted', 'alone', 'lonely']
guilt=['guilty', 'ashamed', 'blameworthy', 'angry at self', 'disgusted with self', 'dissatisfied with self']
hostility=['angry', 'irritable', 'hostile', 'scornful', 'digusted ','loathing']
shyness = ['shy', 'bashful', 'sheepish', 'timid']
fatigue=['sleepy', 'tired', 'sluggish', 'drowsy']
positive =['active', 'alert', 'attentive', 'enthusiastic', 'excited', 'inspired', 'interested', 'proud', 'strong', 'determined']
joviality=['cheerful', 'happy', 'joyful', 'delighted', 'enthusiastic', 'excited', 'lively', 'energetic']
self_assurance=['proud', 'strong', 'confident', 'bold', 'fearless', 'daring']
attentiveness=['alert','attentive','concentrating','determined']
serenity=['calm', 'relaxed', 'at ease']
surprise=['surprised', 'amazed', 'astonished']
def calculate(li):
    global df
    sum = 0
    for i in li:
        val = int(df.loc[i, "Values"])
        sum+=val
    return(sum)


#print(df)
def generate(name):
    data = {}
    keys=[]
    values=[]
    start = False
    print('test')
    with open(name,newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in spamreader:
            for j in i:
                if 'cheerful'  in j or 'sheepish' in j:
                    start = True
                if start is True:
                    if len(j)>0 and j not in 'None':
                        if len(j)>1 and j not in 'None':

                            stop = j.find('. ')
                            j=(j[stop+2:])
                            key = j
                            #print('key is ', key)
                            keys.append(j)
                        else:
                            data.update({str(key):j})
                            values.append(j)
                            #print('value is ', j)
        csvfile.close()
        pan = {'Values': values}
        df=pd.DataFrame.from_dict(pan)
        df.index= keys
        return df



counter=20

while counter <23:

    convert('PANAS-X1',counter)
    print('PANAS1 DONE')
    convert('PANAS-X2',counter)

    print('PANAS2 DONE')
    convert('PANAS-X3',counter)
    print('PANAS3 DONE', counter)
    print('here' , os.listdir(header+ str(counter)+'/'))
    for f_name in os.listdir(header+ str(counter)+'/'):
            content = []
            if f_name.startswith('PANAS') and not f_name.endswith('score.csv')and not f_name.endswith('.xlsx'):

                print('counter is ',counter)

                df = generate((header+str(counter) + '/')+f_name)
                val = f_name.find('- Sheet1')
                label = (f_name[:val-1])
                print(label)

                negscore = calculate(negative)
                fearscore = calculate(fear)
                sadscore=calculate(sadness)
                guiltscore=calculate(guilt)
                hostilityscore=calculate(hostility)
                shyscore=calculate(shyness)
                fatiguescore=calculate(fatigue)
                posscore=calculate(positive)
                jovscore= calculate(joviality)
                selfscore=calculate(self_assurance)
                attenscore=calculate(attentiveness)
                serenscore=calculate(serenity)
                surprisescore=calculate(surprise)
                content.append(['General Negative Affect', negscore])
                content.append(['Fear', fearscore])
                content.append(['Sadness', sadscore])
                content.append(['Guilt', guiltscore])
                content.append(['Hostility', hostilityscore])
                content.append(['Shyness', shyscore])
                content.append(['Fatigue', fatiguescore])
                content.append(['General Positive Affect', posscore])
                content.append(['Joviality', jovscore])
                content.append(['Self-Assurance', selfscore])
                content.append(['Attentiveness', attenscore])
                content.append(['Serenity', serenscore])
                content.append(['Surprise', surprisescore])
                path = header+str(counter) + '/'+label + '_score.csv'
                csv_writer(content, path )
                content = []

    counter+=1

'''

        else:
            def calculate2(li, val):
                global df
                sum = 0
                for i in li:
                    val = int(df.loc[i, "Values"])
                    sum+=val
                return(sum-val)
            negscore2 = calculate2(negative, negscore)
            fearscore2 = calculate2(fear, fearscore)
            sadscore2=calculate2(sadness,sadscore)
            guiltscore2=calculate2(guilt,guiltscore)
            hostilityscore2=calculate2(hostility,hostilityscore)
            shyscore2=calculate2(shyness,shyscore)
            fatiguescore2=calculate2(fatigue,fatiguescore)
            posscore2=calculate2(positive,posscore)
            jovscore2= calculate2(joviality,jovscore)
            selfscore2=calculate2(self_assurance,selfscore)
            attenscore2=calculate2(attentiveness,attenscore)
            serenscore2=calculate2(serenity,serenscore)
            surprisescore2=calculate2(surprise,surprisescore)
            print('General Negative Affect: ', negscore2)
            print('Fear: ', fearscore2)
            print('Sadness: ', sadscore2)
            print('Guilt: ', guiltscore2)
            print('Hostility', hostilityscore2)
            print('Shyness: ', shyscore2)
            print('Fatigue: ', fatiguescore2)
            print('General Positive Affect: ', posscore2)
            print('Joviality: ', jovscore2)
            print('Self-Assurance: ', selfscore2)
            print('Attentiveness: ', attenscore2)
            print('Serenity: ', serenscore2)
            print('Surprise: ', surprisescore2)
'''
