"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 19-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import pandas as pd
import os
import re
import time
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
course_links_file_path = course_links_file_path.__str__() + '/BB_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/BBC_all_courses.csv'

possible_cities = {'sydney': 'Sydney',
                   'melbourne': 'Melbourne',
                   'brisbane': 'Brisbane'
                   }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("span"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.replace("\n", "").replace("About the course", "").strip()


def durationo(p_word):
    try:
        if p_word:
            dur_word = p_word.lower()
            if 'full-time' in dur_word and 'part-time' not in dur_word:
                course_data['Full_Time'] = 'Yes'
            else:
                course_data['Full_Time'] = 'No'

            if 'part-time' in dur_word or 'part' in dur_word and 'full-time' not in dur_word:
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Part_Time'] = 'No'

            if 'part-time' in dur_word or 'part' in dur_word and 'full-time' in dur_word:
                course_data['Part_Time'] = 'Yes'
                course_data['Full_Time'] = 'Yes'

            durr = p_word.__str__().lower()
            if 'year' in durr:
                value_conv = DurationConverter.convert_duration(durr)
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
                course_data['Duration'] = 1.0
                course_data['Duration_Time'] = 'Year'
    except Exception:
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''


def ielts(iel):
    for ie in iel:
        ielts_amount = ie.text.strip()
        if has_numbers(ielts_amount):
            ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
            course_data['Prerequisite_2_grade_2'] = ielts


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'Billy Blue College', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': 'Equivalent AQF level',
                   'Prerequisite_1_grade_1': 'No ATAR needed', 'Prerequisite_2_grade_2': '',
                   'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': 'A', 'Description': '',
                   'Career_Outcomes/path': '',
                   'Country': 'Australia', 'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '',
                   'Blended': '', 'Remarks': '',
                   'Subject_or_Unit_1': '', 'Subject_Objective_1': '', 'Subject_Description_1': '',
                   'Subject_or_Unit_2': '', 'Subject_Objective_2': '', 'Subject_Description_2': '',
                   'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
                   'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
                   'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
                   'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
                   'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
                   'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
                   'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
                   'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
                   'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
                   'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
                   'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
                   'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
                   'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
                   'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
                   'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
                   'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
                   'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
                   'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
                   'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
                   'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
                   'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
                   'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
                   'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
                   'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
                   'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
                   'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
                   'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
                   'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
                   'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
                   'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
                   'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
                   'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
                   'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
                   'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
                   'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
                   'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
                   'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
                   'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''
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
    course_name = soup.find(id="page-title")
    if course_name:
        course_title = course_name.find("h1")
        if course_title:
            course_data['Course'] = course_title.text.strip()
        else:
            course_data['Course'] = course_name.text.strip()
    else:
        course_data['Course'] = ""

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Description
    course_desc = soup.find("p", class_="branded-fashion-text")
    course_des = soup.select(".container > p:nth-of-type(1)")
    if course_desc:
        course_data['Description'] = course_desc.text.replace("\n", "").strip()
    elif course_des:
        description(course_des)

    # Duration
    dura = soup.select("div:nth-of-type(4) ul.accord-open")
    for to in dura:
        p_word = to.text.strip().replace("4 trimesters", "").replace("2 trimesters", ""). \
            replace("Full-time accelerated: 2 years", "").replace("Full-time accelerated: 1 year", "").strip(). \
            replace("Full-time accelerated: 3 years", "").strip()
        durationo(p_word)

    study_options = soup.select(".text-white div.col-sm-6:nth-of-type(1)")
    study_options2 = soup.select("table:nth-of-type(1) tr:nth-of-type(6) td:nth-of-type(2)")
    if study_options:
        for so in study_options:
            s_word = so.text.strip().lower()
            if "sydney" in s_word:
                actual_cities.append("Sydney")
            if "brisbane" in s_word:
                actual_cities.append("Brisbane")
            if "melbourne" in s_word:
                actual_cities.append("Melbourne")

            if "blended" in s_word:
                course_data['Blended'] = "Yes"
            else:
                course_data['Blended'] = "No"
            if "online" in s_word:
                course_data['Online'] = "Yes"
                course_data['Distance'] = "Yes"
            else:
                course_data['Online'] = "No"
                course_data['Distance'] = "No"
    elif study_options2:
        for tso in study_options2:
            st_word = tso.text.strip().lower()
            if "sydney" in st_word:
                actual_cities.append("Sydney")
            if "brisbane" in st_word:
                actual_cities.append("Brisbane")
            if "melbourne" in st_word:
                actual_cities.append("Melbourne")

            if "blended" in st_word or "online" in st_word:
                course_data['Blended'] = "Yes"
                course_data['Online'] = "Yes"
                course_data['Distance'] = "Yes"
            else:
                course_data['Blended'] = "No"
                course_data['Online'] = "No"
                course_data['Distance'] = "No"

    if 'Sydney' in actual_cities or 'Melbourne' in actual_cities or 'Brisbane' in actual_cities:
        course_data['Offline'] = "Yes"
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Offline'] = "No"
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Blended']:
        course_data['Online'] = "Yes"
        course_data['Distance'] = "Yes"

    # IELTS
    iel = soup.select("#international-admissions-criteria > div > div > ul > li")
    if iel:
        ielts(iel)

    # Career Outcomes
    overview = soup.find("div", class_="gray-bg")
    overview2 = soup.select_one(".container > ul:nth-of-type(1)")
    if overview:
        career = overview.find("ul")
        if career:
            course_data['Career_Outcomes/path'] = career.text.strip().replace("\n", ", ").strip()
        else:
            course_data['Career_Outcomes/path'] = "None1"
    elif overview2:
        course_data['Career_Outcomes/path'] = overview2.text.strip().replace("\n", ", ").strip()

    course_data["Faculty"] = "College of Design"

    if "GCERT" in course_data['Level_Code'] or "MST" in course_data['Level_Code']:
        course_data['Prerequisite_3_grade_3'] = "Bachelor's Degree"
    else:
        course_data['Prerequisite_3_grade_3'] = "Year 12"

    subjects = []

    div = soup.select(".active a.custom_coreunit")
    if div:
        for di in div:
            if di.text not in subjects:
                subjects.append(di.text)

    try:
        level_2 = browser.find_element_by_xpath('//*[@id="whatyouwillstudyTabs"]/li[2]/a').click()
        div = soup.select("div#year2 a.custom_coreunit")
        if div:
            for di in div:
                if di.text not in subjects:
                    subjects.append(di.text)

        level_3 = browser.find_element_by_xpath('//*[@id="whatyouwillstudyTabs"]/li[3]/a').click()
        div = soup.select("div#year3 a.custom_coreunit")
        if div:
            for di in div:
                if di.text not in subjects:
                    subjects.append(di.text)
    except Exception:
        pass

    i = 0
    for sub in subjects:
        course_data[f'Subject_or_Unit_{i}'] = sub
        i += 1

    # Local Fees (https://www.torrens.edu.au/wp-content/uploads/other/domestic-fees.pdf)
    # Int Fees (https://www.torrens.edu.au/wp-content/uploads/other/international-fees.pdf)
    if "DIP" in course_data['Level_Code']:
        course_data['Int_Fees'] = 29400
        if "Diploma of Design" in course_data['Course']:
            course_data['Local_Fees'] = 24000
        else:
            course_data['Local_Fees'] = 24900
    elif "BA" in course_data['Level_Code']:
        course_data['Local_Fees'] = 74700
        course_data['Int_Fees'] = 88200
        if "Bachelor of Business and Bachelor of Design" in course_data['Course']:
            course_data['Local_Fees'] = 86800
            course_data['Int_Fees'] = 102000
    elif "GCERT" in course_data['Level_Code']:
        course_data['Local_Fees'] = 13700
        course_data['Int_Fees'] = 15650
    elif "MST" in course_data['Level_Code']:
        course_data['Local_Fees'] = 54800
        course_data['Int_Fees'] = 62600
        if "Master of Design / Master of Design (Advanced)" in course_data['Course']:
            course_data['Local_Fees'] = 41100
            course_data['Int_Fees'] = 39000

    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

print(*course_data_all, sep='\n')

desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty',
                      'Int_Fees', 'Local_Fees', 'Currency', 'Currency_Time',
                      'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                      'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3',
                      'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2', 'Prerequisite_3_grade_3',
                      'Website', 'Course_Lang', 'Availability', 'Description', 'Career_Outcomes/path', 'Country',
                      'Online', 'Offline', 'Distance', 'Face_to_Face', 'Blended', 'Remarks',
                      'Subject_or_Unit_1', 'Subject_Objective_1', 'Subject_Description_1',
                      'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                      'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                      'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                      'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                      'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                      'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                      'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                      'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                      'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                      'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                      'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                      'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                      'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                      'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                      'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                      'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                      'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                      'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                      'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                      'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                      'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                      'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                      'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                      'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                      'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                      'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                      'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                      'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                      'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                      'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                      'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                      'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                      'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                      'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                      'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                      'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                      'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                      'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                      'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40'
                      ]

# tabulate our data
df = pd.DataFrame(course_data_all, columns=desired_order_list)
df.to_csv(csv_file, index=False)

browser.quit()
