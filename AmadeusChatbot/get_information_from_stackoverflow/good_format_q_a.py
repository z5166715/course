'''

this file use the stackoverflow API to get the question-body and answer-body

notice we pull 10000questions and 10000answers,and this API has a restrict of accessing number
,so this file will spend some time


'''


import stackexchange
import json
import time

# user_api_key = 'EAD5DmeOnLNNeLbMyGl8dQ(('
# user_api_key = 'pXlviKYs*UZIwKLPwJGgpg(('
user_api_key = 'D0H4UUZ2UsslobBZmd90wA(('
site = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
site.be_inclusive()
def get_content(question_id, answer_id):
    # user_api_key = 'EAD5DmeOnLNNeLbMyGl8dQ(('
    # user_api_key = 'pXlviKYs*UZIwKLPwJGgpg(('
    # site = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
    # site.be_inclusive()

    question = site.question(question_id)
    answer = site.answer(answer_id)
    # print(question.body)
    # print(answer.body)
    return question.body,answer.body,question.title






with open('q_and_a.json','r') as file:
    content = json.load(file)

start = 0#-----------------------------------------------modify
for number_file in range(0,10):#-----------------------------------------------modify index
    stop = start + 1000
    print(start,stop)


    with open('right_format{}.json'.format(number_file),'w') as f:
        format_dict = {}

        for index in range(start,stop):
            if index % 25 == 0:
                print(index)
                time.sleep(5)
            format_dict[str(index)] = {}
            question_id = content[str(index)]['question_id']
            print(content[str(index)])
            answer_id = content[str(index)]['answer_id']
            # with open('right_format.json','a') as f:
            format_dict[str(index)]['question_id'] = question_id
            format_dict[str(index)]['answer_id'] = answer_id
            format_dict[str(index)]['question'],format_dict[str(index)]['answer'],format_dict[str(index)]['title']\
                = get_content(question_id,answer_id)

        f.write(json.dumps(format_dict,indent=4))


    start = start +1000
