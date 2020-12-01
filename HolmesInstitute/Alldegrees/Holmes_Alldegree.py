"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 30-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import csv
import os
import time
from pathlib import Path

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
course_links_file_path = course_links_file_path.__str__() + '/Holmes_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/Holmes_allcourses.csv'

course_data = {'Level_Code': '', 'University': 'Holmes Institute', 'City': '',
               'Course': '', 'Faculty': '', 'Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
               'Duration': '', 'Duration_Time': '', 'Full_Time': 'Yes', 'Part_Time': 'No',
               'Prerequisite_1': '', 'Prerequisite_2': '', 'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '',
               'Website': '', 'Course_Lang': 'English', 'Availability': 'A',
               'Description': '', 'Career_Outcomes/path': '', 'Country': 'Australia',
               'Online': 'No', 'Offline': 'Yes', 'Distance': 'No', 'Face_to_Face': 'Yes', 'Blended': 'No',
               'Remarks': '',
               'Subjects_or_Units_1': '', 'Subjects_or_Units_2': '', 'Subjects_or_Units_3': '',
               'Subjects_or_Units_4': '', 'Subjects_or_Units_5': '', 'Subjects_or_Units_6': '',
               'Subjects_or_Units_7': '', 'Subjects_or_Units_8': '', 'Subjects_or_Units_9': '',
               'Subjects_or_Units_10': '', 'Subjects_or_Units_11': '', 'Subjects_or_Units_12': '',
               'Subjects_or_Units_13': '', 'Subjects_or_Units_14': '', 'Subjects_or_Units_15': '',
               'Subjects_or_Units_16': '', 'Subjects_or_Units_17': '', 'Subjects_or_Units_18': '',
               'Subjects_or_Units_19': '', 'Subjects_or_Units_20': '', 'Subjects_or_Units_21': '',
               'Subjects_or_Units_22': '', 'Subjects_or_Units_23': '', 'Subjects_or_Units_24': '',
               'Subjects_or_Units_25': '', 'Subjects_or_Units_26': '', 'Subjects_or_Units_27': '',
               'Subjects_or_Units_28': '', 'Subjects_or_Units_29': '', 'Subjects_or_Units_30': '',
               'Subject_Objective_1': '', 'Subject_Objective_2': '', 'Subject_Objective_3': '',
               'Subject_Objective_4': '', 'Subject_Objective_5': '', 'Subject_Objective_6': '',
               'Subject_Objective_7': '', 'Subject_Objective_8': '', 'Subject_Objective_9': '',
               'Subject_Objective_10': '', 'Subject_Objective_11': '', 'Subject_Objective_12': '',
               'Subject_Objective_13': '', 'Subject_Objective_14': '', 'Subject_Objective_15': '',
               'Subject_Objective_16': '', 'Subject_Objective_17': '', 'Subject_Objective_18': '',
               'Subject_Objective_19': '', 'Subject_Objective_20': '', 'Subject_Objective_21': '',
               'Subject_Objective_22': '', 'Subject_Objective_23': '', 'Subject_Objective_24': '',
               'Subject_Objective_25': '', 'Subject_Objective_26': '', 'Subject_Objective_27': '',
               'Subject_Objective_28': '', 'Subject_Objective_29': '', 'Subject_Objective_30': '',
               'Subject_Description_1': '', 'Subject_Description_2': '', 'Subject_Description_3': '',
               'Subject_Description_4': '', 'Subject_Description_5': '', 'Subject_Description_6': '',
               'Subject_Description_7': '', 'Subject_Description_8': '', 'Subject_Description_9': '',
               'Subject_Description_10': '', 'Subject_Description_11': '', 'Subject_Description_12': '',
               'Subject_Description_13': '', 'Subject_Description_14': '', 'Subject_Description_15': '',
               'Subject_Description_16': '', 'Subject_Description_17': '', 'Subject_Description_18': '',
               'Subject_Description_19': '', 'Subject_Description_20': '', 'Subject_Description_21': '',
               'Subject_Description_22': '', 'Subject_Description_23': '', 'Subject_Description_24': '',
               'Subject_Description_25': '', 'Subject_Description_26': '', 'Subject_Description_27': '',
               'Subject_Description_28': '', 'Subject_Description_29': '', 'Subject_Description_30': ''
               }

possible_cities = {'sydney': 'Sydney',
                   'melbourne': 'Melbourne',
                   'brisbane': 'Brisbane',
                   'gold coast': 'Gold Coast'
                   }

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels


def tag_text(string_):
    return string_.get_text().__str__().strip()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.replace("\n", "").strip()


