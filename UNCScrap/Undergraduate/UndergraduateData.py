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
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/UNC_UG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/UNC_unordered_undergraduate.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("em"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'University of Newcastle',
               'City': '',
               'Course': '',
               'Faculty': '',
               'Int_Fees': '',
               'Local_Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': '',
               'Full_Time': '',
               'Part_Time': '',
               'Prerequisite_1': 'ATAR',
               'Prerequisite_2': 'IELTS',
               'Prerequisite_3': '',
               'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': '',
               'Prerequisite_3_grade_3': '',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': '',
               'Description': '',
               'Career_Outcomes/path': '',
               'Country': 'Australia',
               'Online': '',
               'Offline': '',
               'Distance': '',
               'Face_to_Face': '',
               'Blended': '',
               'Remarks': ''}

possible_cities = {'newcastle': 'Newcastle',
                   'central coast': 'Central Coast',
                   'sydney': 'Sydney'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

faculty_key = TemplateData.faculty_key  # dictionary of course levels

for each_url in course_links_file:
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(0.1)

    # COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE & course level
    courseName = soup.find('h1', class_='page-header-title')
    if courseName:
        course_level = courseName.find('small').text
        course_title = courseName.text.replace(course_level, "")
        course_data['Course'] = course_title
    else:
        courseName = soup.find('h1', class_="headline-60px inverted-headline")
        course_level = courseName.find('small').text
        course_title = courseName.text.replace(course_level, "")
        course_data['Course'] = course_title

    if '(Honours)' in course_title and 'Bachelor' in course_level:
        course_level = 'Bachelor honours'

    # Description
    degree_details = soup.find(id="degree-details")
    otherDegree = soup.find('div', class_="grid-block")
    degreepre = soup.find('p', class_="replacement-program")

    if degree_details:
        description = degree_details.p.text
        course_data['Description'] = description
    elif otherDegree:
        description = otherDegree.find_next('p').text
        course_data['Description'] = description
    elif degreepre:
        course_data['Description'] = degreepre.text
    else:
        course_data['Description'] = "None"

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_level:
                course_data['Level_Code'] = i

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    # Availability
    country = soup.find('span', class_="region-toggle")
    if '(pre' in course_title:
        course_data['Availability'] = 'N'
        course_data['Int_Fees'] = " "
    else:
        course_data['Availability'] = 'A'

    # Career Outcome
    careerDetails = soup.find(id="tab-career")
    if careerDetails:
        career = careerDetails.find(id="career-opportunities").find('ul')
        career_path = []
        if career:
            li = career.find_all('li')
            if li:
                for element in li:
                    oneCareer = element.text.__str__().strip()
                    if oneCareer:
                        career_path.append(oneCareer)
        career_path = ', '.join(career_path)
        course_data['Career_Outcomes/path'] = career_path
    else:
        course_data['Career_Outcomes/path'] = " "

    factsHeader = soup.find('div', class_="fast-facts-header")
    if factsHeader:
        available = factsHeader.find('nav', class_="fast-fact-toggle").findAll('a')
        for a in available:
            if 'Online' in a.text:
                course_data['Online'] = "Yes"
            else:
                course_data['Online'] = "No"
                tempLine = a.text.lower()
                for i in possible_cities:
                    if i in tempLine:
                        actual_cities.append(possible_cities[i])
                        course_data['Offline'] = "Yes"
                        course_data['Face_to_Face'] = "Yes"

    # Course fees
    try:
        moneyColumn = soup.select("tr:contains('Fees') li")

        if moneyColumn:
            for ea in moneyColumn:
                int_feeRaw = tag_text(ea)
                int_fee = re.findall(currency_pattern, int_feeRaw)[0].replace('AUD', '')
                if int_fee:
                    course_data['Int_Fees'] = int_fee
                else:
                    course_data['Int_Fees'] = " "

    except IndexError:
        course_data['Int_Fees'] = ""

    # print(course_data['Int_Fees'], course_data['Website'])

    try:
        ti = soup.select('.inner div.flex-inner:nth-of-type(3) div:nth-of-type(1) p')
        if ti:
            p_word = ti.__str__().strip().replace('<p>', '').replace('.</p>]', '').strip()

            if 'full-time' in p_word.lower() and 'part-time' not in p_word.lower():
                course_data['Full_Time'] = 'Yes'
            else:
                course_data['Full_Time'] = 'No'
            if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' not in p_word.lower():
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Part_Time'] = 'No'
            if 'full-time' in p_word.lower() and 'part-time' in p_word.lower():
                course_data['Blended'] = 'Yes'
            else:
                course_data['Blended'] = 'No'

            if 'year' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                duration_time = 'Years'
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time
                if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                    duration_time = 'Year'
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = duration_time
                    # print('DURATION + DURATION TIME: ', duration, duration_time)
                elif 'month' in duration_time.__str__().lower():
                    value_conv = DurationConverter.convert_duration(p_word)
                    duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                    duration_time = 'Months'
                    if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                        duration_time = 'Month'
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = duration_time

    except IndexError:
        course_data['Full_Time'] = ''
        course_data['Part_Time'] = ''
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''
        print("this course doesn't have information pertaining to duration")

    # ATAR
    div_right = soup.find('div', class_='atar')
    if div_right:
        Atar = div_right.extract()
        course_data['Prerequisite_1_grade_1'] = tag_text(Atar)
    # print(course_data['Prerequisite_1_grade_1'])
    print(course_data['Course'])
    # IELTS
    ieltsvalue = soup.select('.inner div.flex-inner:nth-of-type(2) li:nth-of-type(1)')
    for a in ieltsvalue:
        raw_ielts = tag_text(a)
        ielts = re.findall(r'\d+\.*\d*', raw_ielts)[0]
        course_data['Prerequisite_2_grade_2'] = ielts

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
                      'Local_Fees',
                      'Int_Fees',
                      'Currency',
                      'Currency_Time',
                      'Duration',
                      'Duration_Time',
                      'Full_Time',
                      'Part_Time',
                      'Prerequisite_1',
                      'Prerequisite_2',
                      'Prerequisite_3',
                      'Prerequisite_1_grade_1',
                      'Prerequisite_2_grade_2',
                      'Prerequisite_3_grade_3',
                      'Website',
                      'Course_Lang',
                      'Availability',
                      'Description',
                      'Career_Outcomes/path',
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

ordered_file = csv_file_path.parent.__str__() + "/UNC_UG_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
