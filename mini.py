import pandas as pd
import csv
def reversal(val):
    array=[0,9,8,7,6,5,4,3,2,1]
    return(array[val])
min = pd.read_csv("Mini5.csv", index_col=0)
result=(min.loc["Shy", "Value"])
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
escore = calculate(extra)
ascore = calculate(agree)
conscore = calculate(conscientious)
emoscore = calculate(emo)
iscore = calculate(intellect)
print("Extraversion score is ", escore)
print("Agreeableness score is", ascore)
print("Conscientiousness score is ", conscore)
print("Emotional Stability score is ", emoscore)
print("Intellect/Openness score is ", iscore)
