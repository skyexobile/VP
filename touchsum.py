import os
import openpyxl
import csv as csv


def csv_writer(data, path):
    with open(path, "a", newline = '\n') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',', quoting =csv.QUOTE_NONE)
        writer.writerows(data)
        csv_file.close()
heading1 = ['SubjectID', 'Gender','Action', 'TouchTotal', 'SoftTouch', 'MediumTouch', 'HardTouch']
heading2 = ['SubjectID', 'Gender', 's_TouchTotal', 'r_TouchTotal', 's_SoftTouch', 'r_SoftTouch','s_MediumTouch',  'r_MediumTouch', 's_HardTouch','r_HardTouch']
#csv_writer([heading1], 'TouchSummaryMerge.csv')
#csv_writer([heading2], 'TouchSummary.csv')
heading1 = ['SubjectID', 'Gender','Extraversion', 'Agreeableness', 'Conscientiousness', 'Emotional Stability', 'Intellect/Openness', 'Action', 'TouchTotal', 'SoftTouch', 'MediumTouch', 'HardTouch']
heading2 = ['SubjectID', 'Gender', 's_TouchTotal', 'r_TouchTotal', 's_SoftTouch', 'r_SoftTouch','s_MediumTouch',  'r_MediumTouch', 's_HardTouch','r_HardTouch']
csv_writer([heading1], 'TouchSummaryMerge.csv')
csv_writer([heading2], 'TouchSummary.csv')
for counter in range(1, 23):
    s_soft_counter=0
    s_medium_counter=0
    s_hard_counter=0
    s_release_count=0
    r_soft_counter=0
    r_medium_counter=0
    r_hard_counter=0
    r_release_count=0
    e_score=0
    a_score=0
    c_score=0
    i_score=0
    emo_score=0
    squeeze = ''
    header = '../VP/A'+str(counter)

    with open(header+'/sent_data.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if 'release' in row:
                    if 'soft' in squeeze:
                        s_soft_counter+=1
                    elif 'medium' in squeeze:
                        s_medium_counter+=1
                    elif 'hard' in squeeze:
                        s_hard_counter+=1
                    s_release_count +=1
                else:
                    squeeze = row

            csvfile.close()

    with open(header+'/received_data.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if 'release' in row:
                    if 'soft' in squeeze:
                        r_soft_counter+=1
                    elif 'medium' in squeeze:
                        r_medium_counter+=1
                    elif 'hard' in squeeze:
                        r_hard_counter+=1
                    r_release_count +=1
                else:
                    squeeze = row

            csvfile.close()
    print('here' , os.listdir(header))
    for f_name in os.listdir(header):
        if f_name.startswith('Mini5') and f_name.endswith('score.csv'):
            with open(header+'/'+f_name, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        if "Extraversion" in row:
                            e_score = row[1]
                        elif "Agreeableness" in row:
                            a_score = row[1]
                        elif "Conscientiousness" in row:
                            c_score = row[1]
                        elif "Emotional Stability" in row:
                            emo_score = row[1]
                        else:
                            i_score = row[1]
            csvfile.close()
    print('SubjectID', counter)
    print('Extraversion', e_score)
    print('Agreeableness', a_score)
    print('Consc.', c_score)
    print('Emotional', emo_score)
    print('Intellect', i_score)
    print('Sent ',s_release_count)
    print('soft', s_soft_counter)
    print('medium', s_medium_counter)
    print('hard', s_hard_counter)
    print('Received ',r_release_count)
    print('soft', r_soft_counter)
    print('medium', r_medium_counter)
    print('hard', r_hard_counter)
    print('Finished')
    csv_writer([[counter,'Female', e_score, a_score,c_score, emo_score, i_score, 'Sent', s_release_count, s_soft_counter, s_medium_counter, s_hard_counter]], 'TouchSummaryMerge.csv')
    csv_writer([[counter,'Female', e_score, a_score,c_score, emo_score, i_score,'Received', r_release_count, r_soft_counter, r_medium_counter, r_hard_counter]], 'TouchSummaryMerge.csv')

    csv_writer([[counter,'Female', s_release_count,r_release_count,s_soft_counter,r_soft_counter,s_medium_counter, r_medium_counter, s_hard_counter,r_hard_counter]], 'TouchSummary.csv')
    s_soft_counter=0
    s_medium_counter=0
    s_hard_counter=0
    s_release_count=0
    r_soft_counter=0
    r_medium_counter=0
    r_hard_counter=0
    r_release_count=0
    e_score=0
    a_score=0
    c_score=0
    i_score=0
    emo_score=0
    squeeze = ''
    header = '../VP/B'+str(counter)
    with open(header+'/sent_data.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if 'release' in row:
                    if 'soft' in squeeze:
                        s_soft_counter+=1
                    elif 'medium' in squeeze:
                        s_medium_counter+=1
                    elif 'hard' in squeeze:
                        s_hard_counter+=1
                    s_release_count +=1
                else:
                    squeeze = row

            csvfile.close()

    with open(header+'/received_data.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if 'release' in row:
                    if 'soft' in squeeze:
                        r_soft_counter+=1
                    elif 'medium' in squeeze:
                        r_medium_counter+=1
                    elif 'hard' in squeeze:
                        r_hard_counter+=1
                    r_release_count +=1
                else:
                    squeeze = row

            csvfile.close()
    for f_name in os.listdir(header):
        if f_name.startswith('Mini5') and f_name.endswith('score.csv'):
            with open(header+'/'+f_name, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        if "Extraversion" in row:
                            e_score = row[1]
                        elif "Agreeableness" in row:
                            a_score = row[1]
                        elif "Conscientiousness" in row:
                            c_score = row[1]
                        elif "Emotional Stability" in row:
                            emo_score = row[1]
                        else:
                            i_score = row[1]
            csvfile.close()

    print('SubectID', counter)
    print('Extraversion', e_score)
    print('Agreeableness', a_score)
    print('Consc.', c_score)
    print('Emotional', emo_score)
    print('Intellect', i_score)
    print('Sent ',s_release_count)
    print('soft', s_soft_counter)
    print('medium', s_medium_counter)
    print('hard', s_hard_counter)
    print('Received ',r_release_count)
    print('soft', r_soft_counter)
    print('medium', r_medium_counter)
    print('hard', r_hard_counter)
    print('Finished')
    csv_writer([[counter,'Male', e_score, a_score,c_score, emo_score, i_score, 'Sent', s_release_count, s_soft_counter, s_medium_counter, s_hard_counter]], 'TouchSummaryMerge.csv')
    csv_writer([[counter,'Male', e_score, a_score,c_score, emo_score, i_score,'Received', r_release_count, r_soft_counter, r_medium_counter, r_hard_counter]], 'TouchSummaryMerge.csv')

    csv_writer([[counter,'Male', s_release_count,r_release_count,s_soft_counter,r_soft_counter,s_medium_counter, r_medium_counter, s_hard_counter,r_hard_counter]], 'TouchSummary.csv')
