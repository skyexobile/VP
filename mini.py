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
    csv = open(header+str(count)+'/'+fn+'.csv', "w+")
    writing = True
    track = 0
    for row in data:
        l = list(row)
        for i in range(len(l)):
            val = str(l[i].value)
            if track ==0:
                print('comma')
                csv.write(',Value')
                csv.write('\n')
                track+=1
                writing=False
            elif i == 0:
                writng = False
            elif val in "None":
                print('found a none')
                writing = False
            elif val in "Value":
                writing = False
                break
            if i == len(l) - 1:
                val = str(l[i].value)
                if val.endswith('.0'):
                    val = val[:-2]
                if val not in "None":
                    csv.write(val)
                    print('val is ', val)
                    writing = True
                else:
                    writing=False
            else:
                val = str(l[i].value)
                if val.endswith('.0'):
                    val = val[:-2]
                if val not in "None":
                    csv.write(val + ',')
                    print('vall is ', val + ',')
                    writing = False

            if writing == True:
                print('nsalinw')
                csv.write('\n')

    ## close the csv file
    csv.close()



def reversal(val):
    array=[0,9,8,7,6,5,4,3,2,1]
    return(array[val])

#print(min)
extra=["Talkative", "Extraverted", "Bold", "Energetic", "Shy*", "Quiet*", "Bashful*", "Withdrawn*"]
agree=["Sympathetic", "Warm", "Kind", "Cooperative", "Cold*", "Unsympathetic*", "Rude*", "Harsh*"]
conscientious=["Organized", "Efficient", "Systematic", "Practical", "Disorganized*", "Sloppy*", "Inefficient*", "Careless*"]
emo=["Unenvious", "Relaxed", "Moody*", "Jealous*", "Temperamental*", "Envious*", "Touchy*", "Fretful*"]
intellect=["Creative", "Imaginative", "Philosophical", "Intellectual", "Complex", "Deep", "Uncreative*", "Unintellectual*"]
def calculate(li):
    sum = 0
    for i in li:
        if i.endswith('*'):
            sum += (reversal(min.loc[i[:-1], "Value"]))
        else:
            sum+=(min.loc[i, "Value"])
    return(sum/8)
counter=11
while counter<23:
    convert('Mini5',counter)

    path = '../VP/B'+ str(counter)+'/'+'Mini5'
    min = pd.read_csv(path+ '.csv', index_col=0)
    print(min)
    escore = calculate(extra)
    ascore = calculate(agree)
    conscore = calculate(conscientious)
    emoscore = calculate(emo)
    iscore = calculate(intellect)
    content = []

    print("Extraversion score is ", escore)
    print("Agreeableness score is", ascore)
    print("Conscientiousness score is ", conscore)
    print("Emotional Stability score is ", emoscore)
    print("Intellect/Openness score is ", iscore)

    content.append(["Extraversion", escore])
    content.append(["Agreeableness", ascore])
    content.append(["Conscientiousness", conscore])
    content.append(["Emotional Stability", emoscore])
    content.append(["Intellect/Openness", iscore])
    print(content)
    with open(path + '_score.csv', "w", newline = '\n') as csv_file:
            writer = csv.writer(csv_file, delimiter = ',', quoting =csv.QUOTE_NONE)
            writer.writerows(content)
            csv_file.close()

    counter+=1
