import pandas as pd
import re
import csv


def del_quote(str):
    out_put = re.sub(u"\\<.*?\\>", "", str)
    return out_put

def del_quote2(str):
    punctuation ="><()"
    re_punctuation="[{}]+".format(punctuation)
    out_put = re.sub(re_punctuation, "", str)
    return out_put


def data2csv(data):
    matrix=[]
    count=0


    for i in data:
        row=[]
        for j in i:
            row.append(del_quote(j))
        matrix.append(row)
        count+=1
    for count in range(500,10000,500):
        df=pd.DataFrame(matrix[count-500:count],columns=['question','answer'])
        df.to_csv(f'10000_train_data{count}.csv',index=False)


def data2csv_comm(data):
    matrix=[]
    count=0


    for i in data:
        row=[]
        for j in i:
            row.append(del_quote2(j))
        matrix.append(row)
        count+=1

    with open("comm.csv","w",encoding="utf-8",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["knowledge_area","area_abstract","area_url","degree","course_number","course_name","course_uoc","course_url","course_outline","faculty","School","course term","timetable","teacher"])
        writer.writerows(matrix)
        