for each_url in course_links_file:
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    courses = []
    course_description = []

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find(id="content_page_item").find("h1")
    if course_name:
        course_title = tag_text(course_name).strip().split("(")
        course_data['Course'] = course_title[0]
    else:
        course_data['Course'] = ""

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Description
    course_desc = soup.select("#content_page_item > p:nth-of-type(1)")
    if "Bachelor of Business" in course_data['Course']:
        description(course_desc)
        course_data['Duration'] = 3
        course_data['Duration_Time'] = "Years"

        course_data['Fees'] = 55200

        table_course = soup.select("p:nth-of-type(n+21) strong")
        for so in table_course:
            coccoc = so.text. \
                replace("HC1010 - ", "").replace("HC1021 - ", "").replace("HC1031 - ", ""). \
                replace("HC1041 - ", "").replace("HC1052 - ", "").replace("HC1062 - ", ""). \
                replace("HC1072 - ", "").replace("HC1082 - ", "").replace("HC2022 - ", ""). \
                replace("HC2101 - ", "").replace("HC2112 - ", "").replace("HC3131 - ", ""). \
                replace("HC3141 - ", "").replace("HC3152 - ", "").replace("HC2121 - ", ""). \
                replace("HI2011 - ", "").replace("HC2091 - ", "").replace("HI3021 - ", ""). \
                replace("HI3042 - ", "").replace("HK2011 - ", "").replace("HK3031 - ", ""). \
                replace("HK3041 - ", "").replace("HI3031 - ", "").replace("HK3052 - ", ""). \
                replace("HM2011 - ", "").replace("HM2022 - ", "").replace("HM3041 - ", "").strip()
            courses.append(coccoc)

        strong = soup.select("p:nth-of-type(n+21)")
        for so in strong:
            course_description.append(so.text)

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_description[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[2]:
            course_data['Subject_Objective_3'] = course_description[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[3]:
            course_data['Subject_Objective_4'] = course_description[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[4]:
            course_data['Subject_Objective_5'] = course_description[4]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[5]:
            course_data['Subject_Objective_6'] = course_description[5]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[6]:
            course_data['Subject_Objective_7'] = course_description[6]
        course_data['Subjects_or_Units_8'] = courses[7]
        if course_data['Subjects_or_Units_8'] in course_description[7]:
            course_data['Subject_Objective_8'] = course_description[7]
        course_data['Subjects_or_Units_9'] = courses[8]
        if course_data['Subjects_or_Units_9'] in course_description[8]:
            course_data['Subject_Objective_9'] = course_description[8]
        course_data['Subjects_or_Units_10'] = courses[9]
        if course_data['Subjects_or_Units_10'] in course_description[9]:
            course_data['Subject_Objective_10'] = course_description[9]
        course_data['Subjects_or_Units_11'] = courses[10]
        if course_data['Subjects_or_Units_11'] in course_description[10]:
            course_data['Subject_Objective_11'] = course_description[10]
        course_data['Subjects_or_Units_12'] = courses[11]
        if course_data['Subjects_or_Units_12'] in course_description[11]:
            course_data['Subject_Objective_12'] = course_description[11]
        course_data['Subjects_or_Units_13'] = courses[12]
        if course_data['Subjects_or_Units_13'] in course_description[12]:
            course_data['Subject_Objective_13'] = course_description[12]
        course_data['Subjects_or_Units_14'] = courses[13]
        if course_data['Subjects_or_Units_14'] in course_description[13]:
            course_data['Subject_Objective_14'] = course_description[13]
        course_data['Subjects_or_Units_15'] = courses[14]
        if course_data['Subjects_or_Units_15'] in course_description[14]:
            course_data['Subject_Objective_15'] = course_description[14]
        course_data['Subjects_or_Units_16'] = courses[15]
        if course_data['Subjects_or_Units_16'] in course_description[15]:
            course_data['Subject_Objective_16'] = course_description[15]
        course_data['Subjects_or_Units_17'] = courses[16]
        if course_data['Subjects_or_Units_17'] in course_description[16]:
            course_data['Subject_Objective_17'] = course_description[16]
        course_data['Subjects_or_Units_18'] = courses[17]
        if course_data['Subjects_or_Units_18'] in course_description[17]:
            course_data['Subject_Objective_18'] = course_description[17]
        course_data['Subjects_or_Units_19'] = courses[18]
        if course_data['Subjects_or_Units_19'] in course_description[18]:
            course_data['Subject_Objective_19'] = course_description[18]
        course_data['Subjects_or_Units_20'] = courses[19]
        if course_data['Subjects_or_Units_20'] in course_description[19]:
            course_data['Subject_Objective_20'] = course_description[19]
        course_data['Subjects_or_Units_21'] = courses[20]
        if course_data['Subjects_or_Units_21'] in course_description[20]:
            course_data['Subject_Objective_21'] = course_description[20]
        course_data['Subjects_or_Units_22'] = courses[21]
        if course_data['Subjects_or_Units_22'] in course_description[21]:
            course_data['Subject_Objective_22'] = course_description[21]
        course_data['Subjects_or_Units_23'] = courses[22]
        if course_data['Subjects_or_Units_23'] in course_description[22]:
            course_data['Subject_Objective_23'] = course_description[22]
        course_data['Subjects_or_Units_24'] = courses[23]
        if course_data['Subjects_or_Units_24'] in course_description[23]:
            course_data['Subject_Objective_24'] = course_description[23]
        course_data['Subjects_or_Units_25'] = courses[24]
        if course_data['Subjects_or_Units_25'] in course_description[24]:
            course_data['Subject_Objective_25'] = course_description[24]
        course_data['Subjects_or_Units_26'] = courses[25]
        if course_data['Subjects_or_Units_26'] in course_description[25]:
            course_data['Subject_Objective_26'] = course_description[25]
        course_data['Subjects_or_Units_27'] = courses[26]
        if course_data['Subjects_or_Units_27'] in course_description[26]:
            course_data['Subject_Objective_27'] = course_description[26]
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subject_Objective_30'] = ''

        cities = soup.select("[width] tr:nth-of-type(n+2) td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    elif "Bachelor of Professional Accounting" in course_data['Course']:
        description(course_desc)

        course_data['Duration'] = 3
        course_data['Duration_Time'] = "Years"

        course_data['Fees'] = 55200

        career = soup.select("#content_page_item p:nth-of-type(2)")
        if career:
            for car in career:
                course_data['Career_Outcomes/path'] = car.text

        table_course = soup.select("strong")
        for so in table_course:
            coccoc = so.text.replace("HA1011 - ", "").replace("HA1022 - ", "").replace("HA2011 - ", ""). \
                replace("HA2032 – ", "").replace("HA2022 - ", "").replace("HA2042 - ", "").replace("HA3021 - ", ""). \
                replace("HS2031", "").replace("HA3032 - ", "").replace("HA3011 - ", "").replace("HA3042  - ", ""). \
                replace("HA3042  - ", "").replace("HA1020 – ", "").replace("HC1010 – ", "").replace("HC2091 - ", ""). \
                replace("HC1072 – ", "").replace("HC2121 - ", "").strip()
            courses.append(coccoc)

        strong = soup.select("p:nth-of-type(n+7)")
        for so in strong:
            course_description.append(so.text)

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_description[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[2]:
            course_data['Subject_Objective_3'] = course_description[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[3]:
            course_data['Subject_Objective_4'] = course_description[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[4]:
            course_data['Subject_Objective_5'] = course_description[4]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[5]:
            course_data['Subject_Objective_6'] = course_description[5]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[6]:
            course_data['Subject_Objective_7'] = course_description[6]
        course_data['Subjects_or_Units_8'] = courses[7]
        if course_data['Subjects_or_Units_8'] in course_description[7]:
            course_data['Subject_Objective_8'] = course_description[7]
        course_data['Subjects_or_Units_9'] = courses[8]
        if course_data['Subjects_or_Units_9'] in course_description[8]:
            course_data['Subject_Objective_9'] = course_description[8]
        course_data['Subjects_or_Units_10'] = courses[9]
        if course_data['Subjects_or_Units_10'] in course_description[9]:
            course_data['Subject_Objective_10'] = course_description[9]
        course_data['Subjects_or_Units_11'] = courses[10]
        if course_data['Subjects_or_Units_11'] in course_description[10]:
            course_data['Subject_Objective_11'] = course_description[10]
        course_data['Subjects_or_Units_12'] = courses[11]
        if course_data['Subjects_or_Units_12'] in course_description[11]:
            course_data['Subject_Objective_12'] = course_description[11]
        course_data['Subjects_or_Units_13'] = courses[12]
        if course_data['Subjects_or_Units_13'] in course_description[12]:
            course_data['Subject_Objective_13'] = course_description[12]
        course_data['Subjects_or_Units_14'] = courses[13]
        if course_data['Subjects_or_Units_14'] in course_description[13]:
            course_data['Subject_Objective_14'] = course_description[13]
        course_data['Subjects_or_Units_15'] = courses[14]
        if course_data['Subjects_or_Units_15'] in course_description[14]:
            course_data['Subject_Objective_15'] = course_description[14]
        course_data['Subjects_or_Units_16'] = ""
        course_data['Subjects_or_Units_17'] = ""
        course_data['Subjects_or_Units_18'] = ""
        course_data['Subjects_or_Units_19'] = ""
        course_data['Subjects_or_Units_20'] = ""
        course_data['Subjects_or_Units_21'] = ""
        course_data['Subjects_or_Units_22'] = ''
        course_data['Subjects_or_Units_23'] = ''
        course_data['Subjects_or_Units_24'] = ''
        course_data['Subjects_or_Units_25'] = ''
        course_data['Subjects_or_Units_26'] = ''
        course_data['Subjects_or_Units_27'] = ''
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_16'] = ''
        course_data['Subject_Objective_17'] = ''
        course_data['Subject_Objective_18'] = ''
        course_data['Subject_Objective_19'] = ''
        course_data['Subject_Objective_20'] = ''
        course_data['Subject_Objective_21'] = ''
        course_data['Subject_Objective_22'] = ''
        course_data['Subject_Objective_23'] = ''
        course_data['Subject_Objective_24'] = ''
        course_data['Subject_Objective_25'] = ''
        course_data['Subject_Objective_26'] = ''
        course_data['Subject_Objective_27'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subject_Objective_30'] = ''

        cities = soup.select("[width] tr:nth-of-type(n+2) td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])

    elif "Bachelor of Information Systems" in course_data['Course']:
        description(course_desc)
        course_data['Duration'] = 3
        course_data['Duration_Time'] = "Years"
        course_data['Fees'] = 55200
        table_course = soup.select("p:nth-of-type(n+7) strong")
        for so in table_course:
            coccoc = so.text.replace("HS1011", "").replace("HS1021", "").replace("HC1031", "").replace("HC1062", ""). \
                replace("HC1041", "").replace("HS2011", "").replace("HS2021", "").replace("HS2031", "") \
                .replace("HS2041", "").replace("HC2051", "").replace("HS2061", "").replace("HC3152", ""). \
                replace("HS3011", "").replace("HS3021", "").replace("HS3031", "").replace("HS3041", "").replace(
                "HC1052", ""). \
                replace("HC2121", "").strip()
            # print(coccoc)
            courses.append(coccoc)
        strong = soup.select("p:nth-of-type(n+7)")
        for so in strong:
            course_description.append(so.text)

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_description[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[2]:
            course_data['Subject_Objective_3'] = course_description[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[3]:
            course_data['Subject_Objective_4'] = course_description[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[7]:
            course_data['Subject_Objective_5'] = course_description[7]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[8]:
            course_data['Subject_Objective_6'] = course_description[8]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[9]:
            course_data['Subject_Objective_7'] = course_description[9]
        course_data['Subjects_or_Units_8'] = courses[7]
        if course_data['Subjects_or_Units_8'] in course_description[10]:
            course_data['Subject_Objective_8'] = course_description[10]
        course_data['Subjects_or_Units_9'] = courses[8]
        if course_data['Subjects_or_Units_9'] in course_description[11]:
            course_data['Subject_Objective_9'] = course_description[11]
        course_data['Subjects_or_Units_10'] = courses[9]
        if course_data['Subjects_or_Units_10'] in course_description[12]:
            course_data['Subject_Objective_10'] = course_description[12]
        course_data['Subjects_or_Units_11'] = courses[10]
        if course_data['Subjects_or_Units_11'] in course_description[13]:
            course_data['Subject_Objective_11'] = course_description[13]
        course_data['Subjects_or_Units_12'] = courses[11]
        if course_data['Subjects_or_Units_12'] in course_description[14]:
            course_data['Subject_Objective_12'] = course_description[14]
        course_data['Subjects_or_Units_13'] = courses[12]
        if course_data['Subjects_or_Units_13'] in course_description[15]:
            course_data['Subject_Objective_13'] = course_description[15]
        course_data['Subjects_or_Units_14'] = courses[13]
        if course_data['Subjects_or_Units_14'] in course_description[17]:
            course_data['Subject_Objective_14'] = course_description[17]
        course_data['Subjects_or_Units_15'] = courses[14]
        if course_data['Subjects_or_Units_15'] in course_description[18]:
            course_data['Subject_Objective_15'] = course_description[18]
        course_data['Subjects_or_Units_16'] = courses[15]
        if course_data['Subjects_or_Units_16'] in course_description[19]:
            course_data['Subject_Objective_16'] = course_description[19]
        course_data['Subjects_or_Units_17'] = courses[16]
        if course_data['Subjects_or_Units_17'] in course_description[22]:
            course_data['Subject_Objective_17'] = course_description[22]
        course_data['Subjects_or_Units_18'] = courses[17]
        if course_data['Subjects_or_Units_18'] in course_description[23]:
            course_data['Subject_Objective_18'] = course_description[23]
        course_data['Subjects_or_Units_19'] = courses[18]
        if course_data['Subjects_or_Units_19'] in course_description[24]:
            course_data['Subject_Objective_19'] = course_description[24]
        course_data['Subjects_or_Units_20'] = courses[19]
        if course_data['Subjects_or_Units_20'] in course_description[26]:
            course_data['Subject_Objective_20'] = course_description[26]
        course_data['Subjects_or_Units_21'] = courses[20]
        if course_data['Subjects_or_Units_21'] in course_description[27]:
            course_data['Subject_Objective_21'] = course_description[27]
        course_data['Subjects_or_Units_22'] = ''
        course_data['Subject_Objective_22'] = ''
        course_data['Subjects_or_Units_23'] = ''
        course_data['Subject_Objective_23'] = ''
        course_data['Subjects_or_Units_24'] = ''
        course_data['Subject_Objective_24'] = ''
        course_data['Subjects_or_Units_25'] = ''
        course_data['Subject_Objective_25'] = ''
        course_data['Subjects_or_Units_26'] = ''
        course_data['Subject_Objective_26'] = ''
        course_data['Subjects_or_Units_27'] = ''
        course_data['Subject_Objective_27'] = ''
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_30'] = ''

        cities = soup.select("[width='630'] td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    elif "Graduate Diploma in Business" in course_data['Course']:
        description(course_desc)

        # Duration
        course_data['Duration'] = 1
        course_data['Duration_Time'] = "Year"
        course_data['Fees'] = 19200

        table_course = soup.select("tr:nth-of-type(n+2) td:nth-of-type(2)")
        for so in table_course:
            courses.append(so.text)

        strong = soup.select("p:nth-of-type(n+10)")
        for so in strong:
            course_description.append(so.text)

        course_ex = course_description[1].split("HI")

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_ex[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[1]:
            course_data['Subject_Objective_3'] = course_ex[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[1]:
            course_data['Subject_Objective_4'] = course_ex[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[2]:
            course_data['Subject_Objective_5'] = course_description[2]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[3]:
            course_data['Subject_Objective_6'] = course_description[3]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[4]:
            course_data['Subject_Objective_7'] = course_description[4]
        course_data['Subjects_or_Units_8'] = courses[7]
        if course_data['Subjects_or_Units_8'] in course_description[5]:
            course_data['Subject_Objective_8'] = course_description[5]
        course_data['Subjects_or_Units_9'] = courses[8]
        if course_data['Subjects_or_Units_9'] in course_description[6]:
            course_data['Subject_Objective_9'] = course_description[6]
        course_data['Subjects_or_Units_10'] = courses[9]
        if course_data['Subjects_or_Units_10'] in course_description[7]:
            course_data['Subject_Objective_10'] = course_description[7]
        course_data['Subjects_or_Units_11'] = courses[10]
        if course_data['Subjects_or_Units_11'] in course_description[8]:
            course_data['Subject_Objective_11'] = course_description[8]
        course_data['Subjects_or_Units_12'] = courses[11]
        if course_data['Subjects_or_Units_12'] in course_description[9]:
            course_data['Subject_Objective_12'] = course_description[9]
        course_data['Subjects_or_Units_13'] = courses[12]
        if course_data['Subjects_or_Units_13'] in course_description[10]:
            course_data['Subject_Objective_13'] = course_description[10]
        course_data['Subjects_or_Units_14'] = courses[13]
        if course_data['Subjects_or_Units_14'] in course_description[11]:
            course_data['Subject_Objective_14'] = course_description[11]
        course_data['Subjects_or_Units_15'] = courses[14]
        if course_data['Subjects_or_Units_15'] in course_description[12]:
            course_data['Subject_Objective_15'] = course_description[12]
        course_data['Subjects_or_Units_16'] = courses[15]
        if course_data['Subjects_or_Units_16'] in course_description[13]:
            course_data['Subject_Objective_16'] = course_description[13]
        course_data['Subjects_or_Units_17'] = courses[16]
        if course_data['Subjects_or_Units_17'] in course_description[14]:
            course_data['Subject_Objective_17'] = course_description[14]
        course_data['Subjects_or_Units_18'] = courses[17]
        if course_data['Subjects_or_Units_18'] in course_description[15]:
            course_data['Subject_Objective_18'] = course_description[15]
        course_data['Subjects_or_Units_19'] = courses[18]
        if course_data['Subjects_or_Units_19'] in course_description[16]:
            course_data['Subject_Objective_19'] = course_description[16]
        course_data['Subjects_or_Units_20'] = ""
        course_data['Subject_Objective_20'] = ''
        course_data['Subjects_or_Units_21'] = ""
        course_data['Subject_Objective_21'] = ''
        course_data['Subjects_or_Units_22'] = ''
        course_data['Subject_Objective_22'] = ''
        course_data['Subjects_or_Units_23'] = ''
        course_data['Subject_Objective_23'] = ''
        course_data['Subjects_or_Units_24'] = ''
        course_data['Subject_Objective_24'] = ''
        course_data['Subjects_or_Units_25'] = ''
        course_data['Subject_Objective_25'] = ''
        course_data['Subjects_or_Units_26'] = ''
        course_data['Subject_Objective_26'] = ''
        course_data['Subjects_or_Units_27'] = ''
        course_data['Subject_Objective_27'] = ''
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_30'] = ''

        cities = soup.select("[width='593'] td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])

    elif "Master of Business Administration" in course_data['Course']:

        description(course_desc)

        course_data['Duration'] = 1
        course_data['Duration_Time'] = "Year"

        course_data['Fees'] = 28800

        table_course = soup.select("tr:nth-of-type(n+2) td:nth-of-type(2)")
        for so in table_course:
            courses.append(so.text)

        strong = soup.select("p:nth-of-type(n+14)")
        for so in strong:
            course_description.append(so.text)

        course_des1 = course_description[1].split("HI")
        course_des7 = course_description[7].split("HI")
        course_des9 = course_description[9].split("HI")
        course_des11 = course_description[11].split("HI")

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_des1[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[1]:
            course_data['Subject_Objective_3'] = course_des1[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[1]:
            course_data['Subject_Objective_4'] = course_des1[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[2]:
            course_data['Subject_Objective_5'] = course_description[2]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[3]:
            course_data['Subject_Objective_6'] = course_description[3]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[4]:
            course_data['Subject_Objective_7'] = course_description[4]
        course_data['Subjects_or_Units_8'] = courses[7]
        if course_data['Subjects_or_Units_8'] in course_description[5]:
            course_data['Subject_Objective_8'] = course_description[5]
        course_data['Subjects_or_Units_9'] = courses[8]
        if course_data['Subjects_or_Units_9'] in course_description[6]:
            course_data['Subject_Objective_9'] = course_description[6]
        course_data['Subjects_or_Units_10'] = courses[9]
        if course_data['Subjects_or_Units_10'] in course_description[7]:
            course_data['Subject_Objective_10'] = course_des7[1]
        course_data['Subjects_or_Units_11'] = courses[10]
        if course_data['Subjects_or_Units_11'] in course_description[7]:
            course_data['Subject_Objective_11'] = course_des7[2]
        course_data['Subjects_or_Units_12'] = courses[11]
        if course_data['Subjects_or_Units_12'] in course_description[7]:
            course_data['Subject_Objective_12'] = course_des7[3]
        course_data['Subjects_or_Units_13'] = courses[12]
        if course_data['Subjects_or_Units_13'] in course_description[8]:
            course_data['Subject_Objective_13'] = course_description[8]
        course_data['Subjects_or_Units_14'] = courses[13]
        if course_data['Subjects_or_Units_14'] in course_description[9]:
            course_data['Subject_Objective_14'] = course_des9[1]
        course_data['Subjects_or_Units_15'] = courses[14]
        if course_data['Subjects_or_Units_15'] in course_description[9]:
            course_data['Subject_Objective_15'] = course_des9[2]
        course_data['Subjects_or_Units_16'] = courses[15]
        if course_data['Subjects_or_Units_16'] in course_description[9]:
            course_data['Subject_Objective_16'] = course_des9[3]
        course_data['Subjects_or_Units_17'] = courses[16]
        if course_data['Subjects_or_Units_17'] in course_description[10]:
            course_data['Subject_Objective_17'] = course_description[10]
        course_data['Subjects_or_Units_18'] = courses[17]
        if course_data['Subjects_or_Units_18'] in course_description[11]:
            course_data['Subject_Objective_18'] = course_des11[1]
        course_data['Subjects_or_Units_19'] = courses[18]
        if course_data['Subjects_or_Units_19'] in course_description[11]:
            course_data['Subject_Objective_19'] = course_des11[2]
        course_data['Subjects_or_Units_20'] = courses[19]
        if course_data['Subjects_or_Units_20'] in course_description[12]:
            course_data['Subject_Objective_20'] = course_description[12]
        course_data['Subjects_or_Units_21'] = ""
        course_data['Subject_Objective_21'] = ''
        course_data['Subjects_or_Units_22'] = ''
        course_data['Subject_Objective_22'] = ''
        course_data['Subjects_or_Units_23'] = ''
        course_data['Subject_Objective_23'] = ''
        course_data['Subjects_or_Units_24'] = ''
        course_data['Subject_Objective_24'] = ''
        course_data['Subjects_or_Units_25'] = ''
        course_data['Subject_Objective_25'] = ''
        course_data['Subjects_or_Units_26'] = ''
        course_data['Subject_Objective_26'] = ''
        course_data['Subjects_or_Units_27'] = ''
        course_data['Subject_Objective_27'] = ''
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_30'] = ''

        cities = soup.select("[width='593'] td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    elif "Master of Professional Accounting" in course_data['Course']:

        description(course_desc)

        course_data['Duration'] = 1
        course_data['Duration_Time'] = "Year"

        course_data['Fees'] = 28800

        table_course = soup.find_all("strong")
        for so in table_course:
            coccoc = so.text.replace("HI5001", "").replace("HI5002", "").replace("HI5003", "").replace("HI5017", ""). \
                replace("HI5019", "").replace("HI5020", "").replace("HI6025", "").replace("HI6026", "") \
                .replace("HI6027", "").replace("HI6028", "").replace("HI 6007", "").replace("HI 6008", "").strip()
            # print(coccoc)
            courses.append(coccoc)

        strong = soup.select("p:nth-of-type(n+10)")
        for so in strong:
            course_description.append(so.text)

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_description[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[2]:
            course_data['Subject_Objective_3'] = course_description[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[3]:
            course_data['Subject_Objective_4'] = course_description[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[4]:
            course_data['Subject_Objective_5'] = course_description[4]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[5]:
            course_data['Subject_Objective_6'] = course_description[5]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[6]:
            course_data['Subject_Objective_7'] = course_description[6]
        course_data['Subjects_or_Units_8'] = courses[7]
        if course_data['Subjects_or_Units_8'] in course_description[7]:
            course_data['Subject_Objective_8'] = course_description[7]
        course_data['Subjects_or_Units_9'] = courses[8]
        if course_data['Subjects_or_Units_9'] in course_description[8]:
            course_data['Subject_Objective_9'] = course_description[8]
        course_data['Subjects_or_Units_10'] = courses[9]
        if course_data['Subjects_or_Units_10'] in course_description[9]:
            course_data['Subject_Objective_10'] = course_description[9]
        course_data['Subjects_or_Units_11'] = courses[10]
        if course_data['Subjects_or_Units_11'] in course_description[10]:
            course_data['Subject_Objective_11'] = course_description[10]
        course_data['Subjects_or_Units_12'] = courses[11]
        if course_data['Subjects_or_Units_12'] in course_description[11]:
            course_data['Subject_Objective_12'] = course_description[11]
        course_data['Subjects_or_Units_13'] = ""
        course_data['Subject_Objective_13'] = ''
        course_data['Subjects_or_Units_14'] = ""
        course_data['Subject_Objective_14'] = ''
        course_data['Subjects_or_Units_15'] = ""
        course_data['Subject_Objective_15'] = ''
        course_data['Subjects_or_Units_16'] = ""
        course_data['Subject_Objective_16'] = ''
        course_data['Subjects_or_Units_17'] = ""
        course_data['Subject_Objective_17'] = ''
        course_data['Subjects_or_Units_18'] = ""
        course_data['Subject_Objective_18'] = ''
        course_data['Subjects_or_Units_19'] = ""
        course_data['Subject_Objective_19'] = ''
        course_data['Subjects_or_Units_20'] = ""
        course_data['Subject_Objective_20'] = ''
        course_data['Subjects_or_Units_21'] = ""
        course_data['Subject_Objective_21'] = ''
        course_data['Subjects_or_Units_22'] = ''
        course_data['Subject_Objective_22'] = ''
        course_data['Subjects_or_Units_23'] = ''
        course_data['Subject_Objective_23'] = ''
        course_data['Subjects_or_Units_24'] = ''
        course_data['Subject_Objective_24'] = ''
        course_data['Subjects_or_Units_25'] = ''
        course_data['Subject_Objective_25'] = ''
        course_data['Subjects_or_Units_26'] = ''
        course_data['Subject_Objective_26'] = ''
        course_data['Subjects_or_Units_27'] = ''
        course_data['Subject_Objective_27'] = ''
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_30'] = ''
        cities = soup.select("[width='593'] td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])

    elif "Master of Information Systems" in course_data['Course']:
        course_data['Duration'] = 1
        course_data['Duration_Time'] = "Year"

        course_data['Fees'] = 38400

        cities = soup.select("[width='630'] td")
        for cit in cities:
            campu = cit.text.lower()

            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])

        table_course = soup.select("p:nth-of-type(n+17) > strong:nth-of-type(1)")
        for so in table_course:
            coccoc = so.text.replace("HI6032 ", "").replace("HI5033 ", "").replace("HI5030", "").replace("HI5031", ""). \
                replace("HI5029", "").replace("HI6035", "").replace("HI6037", "").replace("HI6034", ""). \
                replace("HI6036", "").replace("HI6007", "").replace("HI6008", "").replace("HI6050", ""). \
                replace("HI6041 ", "").replace("HI6043 ", "").replace("HI6044", "").replace("HI6038", ""). \
                replace("HI6039", "").replace("HI6040", "").replace("HI6045", "").replace("HI6046", ""). \
                replace("HI6047", "").strip()
            # print(coccoc)
            courses.append(coccoc)

        strong = soup.select("p:nth-of-type(n+17)")
        for so in strong:
            course_description.append(so.text)

        course_data['Subjects_or_Units_1'] = courses[0]
        if course_data['Subjects_or_Units_1'] in course_description[0]:
            course_data['Subject_Objective_1'] = course_description[0]
        course_data['Subjects_or_Units_2'] = courses[1]
        if course_data['Subjects_or_Units_2'] in course_description[1]:
            course_data['Subject_Objective_2'] = course_description[1]
        course_data['Subjects_or_Units_3'] = courses[2]
        if course_data['Subjects_or_Units_3'] in course_description[2]:
            course_data['Subject_Objective_3'] = course_description[2]
        course_data['Subjects_or_Units_4'] = courses[3]
        if course_data['Subjects_or_Units_4'] in course_description[3]:
            course_data['Subject_Objective_4'] = course_description[3]
        course_data['Subjects_or_Units_5'] = courses[4]
        if course_data['Subjects_or_Units_5'] in course_description[4]:
            course_data['Subject_Objective_5'] = course_description[4]
        course_data['Subjects_or_Units_6'] = courses[5]
        if course_data['Subjects_or_Units_6'] in course_description[6]:
            course_data['Subject_Objective_6'] = course_description[6]
        course_data['Subjects_or_Units_7'] = courses[6]
        if course_data['Subjects_or_Units_7'] in course_description[7]:
            course_data['Subject_Objective_7'] = course_description[7]
        course_data['Subjects_or_Units_8'] = courses[8]
        if course_data['Subjects_or_Units_8'] in course_description[10]:
            course_data['Subject_Objective_8'] = course_description[10]
        course_data['Subjects_or_Units_9'] = courses[9]
        if course_data['Subjects_or_Units_9'] in course_description[11]:
            course_data['Subject_Objective_9'] = course_description[11]
        course_data['Subjects_or_Units_10'] = courses[10]
        if course_data['Subjects_or_Units_10'] in course_description[12]:
            course_data['Subject_Objective_10'] = course_description[12]
        course_data['Subjects_or_Units_11'] = courses[11]
        if course_data['Subjects_or_Units_11'] in course_description[13]:
            course_data['Subject_Objective_11'] = course_description[13]
        course_data['Subjects_or_Units_12'] = courses[14]
        if course_data['Subjects_or_Units_12'] in course_description[16]:
            course_data['Subject_Objective_12'] = course_description[16]
        course_data['Subjects_or_Units_13'] = courses[15]
        if course_data['Subjects_or_Units_13'] in course_description[17]:
            course_data['Subject_Objective_13'] = course_description[17]
        course_data['Subjects_or_Units_14'] = courses[16]
        if course_data['Subjects_or_Units_14'] in course_description[18]:
            course_data['Subject_Objective_14'] = course_description[18]
        course_data['Subjects_or_Units_15'] = courses[18]
        if course_data['Subjects_or_Units_15'] in course_description[21]:
            course_data['Subject_Objective_15'] = course_description[21]
        course_data['Subjects_or_Units_16'] = courses[19]
        if course_data['Subjects_or_Units_16'] in course_description[22]:
            course_data['Subject_Objective_16'] = course_description[22]
        course_data['Subjects_or_Units_17'] = courses[20]
        if course_data['Subjects_or_Units_17'] in course_description[23]:
            course_data['Subject_Objective_17'] = course_description[23]
        course_data['Subjects_or_Units_18'] = courses[21]
        if course_data['Subjects_or_Units_18'] in course_description[26]:
            course_data['Subject_Objective_18'] = course_description[26]
        course_data['Subjects_or_Units_19'] = courses[22]
        if course_data['Subjects_or_Units_19'] in course_description[27]:
            course_data['Subject_Objective_19'] = course_description[27]
        course_data['Subjects_or_Units_20'] = courses[23]
        if course_data['Subjects_or_Units_20'] in course_description[28]:
            course_data['Subject_Objective_20'] = course_description[28]
        course_data['Subjects_or_Units_21'] = ""
        course_data['Subject_Objective_21'] = ''
        course_data['Subjects_or_Units_22'] = ''
        course_data['Subject_Objective_22'] = ''
        course_data['Subjects_or_Units_23'] = ''
        course_data['Subject_Objective_23'] = ''
        course_data['Subjects_or_Units_24'] = ''
        course_data['Subject_Objective_24'] = ''
        course_data['Subjects_or_Units_25'] = ''
        course_data['Subject_Objective_25'] = ''
        course_data['Subjects_or_Units_26'] = ''
        course_data['Subject_Objective_26'] = ''
        course_data['Subjects_or_Units_27'] = ''
        course_data['Subject_Objective_27'] = ''
        course_data['Subjects_or_Units_28'] = ''
        course_data['Subject_Objective_28'] = ''
        course_data['Subjects_or_Units_29'] = ''
        course_data['Subject_Objective_29'] = ''
        course_data['Subjects_or_Units_30'] = ''
        course_data['Subject_Objective_30'] = ''

    print(course_data['Course'], course_data['Fees'], course_data['Website'])

    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

print(*course_data_all, sep='\n')

desired_order_list = ['Level_Code', 'University', 'City',
                      'Course', 'Faculty', 'Fees', 'Currency', 'Currency_Time',
                      'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                      'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2',
                      'Website', 'Course_Lang', 'Availability', 'Description', 'Career_Outcomes/path', 'Country',
                      'Online', 'Offline', 'Distance', 'Face_to_Face', 'Blended', 'Remarks',
                      'Subjects_or_Units_1', 'Subjects_or_Units_2', 'Subjects_or_Units_3', 'Subjects_or_Units_4',
                      'Subjects_or_Units_5', 'Subjects_or_Units_6',
                      'Subjects_or_Units_7', 'Subjects_or_Units_8', 'Subjects_or_Units_9',
                      'Subjects_or_Units_10', 'Subjects_or_Units_11', 'Subjects_or_Units_12',
                      'Subjects_or_Units_13', 'Subjects_or_Units_14', 'Subjects_or_Units_15',
                      'Subjects_or_Units_16', 'Subjects_or_Units_17', 'Subjects_or_Units_18',
                      'Subjects_or_Units_19', 'Subjects_or_Units_20', 'Subjects_or_Units_21',
                      'Subjects_or_Units_22', 'Subjects_or_Units_23', 'Subjects_or_Units_24',
                      'Subjects_or_Units_25', 'Subjects_or_Units_26', 'Subjects_or_Units_27',
                      'Subjects_or_Units_28', 'Subjects_or_Units_29', 'Subjects_or_Units_30',
                      'Subject_Objective_1', 'Subject_Objective_2', 'Subject_Objective_3',
                      'Subject_Objective_4', 'Subject_Objective_5', 'Subject_Objective_6',
                      'Subject_Objective_7', 'Subject_Objective_8', 'Subject_Objective_9',
                      'Subject_Objective_10', 'Subject_Objective_11', 'Subject_Objective_12',
                      'Subject_Objective_13', 'Subject_Objective_14', 'Subject_Objective_15',
                      'Subject_Objective_16', 'Subject_Objective_17', 'Subject_Objective_18',
                      'Subject_Objective_19', 'Subject_Objective_20', 'Subject_Objective_21',
                      'Subject_Objective_22', 'Subject_Objective_23', 'Subject_Objective_24',
                      'Subject_Objective_25', 'Subject_Objective_26', 'Subject_Objective_27',
                      'Subject_Objective_28', 'Subject_Objective_29', 'Subject_Objective_30',
                      'Subject_Description_1', 'Subject_Description_2', 'Subject_Description_3',
                      'Subject_Description_4', 'Subject_Description_5', 'Subject_Description_6',
                      'Subject_Description_7', 'Subject_Description_8', 'Subject_Description_9',
                      'Subject_Description_10', 'Subject_Description_11', 'Subject_Description_12',
                      'Subject_Description_13', 'Subject_Description_14', 'Subject_Description_15',
                      'Subject_Description_16', 'Subject_Description_17', 'Subject_Description_18',
                      'Subject_Description_19', 'Subject_Description_20', 'Subject_Description_21',
                      'Subject_Description_22', 'Subject_Description_23', 'Subject_Description_24',
                      'Subject_Description_25', 'Subject_Description_26', 'Subject_Description_27',
                      'Subject_Description_28', 'Subject_Description_29', 'Subject_Description_30'
                      ]
# tabulate our data
with open(csv_file, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

browser.quit()