"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
from bs4 import Comment
import requests
import os
import copy
import DurationConverter
import TemplateData


def get_page(url):
    """Will download the contents of the page using the requests library.
    :return: a BeautifulSoup object i.e. the content of the webpage related to the given URL.
    """
    # noinspection PyBroadException,PyUnusedLocal
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return bs4.BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        pass
    return None

# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument('--no-sandbox')
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/Monash_undergraduate_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/Monash_undergraduate.csv'

def tag_text(string_):
    return string_.get_text().__str__().strip()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

course_data = {'Level_Code': '',
               'University': 'Monash University',
               'City': '',
               'Course': '',
               'Faculty': '',
               'Int_Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': '',
               'Full_Time': '',
               'Part_Time': '',
               'Prerequisite_1': 'IELTS',
               'Prerequisite_2': 'Equivalent AQF Degree Level',
               'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': 'Year 12',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': 'A',
               'Description': '',
               'Country': 'Australia',
               'Online': 'No',
               'Offline': 'Yes',
               'Distance': 'No',
               'Face_to_Face': 'Yes',
               'Blended': 'No',
               'Remarks': ''}

possible_cities = {'canberra': 'Canberra',
                   'melbourne': 'Melbourne',
                   'clayton': 'Melbourne',
                   'caulfield': 'Melbourne',
                   'peninsula': 'Melbourne'}

currency_pattern = "(?:[\£\$\€\(RM)\]{1}[,\d]+.?\d*)"
course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

faculty_key = TemplateData.faculty_key  # dictionary of course levels

for each_url in course_links_file:
    actual_cities = []

    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'html.parser')
    time.sleep(0.1)

    # COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE & Description
    div_left = soup.find('div', class_='grid-col-sm-12 grid-col-md-12-12 banner-course-info')
    if div_left:
        course_title = soup.find('h1').text
        course_description = div_left.p.text
        course_level = div_left.h4.text

        course_data['Course'] = course_title
        if course_description:
            course_data['Description'] = course_description.strip()
    #English grade
    div_right = soup.find('div', class_='right-half col-xs-12 col-md-6')
    if div_right:
        EnglishScore = soup.find('div', class_='text-3xl font-bold w-70px flex-shrink-0 text-bullet-grey roboto-condensed')
        if EnglishScore:
            English = EnglishScore.extract()
            course_data['Prerequisite_1_grade_1'] = tag_text(English)

    # Course fees
    moneyColumn = soup.select(".tabs__target .grid-col-md-5-9 strong")
    if moneyColumn:
        courseFee = moneyColumn.__str__().strip()\
                                .replace('[<strong>A$', '')\
                                .replace('</strong>]', '')\
                                .replace('-1', '').strip()
        course_data['Int_Fees'] = courseFee
    #print(course_data['Int_Fees'])

    #Duration
    try:
        ti = soup.select("tr:contains('Duration') li")
        if ti:
            p_word = ti.__str__().strip().replace("","")\
                .replace("\n",'').strip()
            if 'full time' in p_word.lower() and 'part time' not in p_word.lower():
                course_data['Full_Time'] = 'Yes'
            else:
                course_data['Full_Time'] = 'No'
            if 'part time' in p_word.lower() or 'part' in p_word.lower() and 'full time' not in p_word.lower():
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Part_Time'] = 'No'
            if 'full time' in p_word.lower() and 'part time' in p_word.lower():
                course_data['Blended'] = 'Yes'
            else:
                course_data['Blended'] = 'No'
            #print(course_data['Full_Time'],course_data['Part_Time'],course_data['Blended'])
            if 'year' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(
                    ''.join(filter(str.isdigit, str(value_conv)))[0])
                duration_time = 'Years'
                if str(duration) == '1' or str(duration) == '1.00' or str(
                        duration) == '1.0':
                    duration_time = 'Year'
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time
                # print('DURATION + DURATION TIME: ', duration, duration_time)

            elif 'month' in duration_time.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(
                    ''.join(filter(str.isdigit, str(value_conv)))[0])
                duration_time = 'Months'
                if str(duration) == '1' or str(duration) == '1.00' or str(
                        duration) == '1.0':
                    duration_time = 'Month'
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time

    except IndexError:
        course_data['Full_Time'] = ''
        course_data['Part_Time'] = ''
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''
        print("this course doesn't have information pertaining to duration")
    #print(course_data['Duration'])

 # AVAILABILITY and LOCATION (and some other bundled data)
    div1 = soup.find('table', class_='course-page__table-basic')
    if div1:
        div2 = div1.find('ul')
        if div2:
            li_all = div2.findAll('li')
            for each_line in li_all:
                tempLine = each_line.text.lower()
     # LOCATION/CITY
                for i in possible_cities:
                    if i in tempLine:
                        actual_cities.append(possible_cities[i])
            #print('CITY: ', actual_cities

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_level:
                course_data['Level_Code'] = i
                course_data['Course_Level'] = j

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    if 'Course_Level' in course_data:
        del course_data['Course_Level']


    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

print(*course_data_all, sep='\n')
desired_order_list = ['Level_Code',
               'University',
               'City',
               'Course',
               'Faculty',
               'Int_Fees',
               'Currency',
               'Currency_Time',
               'Duration',
               'Duration_Time',
               'Full_Time',
               'Part_Time',
               'Prerequisite_1',
               'Prerequisite_2',
               'Prerequisite_1_grade_1',
               'Prerequisite_2_grade_2',
               'Website',
               'Course_Lang',
               'Availability',
               'Description',
               'Country',
               'Online',
               'Offline',
               'Distance',
               'Face_to_Face',
               'Blended',
               'Remarks']
# tabulate our data
course_dict_keys = set().union(*(d.keys() for d in course_data_all))

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, course_dict_keys)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

ordered_file = csv_file_path.parent.__str__() + "/Monash_UG_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)
