'''
this file is used to insert common information and qapair into database
insert_q_a() is used to insert qapair-id and some information which is not such inportant
update_sql is insert right format questions and answers

'''


import pymysql
import json
import re
import pickle

knowledge_area = 'Information Technology'
with open('data.json','r') as f:
    data = json.load(f)

area_abstract = data[knowledge_area]['abstract']
area_url = data[knowledge_area]['url']

def insert_undergraduate(Undergraduate):
    for course_number in Undergraduate.keys():
        degree = 'Undergraduate'
        course_name = Undergraduate[course_number]['course_name']
        print(course_name)
        course_uoc = Undergraduate[course_number]['course_uoc']
        course_url = Undergraduate[course_number]['course_url']
        course_detail = Undergraduate[course_number]['course_detail']
        course_outline = re.sub('\n','',course_detail['outline'])
        faculty = course_detail['Faculty']
        print(course_number)
        try:
            school = course_detail['School']
        except:
            school = 'None'
        if course_detail['course_term'] != []:
            course_term = course_detail['course_term']
        else:
            course_term = 'None'
        timetable_url = course_detail['timetable_url']
        time_string = 'arrangement:'
        if course_detail['timetable'] != []:
            for each_time in course_detail['timetable']:
                time_string =time_string + each_time + ':' +  course_detail['timetable'][each_time] + ' '
            timetable = time_string
        else:
            timetable = 'None'
        operation = "insert into commoninf(	knowledge_area,area_abstract,area_url,\
                degree,course_number,course_name,course_uoc,course_url,course_outline,\
                faculty,school,course_term,timetable_url,timetable_teacher) values ('{}','{}','{}','{}','{}',\
                '{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(knowledge_area, area_abstract, area_url, \
                         degree, course_number, course_name, course_uoc, course_url, pymysql.escape_string(course_outline), \
                         faculty, school, course_term, timetable_url, pymysql.escape_string(timetable))
        print(operation)
        cursor.execute(operation)
        db.commit()



def insert_postgraduate(Postgraduate):
    for course_number in Postgraduate.keys():
        degree = 'Postgraduate'
        course_name = Postgraduate[course_number]['course_name']
        print(course_name)
        course_uoc = Postgraduate[course_number]['course_uoc']
        course_url = Postgraduate[course_number]['course_url']
        course_detail = Postgraduate[course_number]['course_detail']
        course_outline = re.sub('\n', '', course_detail['outline'])
        faculty = course_detail['Faculty']
        print(course_number)
        try:
            school = course_detail['School']
        except:
            school = 'None'
        if course_detail['course_term'] != []:
            course_term = course_detail['course_term']
        else:
            course_term = 'None'
        timetable_url = course_detail['timetable_url']
        time_string = 'arrangement:'
        if course_detail['timetable'] != []:
            for each_time in course_detail['timetable']:
                time_string = time_string + each_time + ':' + course_detail['timetable'][each_time] + ' '
            timetable = time_string
        else:
            timetable = 'None'
        operation = "insert into commoninf(	knowledge_area,area_abstract,area_url,\
                    degree,course_number,course_name,course_uoc,course_url,course_outline,\
                    faculty,school,course_term,timetable_url,timetable_teacher) values ('{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(knowledge_area, area_abstract, area_url,
                                                                          degree, course_number, course_name, course_uoc,
                                                                          course_url, pymysql.escape_string(course_outline),
                                                                          faculty, school, course_term, timetable_url,
                                                                          pymysql.escape_string(timetable))
        print(operation)
        cursor.execute(operation)
        db.commit()
# db.close()
# cursor.execute('')
def insert_q_a():
    db = pymysql.connect('localhost', 'root', '666666', 'comp9900', charset='utf8')
    cursor = db.cursor()
    degree = 'Postgraduate'
    course_number = 'COMP9021'
    with open('q_and_a.json','r') as f:
        content = json.load(f)
    for each in content:
        print(content[each])
        que_and_ans_index = content[each]['question_id'] + ',' + content[each]['answer_id']
        operation = "insert into questionAndanswer(qapair,degree,course_number,question_title,question_body,answer_body) values \
        ('{}','{}','{}','None','None','None')".format(que_and_ans_index,degree,course_number)
        cursor.execute(operation)
        db.commit()
        break
    db.close()



def updata_sql():
    operation = "update questionAndanswer set question_title = '{}',question_body = '{}' ," \
                "answer_body = '{}' where qapair = '{}'"
    db = pymysql.connect('localhost', 'root', '666666', 'comp9900', charset='utf8')
    cursor = db.cursor()

    for file_number in range(0,9):
        with open('get_information_from_stackoverflow/right_format{}.json'.format(file_number),'r') as f:
            content = json.load(f)
            for each in content.keys():
                pair = content[each]['question_id'] + ',' + content[each]['answer_id']
                # break
                update = operation.format(pymysql.escape_string(content[each]['title']),pymysql.escape_string(content[each]['question'])
                                          ,pymysql.escape_string(content[each]['answer']),pair)
                try:
                    cursor.execute(update)
                    db.commit()
                except:
                    continue
    db.close()
# use comp9900;
# -- create table commoninf(
# -- 	knowledge_area varchar(40),
# --     area_abstract varchar(1000),
# --     area_url varchar(100),
# -- 	degree varchar(40),
# -- 	course_number varchar(40),
# --     course_name varchar(40),
# --     course_uoc varchar(40),
# --     course_url varchar(100),
# --     course_outline varchar(3000),
# -- 	faculty varchar(40),
# --     school varchar(40),
# --     course_term varchar(40),
# --     timetable_url varchar(100),
# --     timetable_teacher varchar(100)
# -- )

if __name__ == '__main__':
    with open('data.json', 'r') as f:
        data = json.load(f)

    Undergraduate = data[knowledge_area]['Undergraduate']
    Postgraduate = data[knowledge_area]['Postgraduate']
    db = pymysql.connect('localhost', 'root', '666666', 'comp9900', charset='utf8')

    cursor = db.cursor()
    insert_undergraduate(Undergraduate)
    insert_postgraduate(Postgraduate)
    db.close()

    insert_q_a()
    updata_sql()
