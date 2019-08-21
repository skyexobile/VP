import pandas as pd
import csv
def reversal(val):
    array=[0,4,3,2,1]
    return(array[val])

negative = ['afraid', 'scared', 'nervous', 'jittery', 'guilty', 'ashamed', 'irritable', 'hostile', 'upset', 'distressed']
fear=['afraid', 'scared', 'frightened', 'nervous', 'jittery', 'shaky']
sadness=['sad', 'blue','downhearted', 'alone', 'lonely']
guilt=['guilty', 'ashamed', 'blameworthy', 'angry at self', 'disgusted with self', 'dissatisfied with self']
hostility=['angry', 'irritable', 'hostile', 'scornful', 'disgusted with self', 'loathing']
shyness = ['shy', 'bashful', 'sheepish', 'timid']
fatigue=['sleepy', 'tired', 'sluggish', 'drowsy']
positive =['active', 'alert', 'attentive', 'enthusiastic', 'excited', 'inspired', 'interested', 'proud', 'strong', 'determined']
joviality=['cheerful', 'happy', 'joyful', 'delighted', 'enthusiastic', 'excited', 'lively', 'energetic']
self_assurance=['proud', 'strong', 'confident', 'bold', 'fearless', 'daring']
attentiveness=['alert','attentive','concentrating','determined']
serenity=['calm', 'relaxed', 'at ease']
surprise=['surprised', 'amazed', 'astonished']
data = {}
keys=[]
values=[]
start = False
with open('panas.csv', newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in spamreader:

            for j in i:
                if 'cheerful'  in j or 'sheepish' in j:
                    start = True
                if start is True:
                    if len(j)>0:
                        if len(j)>1:
                            stop = j.find('. ')
                            j=(j[stop+2:])
                            key = j
                            keys.append(j)
                        else:
                            data.update({str(key):j})
                            values.append(j)
        csvfile.close()
pan = {'Values': values}
df=pd.DataFrame.from_dict(pan)
df.index= keys
#print(df)
def calculate(li):
    sum = 0
    for i in li:
        val = int(df.loc[i, "Values"])
        sum+=val
    return(sum)

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
print('General Negative Affect: ', negscore)
print('Fear: ', fearscore)
print('Sadness: ', sadscore)
print('Guilt: ', guiltscore)
print('Hostility', hostilityscore)
print('Shyness: ', shyscore)
print('Fatigue: ', fatiguescore)
print('General Positive Affect: ', posscore)
print('Joviality: ', jovscore)
print('Self-Assurance: ', selfscore)
print('Attentiveness: ', attenscore)
print('Serenity: ', serenscore)
print('Surprise: ', surprisescore)
