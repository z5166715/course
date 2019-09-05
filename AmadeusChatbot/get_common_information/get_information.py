'''
this file is used to get the common information about IT from unsw handbook

'''

import bs4
import re
import json
import urllib.request
from get_common_information.page_operation import get_full_page
import time
from selenium import webdriver


prefix = url = 'https://www.handbook.unsw.edu.au'


def get_url_content(url):
    file = urllib.request.urlopen(url)
    file.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Chrome/57.0')]
    content = file.read().decode('utf-8')
    soup = bs4.BeautifulSoup(content, "html.parser")
    return soup



def get_timetable(url):
    course_staff = {}
    soup = get_url_content(url)
    chat = soup.find(name='td',attrs={'class':'classSearchFormBody'}).find_all(name='td',attrs={'class':'data'})
    chat = ' '.join(str(i) for i in chat)
    # print(chat)
    chat = re.sub('\n','',chat)
    # print(chat)
    pattern = re.compile(r'(\<td class\=\"data\"\>(T[1-3]+[A-Z]*|U[1-3]+[A-Z]*|Z[1-3]+[A-Z]*)\<\/td\> <td class="data">([a-zA-Z\'\- ]+)</td>)')
    new_chat = pattern.findall(chat)
    # print(new_chat)
    for i in new_chat:
        course_staff['{}'.format(i[1])] = i[2]

    print(course_staff)
    return course_staff


def get_outline(url):
    course_detail = {}
    soup = get_url_content(url)

    #searching for 'course outline'
    course_outline = soup.find(name='div',attrs={'data-hbui':"readmore__toggle-text",'class':"a-card-text m-toggle-text has-focus"})
    all_content = re.sub('<div class="a-card-text m-toggle-text has-focus" data-hbui="readmore__toggle-text">','',str(course_outline))
    all_content = re.sub('<div>|<p>|</p>|</div>|<em>|</em>|<strong>|</strong>|<br/>','',all_content)
    course_detail['outline'] = all_content

    #searching for 'Faculty' and 'School'
    course_info = soup.find(name='div',attrs={'class':'a-row a-row-equal-height o-attributes-table'})
    pattern = re.compile(r'>[a-zA-Z0-9,()\- ]+<')
    course_info = pattern.findall(str(course_info))
    flag = 0
    for element in course_info:
        if flag == 1:
            course_detail['Faculty'] = element
            flag = 0
        if flag == 2:
            course_detail['School'] = element
            flag = 0
        if element == '>Faculty<':
            flag = 1
        if element == '>School<':
            flag = 2

    #searching for 'offering term'
    course_info_new = soup.find(name='div',attrs={'class':'a-row a-row-equal-height o-attributes-table'})
    term_blank = 0
    course_info_term = course_info_new.find_all(name='p',attrs={'tabindex':'0'})
    if re.search(r'>[a-zA-Z0-9, ]*Term[a-zA-Z0-9, ]*<|>[a-zA-Z0-9, ]*Semester[a-zA-Z0-9, ]*<',str(course_info_new)):
        course_term = re.search(r'>[a-zA-Z0-9, ]*Term[a-zA-Z0-9, ]*<|>[a-zA-Z0-9, ]*Semester[a-zA-Z0-9, ]*<',str(course_info_term)).group()
    else:
        course_term = []
        term_blank = 1
    # print(course_term)
    course_detail['course_term'] = course_term

    #searching for 'timetable url'
    course_timeteble_url = course_info_new.find_all(name='a',attrs={'target':'_blank'})[-1].get('href')
    course_detail['timetable_url'] = course_timeteble_url
    if term_blank == 1:
        course_detail['timetable'] = []
    else:
        course_detail['timetable'] = get_timetable(course_timeteble_url)#'timetable content'

    # print(course_detail)
    return course_detail


