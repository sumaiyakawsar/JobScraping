"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 05-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/uow_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/UOW_allCourses.csv'

possible_cities = {'wollongong': 'Wollongong',
                   'shoalhaven': 'Shoalhaven',
                   'batemans bay': 'Batemans Bay',
                   'bega': 'Bega',
                   'southern highlands': 'Southern Highlands',
                   'innovation campus': 'Wollongong'
                   }
main_cities = {'wollongong': 'Wollongong',
               'shoalhaven': 'Shoalhaven',
               'batemans bay': 'Batemans Bay',
               'bega': 'Bega',
               'southern highlands': 'Southern Highlands',
               'innovation campus': 'Wollongong',
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
    for tag in soup_.find_all(class_="h2"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.strip().replace("\n", " ").strip()


def int_fees(raw_fee):
    for each_int in raw_fee:
        int_feeraw = tag_text(each_int)
        int_fee = re.findall(currency_pattern, int_feeraw)[0]
        if int_fee:
            course_data['Int_Fees'] = int_fee.replace("$", "").strip()
        else:
            course_data['Int_Fees'] = ""


def local_fees(local_fee):
    for each_local in local_fee:
        local_feeraw = tag_text(each_local)
        locala_fee = re.findall(currency_pattern, local_feeraw)[0]
        if locala_fee:
            course_data['Local_Fees'] = locala_fee.replace("$", "").strip()
        else:
            course_data['Local_Fees'] = ""


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'University of Wollongong', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': 'Equivalent AQF Level',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': 'Year 12',
                   'Website': '', 'Course_Lang': 'English', 'Availability': '', 'Description': '',
                   'Career_Outcomes/path': '', 'Country': 'Australia',
                   'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '', 'Remarks': '',
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
    time.sleep(0.1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.select(
        "#hero-banner > div > div > div.grid_8 > h1")
    if course_name:
        for course in course_name:
            course_title = tag_text(course)
            course_data['Course'] = course_title
    else:
        course_data['Course'] = ""

    if 'Honours' in course_title and 'Bachelor' in course_title:
        course_level = 'Bachelor honours'
    else:
        course_level = course_title
    # Faculty
    faculty_column = soup.select("#course-info > div > div:nth-child(2) > p:nth-child(2)")
    if faculty_column:
        for each_faculty in faculty_column:
            course_data['Faculty'] = each_faculty.text.strip()
    else:
        course_data['Faculty'] = ""

    # City
    city_col = soup.select('#course-info > div > div:nth-child(3) > p:nth-child(2)')
    if city_col:
        for each_city in city_col:
            cities = each_city.text.strip()
            if 'south western sydney' in cities.lower():
                actual_cities.append("Sydney")
            elif 'sydney' in cities.lower():
                actual_cities.append("Sydney")
            if 'southern sydney' in cities.lower():
                actual_cities.append("Sydney")

            for i in possible_cities:
                if i in cities.lower():
                    actual_cities.append(possible_cities[i])

    # Prerequisite_1_grade_1
    Atar_col = soup.select("#course-info > div > div:nth-child(5) > p:nth-child(2)")
    if Atar_col:
        for each_atar in Atar_col:
            atar = each_atar.text.strip()
            if has_numbers(atar):
                course_data['Prerequisite_1_grade_1'] = atar
            else:
                course_data['Prerequisite_1_grade_1'] = "N/A"
    else:
        course_data['Prerequisite_1_grade_1'] = "N/A"

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_level:
                course_data['Level_Code'] = i

    # Duration/Duration Time/FullTime/Parttime/

    course_detail = soup.select("#course-info > div > div.grid_3.clear-left > p:nth-child(2)")
    for ra in course_detail:
        try:
            course_duration = ra.text.replace("2 sessions", "").replace("3 session", "").replace("1 session over", "")
            if course_duration:
                p_word = course_duration.__str__().strip()
                if p_word:
                    if 'full' in p_word.lower() and 'part' not in p_word.lower():
                        course_data['Full_Time'] = 'Yes'
                    else:
                        course_data['Full_Time'] = 'No'
                    if 'part' in p_word.lower() and 'full' not in p_word.lower():
                        course_data['Part_Time'] = 'Yes'
                    else:
                        course_data['Part_Time'] = 'No'

                    if 'part' in p_word.lower() and 'full' in p_word.lower():
                        course_data['Full_Time'] = 'Yes'
                        course_data['Part_Time'] = 'Yes'

                    if 'part' not in p_word.lower() and 'full' not in p_word.lower():
                        course_data['Full_Time'] = "Yes"

                    if 'year' in p_word.__str__().lower():
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                        duration_time = value_conv[1]

                        if str(duration) == '1' or str(duration) == '1.0':
                            duration_time = 'Year'
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time
                        elif 'month' in duration_time.__str__().lower():
                            value_conv = DurationConverter.convert_duration(p_word)
                            duration_time = value_conv[1]
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time
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
                        course_data['Duration_Time'] = value_conv[1]
                        if str(duration) == '1' or str(duration) == '1.0':
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = 'Day'
                    else:
                        course_data['Duration'] = p_word.__str__()
                        course_data['Duration_Time'] = ''
                else:
                    course_data['Duration'] = "N/A"
                    course_data['Duration_Time'] = ''
            else:
                course_data['Duration'] = "N/A"
                course_data['Duration_Time'] = ''
        except IndexError:
            course_data['Full_Time'] = ''
            course_data['Part_Time'] = ''
            course_data['Duration'] = ''
            course_data['Duration_Time'] = ''
            print(course_data['Course'] + "this course doesn't have information pertaining to duration")

    # Description
    course_highlights = soup.select("#course-summary > div.grid_12 > div")

    if course_highlights:
        description(course_highlights)
    else:
        course_data['Description'] = "N/A"

    # career Outcome
    career = soup.select("#careers > div > div:nth-child(1) > ul")
    if career:
        for each_career in career:
            course_data['Career_Outcomes/path'] = each_career.text.strip().replace("\n", ", ").strip()
    else:
        course_data['Career_Outcomes/path'] = "No career outcomes provided"

    # Int fees
    try:
        int_amount = soup.select(
            "#students > div > div > div:nth-child(5) > div:nth-child(5) > div > table > tbody > tr > td:nth-child(3)")
        int_amount2 = soup.select(
            "#students > div > div > div:nth-child(5) > div:nth-child(3) > div > table > tbody > tr > td:nth-child(3)")
        int_amount3 = soup.select(
            "#students > div > div > div:nth-child(5) > div:nth-child(7) > div > table > tbody > tr > td:nth-child(3)")
        int_amount4 = soup.select(
            "#students > div > div > div:nth-child(5) > div:nth-child(9) > div > table > tbody > tr > td:nth-child(3)")
        if int_amount:
            int_fees(int_amount)
        elif int_amount2:
            int_fees(int_amount2)
        elif int_amount3:
            int_fees(int_amount3)
        elif int_amount4:
            int_fees(int_amount4)
        else:
            course_data['Int_Fees'] = "N/A"

    except IndexError:
        course_data['Int_Fees'] = "N/A"

    # Local_fee
    try:
        latest_local = soup.select(
            "#students > div > div > div:nth-child(3) > div:nth-child(6) > table > tbody > tr:nth-child(1) > td:nth-child(3)")
        latest_local2 = soup.select(
            "#students > div > div > div:nth-child(3) > div:nth-child(5) > table > tbody > tr > td:nth-child(3)")
        latest_local3 = soup.select(
            "#students > div > div > div:nth-child(3) > div:nth-child(3) > table > tbody > tr > td:nth-child(3)")
        latest_local4 = soup.select(
            "#students > div > div > div:nth-child(3) > div:nth-child(7) > table > tbody > tr > td:nth-child(3)")

        if latest_local:
            local_fees(latest_local)
        elif latest_local2:
            local_fees(latest_local2)
        elif latest_local3:
            local_fees(latest_local3)
        elif latest_local4:
            local_fees(latest_local4)
        else:
            course_data['Local_Fees'] = "CSP supported"

    except IndexError:
        course_data['Local_Fees'] = "N/A"

    # IELTS
    try:
        ielts_col = soup.select(
            "#students > div > div > div:nth-child(5) > div:nth-child(1) > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(2)")
        if ielts_col:
            for ea in ielts_col:
                ielts_amount = ea.text.strip()
                if has_numbers(ielts_amount):
                    ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                    course_data['Prerequisite_2_grade_2'] = ielts
                else:
                    course_data['Prerequisite_2_grade_2'] = "N/A"
        else:
            course_data['Prerequisite_2_grade_2'] = "N/A"
    except AttributeError:
        course_data['Prerequisite_2_grade_2'] = "N/A"

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    delivery_mode = soup.select("#course-info > div > div:nth-child(7) > p:nth-child(2)")
    if delivery_mode:
        for delivery in delivery_mode:
            delivery_mod = delivery.text.strip().lower()
            if 'on campus' in delivery_mod and 'distance' not in delivery_mod:
                course_data['Offline'] = "Yes"
                course_data['Face_to_Face'] = "Yes"
                course_data['Distance'] = "No"
                course_data['Online'] = "No"
            if 'distance' in delivery_mod and 'on campus' not in delivery_mod:
                course_data['Distance'] = "Yes"
                course_data['Online'] = "Yes"
                course_data['Offline'] = "No"
                course_data['Face_to_Face'] = "No"
            if 'distance' in delivery_mod and 'on campus' in delivery_mod:
                course_data['Distance'] = "Yes"
                course_data['Online'] = "Yes"
                course_data['Offline'] = "Yes"
                course_data['Face_to_Face'] = "Yes"
            if 'flexible' in delivery_mod:
                course_data['Distance'] = "Yes"
                course_data['Online'] = "Yes"
                course_data['Offline'] = "Yes"
                course_data['Face_to_Face'] = "Yes"

    if "Yes" in course_data['Offline'] and "Yes" in course_data['Online']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    # Availability
    avail = soup.select("#students > div > div > div:nth-child(5)")
    if avail:
        for va in avail:
            if "not available to international applicants" in va.text:
                course_data['Availability'] = "D"
            else:
                course_data['Availability'] = "A"

    if "D" in course_data['Availability']:
        course_data['Int_Fees'] = " N/A"
    elif "I" in course_data['Availability']:
        course_data['Local_Fees'] = "N/A"

    # Remark
    remark_col = soup.select("#why-this-course > div > div")
    if remark_col:
        for each_remark in remark_col:
            course_data['Remarks'] = tag_text(each_remark).replace("\n", " ").strip()
    else:
        course_data['Remarks'] = "NA"
  
    
    for i in actual_cities:
        course_data['City'] = main_cities[i.lower()]
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
