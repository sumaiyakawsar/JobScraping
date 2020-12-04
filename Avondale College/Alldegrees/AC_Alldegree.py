"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 13-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import csv
import os
import re
import time
import pandas as pd
from pathlib import Path

import DurationConverter
import TemplateData
import bs4 as bs4
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("headless")
option.add_argument('--no-sandbox')
option.add_argument("start-maximized")
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/AC_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/AC_AllCourses.csv'

course_data = {'Level_Code': '', 'University': 'Avondale College', 'City': '', 'Course': '', 'Faculty': '',
               'Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
               'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
               'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': 'Equivalent AQF Level',
               'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
               'Website': '', 'Course_Lang': 'English', 'Availability': '',
               'Description': '', 'Career_Outcomes/path': '', 'Country': 'Australia',
               'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '', 'Remarks': ''
               }

possible_cities = {'lake macquarie': 'Lake Macquarie',
                   'sydney': 'Sydney'
                   }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hidden-lg-up"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def durationo(p_word):
    if p_word:
        if "not offered full-time" in p_word.lower():
            course_data['Full_Time'] = 'No'
        elif 'full-time' in p_word.lower():
            course_data['Full_Time'] = 'Yes'
        else:
            course_data['Full_Time'] = 'No'
        if 'part-time' in p_word.lower() or 'part' in p_word.lower():
            course_data['Part_Time'] = 'Yes'
        else:
            course_data['Part_Time'] = 'No'

        if 'on-campus' in p_word.lower():
            course_data['Offline'] = "Yes"
            course_data['Face_to_Face'] = "Yes"
        else:
            course_data['Offline'] = "No"
            course_data['Face_to_Face'] = "No"
        if 'distance' in p_word.lower():
            course_data['Online'] = "Yes"
            course_data['Distance'] = "Yes"
        else:
            course_data['Online'] = "No"
            course_data['Distance'] = "No"

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
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''
        course_data['Full_Time'] = ""
        course_data['Part_Time'] = ""


def career(course_career):
    career_block = course_career.find_next_sibling("div", class_="tab-block")

    if career_block:
        career = career_block.find_all("li")
        for car in career:
            carr.append(car.text)
            career_options = ', '.join(carr).strip()
            course_data['Career_Outcomes/path'] = career_options


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'Avondale College', 'City': '', 'Course': '', 'Faculty': '',
                   'Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': 'Equivalent AQF Level',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': '',
                   'Description': '', 'Career_Outcomes/path': '', 'Country': 'Australia',
                   'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '', 'Remarks': ''
                   }
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find("h1")
    if course_name:
        course_title = tag_text(course_name)
        course_data['Course'] = course_title

        course_level = course_title
        if "bachelor" in course_level.lower() and "honours" in course_level.lower():
            course_level = "Bachelor honours"
    else:
        course_data['Course'] = ""

    if "outdoor-leadership-short-courses" in course_data['Website']:
        course_name = soup.select_one("span:nth-of-type(2)")
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
        course_level = course_title
    elif "outdoor-leadership" in course_data['Website']:
        course_name = soup.select_one("span.h3:nth-of-type(1)")
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
        course_level = course_title

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

    if "/" in course_data['Course']:
        course_data['Faculty'] = "Double Degree"

    # print(course_data['Course'], course_data['Website'], course_data['Level_Code'],course_data['Faculty'])

    # Description
    course_desc = soup.find("div", id="About")
    course_desccc = soup.find("div", class_="notice")
    if course_desc:
        about_block = course_desc.find_next_sibling("div", class_="tab-block")
        course_data['Description'] = about_block.text.replace("\n", " ").replace("Back to the top", "").strip()
    elif course_desccc:
        course_data['Description'] = course_desccc.text
    else:

        course_data['Description'] = "N/A"

    # Career Outcomes
    course_career = soup.find("div", id="Career-Opportunities")
    course_career2 = soup.find("div", id="Careers")
    carr = []
    if course_career:
        career(course_career)
    elif course_career2:
        career(course_career2)
    else:
        course_data['Career_Outcomes/path'] = "NA"

    # print(course_data['Website'], course_data['Description'],"\n\n\n\n",course_data['Career_Outcomes/path'])

    course_dura = soup.select("tr:contains('Course duration /Study mode') td")
    if course_dura:
        for re in course_dura:
            p_word = re.text.__str__().strip()
            durationo(p_word)
    else:
        course_data['Online'] = "No"
        course_data['Distance'] = "No"
        course_data['Blended'] = "No"
        course_data['Offline'] = "No"
        course_data['Face_to_Face'] = "No"

    if "master of arts" in course_data['Course'].lower():
        coursedura2 = soup.find("div", id="Course-Structure")
        if coursedura2:
            dura_block = coursedura2.find_next_sibling("div", class_="tab-block")
            if dura_block:
                p_word = dura_block.find("p").text
                durationo(p_word)
        course_data['Duration'] = 1.0
        course_data['Duration_Time'] = "Year"
    elif "outdoor leadership" in course_data['Course'].lower():
        course_data['Duration'] = 1.0
        course_data['Duration_Time'] = "Year"
        course_data['Full_Time'] = "Yes"
        course_data['Part_Time'] = "No"
        course_data['Offline'] = "Yes"
        course_data['Face_to_Face'] = "Yes"
        course_data['Online'] = "No"
        course_data['Distance'] = "No"
    else:
        pass

    if "Not for new students" in course_data['Course']:
        course_data['Availability'] = "N"
    else:
        course_data['Availability'] = "A"

    if "Yes" in course_data['Online'] and "Yes" in course_data['Offline']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    course_city = soup.select("tr:contains('Location') td")
    for to in course_city:
        cities = to.text.lower()
        for i in possible_cities:
            if i in cities:
                actual_cities.append(possible_cities[i])
    print(actual_cities, course_data['Website'])

    if "N" in course_data['Availability']:
        course_data['Online'] = "No"
        course_data['Offline'] = "No"
        course_data['Distance'] = "No"
        course_data['Face_to_Face'] = "No"
        course_data['Blended'] = "No"

    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

print(*course_data_all, sep='\n')

desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty',
                      'Fees', 'Currency', 'Currency_Time', 'Duration', 'Duration_Time',
                      'Full_Time', 'Part_Time', 'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3',
                      'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2', 'Prerequisite_3_grade_3',
                      'Website', 'Course_Lang', 'Availability', 'Description', 'Career_Outcomes/path',
                      'Country', 'Online', 'Offline', 'Distance', 'Face_to_Face', 'Blended', 'Remarks']
# tabulate our data
df = pd.DataFrame(course_data_all, columns=desired_order_list)
df.to_csv(csv_file, index=False)

browser.quit()