def get_page_content(driver,degree):
    content = driver.page_source.encode('utf-8')
    soup = bs4.BeautifulSoup(content, "html.parser")
    try:
        soup = soup.find(name='div',attrs={'id':'{}'.format(degree)})
        course_list = soup.find(name='div',attrs={'id':'subject{}'.format(degree)}).find_all(name='a',attrs={'aria-label':True})
        # print(singleCourse[0])
        print(len(course_list))
        if len(course_list) != 0:
            # print(degree+'......................................')
            course_information = dict()
            for each in course_list:
                course = each.find(name='div',attrs={'class':'section title'}).string
                course_number = each.find(name='div',attrs={'class':'section'}).string
                course_uoc = each.find(name='div',attrs={'class':'section uoc'}).string
                course_url = each.get('href')
                # print(course,course_number,course_uoc,course_url)
                course_information[course_number] = {}
                course_information[course_number]['course_name'] = course
                course_information[course_number]['course_uoc'] = course_uoc
                course_information[course_number]['course_url'] = re.sub('\n','',prefix.strip() + course_url.strip())
                print(course_number)
                course_information[course_number]['course_detail'] = get_outline(course_information[course_number]['course_url'])
            # print(course_information.keys())

        else:
            course_list = soup.find(name='div', attrs={'id': 'subject{}'.format(degree)}).find_all(name='div',attrs={'class':'m-single-course-wrapper-browse'})
            # print(degree+'......................................')
            course_information = dict()
            for each in course_list:
                course_url = each.a.get('href')
                course = each.find(name='p').string
                complex = each.find_all(name='span')
                course_number = complex[1].string
                course_uoc = complex[2].string
                # print(course, course_number, course_uoc, course_url)
                course_information[course_number] = {}
                course_information[course_number]['course_name'] = course
                course_information[course_number]['course_uoc'] = course_uoc
                course_information[course_number]['course_url'] = re.sub('\n','',prefix.strip() + course_url.strip())
                course_information[course_number]['course_detail'] = get_outline(course_information[course_number]['course_url'])
                # print(str(each))
            # print(course_information.keys())
        # print(course_information.keys())
        return course_information
    except:
        pass


def get_all_content(url):
    driver = webdriver.Chrome()
    fields = dict()

    each_area = get_url_content(url).find(name='div',attrs={'id':'tab_field_of_education'}).find_all(name='a')[-2]
    area_name = each_area.find(name='div', attrs={'class': "a-browse-tile-header"}).h3.string
    fields[area_name] = {}
    fields[area_name]['abstract'] = each_area.find(name='div',attrs={'class': "a-browse-tile-content"}).p.string
    fields[area_name]['url'] = re.sub('\n','',(prefix.strip() + each_area.get('href').strip()))
    # driver = webdriver.Chrome()
    url = fields[area_name]['url']
    driver.get(url)
    for degree in ["Undergraduate","Postgraduate","Research"]:
        # driver.get(url)
        webdriver.ActionChains(driver).move_to_element(driver.find_element_by_xpath('//button[@aria-controls="{}"]'.format(degree))).click().perform();
        new_driver = get_full_page(driver)
        course_dict = get_page_content(new_driver,degree)
        fields[area_name][degree] = {}
        fields[area_name][degree] = course_dict
        time.sleep(3)
        print(fields)

    with open('data.json',"w", encoding='utf-8') as f:
        f.write(json.dumps(fields,indent=4))



if __name__ == '__main__':
    get_all_content(url)
    test = 'http://timetable.unsw.edu.au/2019/COMP1511.html'
    # get_timetable(test)
    # chat = '</td> <td class="data">T1</td> <td class="data">Dr AJ Taylor</td> <td class="data">asdadas\t\n\n\n\n\n\n\n\n\n17-MAR-2019</td>Go to Class Detail records'
    # new_chat = re.search(r'\<td class\=\"data\"\>T1\<\/td\>[\n\t]*.*Go to Class Detail records', chat,re.DOTALL).group()
    # print(new_chat)
# test_url = 'https://www.handbook.unsw.edu.au/Undergraduate/courses/2019/ARCH1392/?browseByInterest=68b44253db96df002e4c126b3a961980&'
# get_outline(test_url)


# text = '[<p class="enable-helptext" tabindex="0">Postgraduate</p>, <p class="" tabindex="0">summer--- Term,Term 1,Term 3</p>, <p tabindex="0">'
#
# pattern = re.compile(r'>[a-zA-Z0-9,()\- ]+<')
# course_info = pattern.findall(text)
# print(course_info)