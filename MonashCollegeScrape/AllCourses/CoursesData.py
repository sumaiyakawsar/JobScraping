"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 16-12-20
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
course_links_file_path = course_links_file_path.__str__() + '/Monash_diploma_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/MC_diploma_unordered.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'Monash University',
               'City': '',
               'Course': '',
               'Faculty': '',
               'Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': '',
               'Full_Time': 'Yes',
               'Part_Time': 'No',
               'Prerequisite_1': 'ATAR',
               'Prerequisite_2': 'IELTS',
               'Prerequisite_3': 'Equivalent AQF Degree Level',
               'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': '',
               'Prerequisite_3_grade_3': '',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': 'A',
               'Description': '',
               'Career_Outcomes/path': '',
               'Country': 'Australia',
               'Online': 'No',
               'Offline': '',
               'Distance': 'No',
               'Face_to_Face': '',
               'Blended': 'No',
               'Remarks': ''}

possible_cities = {'docklands': 'Melbourne',
                   'melbourne': 'Melbourne',
                   'clayton': 'Melbourne',
                   'caulfield': 'Melbourne'}

# currency_pattern = "(?:[\£\$\€\(RM)\]{1}[,\d]+.?\d*)"

number = r"(\d+,\d{3})*\.*\d*"  # Checks for numbers
currency_pattern = rf"\${number}"  # checks for money

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

faculty_key = TemplateData.faculty_key  # dictionary of course levels


def career(career_data):
    for each_career in career_data:
        course_data['Career_Outcomes/path'] = tag_text(each_career)


def durationo(p_word):
    if p_word:

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

        elif 'months' in p_word.__str__().lower():
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

        else:
            course_data['Duration'] = "vvv"
            course_data['Duration_Time'] = ''
    else:
        course_data['Duration'] = 'NA'
        course_data['Duration_Time'] = ''
        course_data['Full_Time'] = ""
        course_data['Part_Time'] = ""


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
    course_title = soup.find('h1')
    if course_title:
        course_data['Course'] = course_title.text
    else:
        course_data['Course'] = ""

    course_description = course_title.find_next_sibling("div")

    if course_description:
        course_data['Description'] = course_description.text.strip()
    else:
        course_data['Description'] = "NA"

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # AQF
    aqf_level = soup.select("tr:contains('AQF Level') td")
    for to in aqf_level:
        course_data['Prerequisite_3_grade_3'] = to.text.strip()

    # mode of study
    MOS = soup.select("tr:contains('Mode of study') td")
    for mo in MOS:
        mos = mo.text.strip()
        if "On campus" in mos:
            course_data['Face_to_Face'] = "Yes"
            course_data['Offline'] = "Yes"
        else:
            course_data['Face_to_Face'] = "No"
            course_data['Offline'] = "No"
    # print(course_data['Offline'], course_data['Face_to_Face'], course_data['Website'])

    course_dura = soup.select("tr:contains('Duration') td")
    for re in course_dura:
        p_word = re.text.__str__().strip().replace("Part 1:", "").replace("Part 2:", "").replace("depending on stream",
                                                                                                 "").strip()
        durationo(p_word)
    # print(course_data['Duration'],course_data['Duration_Time'],course_data['Website'])

    # English
    if "Arts" in course_data['Course']:
        course_data['Prerequisite_2_grade_2'] = "6.0"
    else:
        course_data['Prerequisite_2_grade_2'] = "5.5"

    # print(course_data['Prerequisite_2_grade_2'],course_data['Website'])

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    # City
    city = soup.select("tr:contains('Campus') td")
    for each_city in city:
        tempLine = each_city.text.lower()
        # LOCATION/CITY
        for i in possible_cities:
            if i in tempLine:
                actual_cities.append(possible_cities[i])

    career_data = soup.select("#table89236 tr")
    career_data2 = soup.select("#table06540 tr")
    career_data3 = soup.select("#table96826 tr")
    career_data4 = soup.select("#careers_795647 tr")
    career_data5 = soup.select("#table13948 tr")
    career_data6 = soup.select("#table95002 tr")
    career_data7 = soup.select("#careers_797121 tr")
    if career_data:
        career(career_data)
    elif career_data2:
        career(career_data2)
    elif career_data3:
        career(career_data3)
    elif career_data4:
        career(career_data4)
    elif career_data5:
        career(career_data5)
    elif career_data6:
        career(career_data6)
    elif career_data7:
        career(career_data7)
    else:
        course_data['Career_Outcomes/path'] = "?"


    print(course_data['Career_Outcomes/path'], course_data['Website'])

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
                      'Fees',
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

ordered_file = csv_file_path.parent.__str__() + "/MC_diploma_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)


browser.quit()
