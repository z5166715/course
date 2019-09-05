'''
this file pull the question-id and answer-id from stackoverflow and write these as 'q_and_a.json'
in order to facilitate getting right formate questions and answers
'''
from bs4 import BeautifulSoup
import requests
import bs4
import urllib.request
import re
import json

base_url = 'https://stackoverflow.com/questions/tagged/python?sort=frequent&page='
prefix = 'https://stackoverflow.com'
end_url = '&pagesize=50'
page_limit = 200
page_no = 1
index_question = 0

def get_url_content(url):
    file = urllib.request.urlopen(url)
    file.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Chrome/57.0')]
    content = file.read().decode('utf-8')
    soup = bs4.BeautifulSoup(content, "html.parser")
    return soup

def get_id(url,top_question):
    global index_question
    content = get_url_content(url)
    contents = content.find_all(name='div',attrs={'class':'question-summary'})
    for each in contents:
        top_question[index_question] = {}
        each_content_url = each.find(name='a',attrs={'class':'question-hyperlink'}).get('href')
        each_content_url = prefix + each_content_url
        id = re.search('\/(\d+)\/', each_content_url).group(1)
        top_question[index_question]['question_id'] = id
        top_question[index_question]['each_content_url'] = each_content_url
        top_question[index_question]['answer_id'] = get_ans_id(each_content_url)
        index_question += 1
    # print(top_question)
    return top_question

def get_ans_id(url):
    ans_postfix = '?answertab=votes#tab-top'
    whole_url = url + ans_postfix
    content = get_url_content(whole_url)
    if content.find(name='div',attrs={'class':'answer accepted-answer'}):
        answer = content.find(name='div',attrs={'itemprop':'acceptedAnswer'})
    else:
        answer = content.find_all(name='div',attrs={'itemprop':'suggestedAnswer'})[0]
    id = re.search('data-answerid=\"(\d+)\"', str(answer)).group(1)
    print(id,whole_url)
    return id




if __name__ == '__main__':
    top_question = {}
    while page_no <= page_limit:
        page_url = base_url + str(page_no) + end_url
        top_question = get_id(page_url,top_question)
        print('length of dict:   '+str(len(top_question)))
        print("page number:      "+str(page_no))
        page_no += 1
        # break
    with open('q_and_a.json','w',encoding='utf-8') as f:
        f.write(json.dumps(top_question, indent=4))
    # url = 'https://stackoverflow.com/questions/15112125/how-to-test-multiple-variables-against-a-value'
    # get_ans_id(url)