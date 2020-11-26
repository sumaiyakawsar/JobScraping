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
course_links_file_path = course_links_file_path.__str__() + '/Monash_UG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + "/Monash_UG_ordered.csv"


def tag_text(string_):
    return string_.get_text().__str__().strip()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text
        Int_fee = re.search(currency_pattern, int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            course_data['Int_Fees'] = int_fee.replace("$", "").strip()
        else:
            course_data['Int_Fees'] = "Nooooo"


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.strip()


def durationo(p_word):
    try:
        if p_word:

            if 'full time' in p_word.lower() or 'ft' in p_word.lower() and 'part time' not in p_word.lower():
                course_data['Full_Time'] = 'Yes'
            else:
                course_data['Full_Time'] = 'No'

            if 'part time' in p_word.lower() or 'part' in p_word.lower() and 'full time' not in p_word.lower() or 'ft' in p_word.lower():
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Part_Time'] = 'No'

            if 'year' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                duration_time = value_conv[1]

                if str(duration) == '1' or str(duration) == '1.0':
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Year'
                elif 'month' in duration_time.__str__().lower():
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Months'

                else:
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = duration_time

            elif 'month' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                duration_time = value_conv[1]
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time

            elif 'week' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                duration_time = value_conv[1]
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time
            elif 'day' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                course_data['Duration'] = duration
                course_data['Duration_Time'] = 'Days'
                if str(duration) == '1' or str(duration) == '1.0':
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Day'
            else:
                course_data['Duration'] = ""
                course_data['Duration_Time'] = ''
        else:
            course_data['Duration'] = ''
            course_data['Duration_Time'] = ''

    except Exception:
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''


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

number = r"(\d+,\d{3})*\.*\d*"  # Checks for numbers
currency_pattern = rf"\${number}"  # checks for money

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

faculty_key = TemplateData.faculty_key  # dictionary of course levels

for each_url in course_links_file:
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    # lxml is considered to be faster parser compared to html5lib and html.parser
    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(0.1)

    # COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE & Description
    div_left = soup.find('div', class_='grid-col-sm-12 grid-col-md-12-12 banner-course-info')
    course_name = soup.find('div', class_="page-header-courses")
    if div_left:
        course_title = div_left.find('h1').text

        course_level = div_left.h4.text
        if course_title:
            course_data['Course'] = course_title
        else:
            course_data['Course'] = "NA"

        course_description = div_left.p.text
        if course_description:
            course_data['Description'] = course_description.strip()
        else:
            course_data['Description'] = "NA"

    elif course_name:
        course_title = course_name.find("strong", class_="h1").text

        course_level = course_name.find("p", class_="mobile-hidden").text

        if course_title:
            course_data['Course'] = course_title
        else:
            course_data['Course'] = "NA"

        course_description = soup.select(".course-page__summary-text p:nth-of-type(1)")
        if course_description:
            description(course_description)
        else:
            course_data['Description'] = "NA"

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j.lower() in course_level.lower():
                course_data['Level_Code'] = i
                course_data['Course_Level'] = j
    # Course fees
    moneyColumn = soup.select(".tabs__target .grid-col-md-5-9 strong")
    moneyColumn2 = soup.select(".tabs__target .grid-col-md-5-9 p:nth-of-type(3)")
    if moneyColumn:
        int_money_r(moneyColumn)
        if moneyColumn2:
            int_money_r(moneyColumn2)
    else:
        course_data['Int_Fees'] = "N/A"

    # Duration
    ti = soup.select("tr:contains('Duration')")
    if ti:
        for to in ti:
            p_word = to.text.strip().replace("PART 1", "").replace("PART 2", "").replace("2 trimester", "").strip()
            durationo(p_word)

        # AVAILABILITY and LOCATION (and some other bundled data)
    div1 = soup.find('table', class_='course-page__table-basic')
    if div1:
        div2 = div1.find('ul')
        if div2:
            li_all = div2.findAll('li')
            for each_line in li_all:
                tempLine = each_line.text.lower()
                if 'full time' in tempLine or 'ft' in tempLine and 'part time' not in tempLine:
                    course_data['Full_Time'] = 'Yes'
                else:
                    course_data['Full_Time'] = 'No'

                if 'part time' in tempLine or 'part' in tempLine and 'full time' not in tempLine or 'ft' in tempLine:
                    course_data['Part_Time'] = 'Yes'
                else:
                    course_data['Part_Time'] = 'No'

                # LOCATION/CITY
                for i in possible_cities:
                    if i in tempLine:
                        actual_cities.append(possible_cities[i])
    print(course_data['Int_Fees'], course_data['Full_Time'], course_data['Part_Time'], course_data['Website'],
          course_data['Description'])
    # Remark
    # English grade
    div_right = soup.find('div', class_='right-half col-xs-12 col-md-6')
    if div_right:
        EnglishScore = soup.find('div',
                                 class_='text-3xl font-bold w-70px flex-shrink-0 text-bullet-grey roboto-condensed')
        if EnglishScore:
            English = EnglishScore.extract()
            course_data['Prerequisite_1_grade_1'] = tag_text(English)

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

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

browser.quit()

