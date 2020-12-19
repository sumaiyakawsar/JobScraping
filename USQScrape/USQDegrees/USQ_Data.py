"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 02-11-20
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
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/USQ_link.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/USQ_All_courses.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hide"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


possible_cities = {'springfield': 'Ipswich',
                   'toowoomba': 'Toowoomba',
                   'ipswich': 'Ipswich',
                   'stanthorpe': 'Stanthorpe',
                   'online': 'Online'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'University of Southern Queensland', 'City': '', 'Course': '',
                   'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': '', 'Prerequisite_3': '',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
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
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source
    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(0.5)

    actual_cities = []

    # Course-Website
    course_data['Website'] = pure_url

    # Course
    course_tag = soup.find("h1")
    if course_tag:
        course_title = course_tag.text.replace("\n", " ").strip()
        course_data['Course'] = course_title

    if 'Bachelor' in course_data['Course'] and 'Honours' in course_data['Course']:
        course_level = "Bachelor honours"
    else:
        course_level = course_title

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_level:
                course_data['Level_Code'] = i
  
    # study mode
    studymode = soup.select("div.col-xs-6.col-sm-3:contains('mode')")
    studymode2 = soup.select("div.col-xs-6.col-sm-4:contains('mode')")
    if studymode:
        for each_mode in studymode:
            mode = each_mode.text.strip().replace("\n", "").lower()
            if 'online' in mode or 'external' in mode:
                if 'online' not in actual_cities:
                    actual_cities.append("Online")
    elif studymode2:
        for each_mode in studymode2:
            mode = each_mode.text.strip().replace("\n", "").lower()
            if 'online' in mode or 'external' in mode:
                if 'online' not in actual_cities:
                    actual_cities.append("Online")

    # City
    cities = soup.select("div.col-xs-6.col-sm-3:contains('Campus')")
    cities2 = soup.select("div.col-xs-6.col-sm-4:contains('Campus')")
    if cities:
        for each_city in cities:
            temp_line = each_city.text.lower().strip().replace("\n", "")
            for i in possible_cities:
                if i in temp_line:
                    actual_cities.append(possible_cities[i])
    elif cities2:
        for each_city in cities2:
            temp_line = each_city.text.lower().strip().replace("\n", "")
            for i in possible_cities:
                if i in temp_line:
                    actual_cities.append(possible_cities[i])

    if 'Online' in actual_cities:
        course_data['Online'] = "Yes"
        course_data['Distance'] = "Yes"
    else:
        course_data['Online'] = "No"
        course_data['Distance'] = "No"

    if 'Ipswich' in actual_cities or 'Stanthorpe' in actual_cities or 'Toowoomba' in actual_cities:
        course_data['Offline'] = "Yes"
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Offline'] = "No"
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Offline'] and "Yes" in course_data['Online']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    # Local fee
    try:
        localCSP = soup.select(
            "#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > "
            "tbody > tr:contains('Domestic full') > td:nth-child(2)")
        if localCSP:
            for each_local in localCSP:
                local_feeRaw = tag_text(each_local)
                local_fee = re.findall(currency_pattern, local_feeRaw)[0]
                if local_fee:
                    course_data['Local_Fees'] = local_fee.replace("AUD", "").strip()
    except IndexError:
        course_data['Local_Fees'] = ""

    # Prerequisites 1
    try:
        pre_req_1 = soup.select("tr:contains('ATAR (2021)') td:nth-of-type(2)")
        if pre_req_1:
            for grade in pre_req_1:
                gra = grade.text
                if has_numbers(gra):

                    atar = re.search(r'\d+(?:\.*\d*)?', gra)
                    if atar:
                        course_data['Prerequisite_1_grade_1'] = atar.group()
    except Exception:
        pass

    # Duration/Duration Time/FullTime/Parttime/
    course_detail = soup.select("div.col-xs-6:contains('Duration')")
    for ra in course_detail:
        try:
            course_duration = ra.text
            if course_duration:
                p_word = course_duration.__str__().strip()
                if 'full-time' in p_word.lower() or "or part-time equivalent" in p_word.lower():
                    course_data['Full_Time'] = 'Yes'
                else:
                    course_data['Full_Time'] = 'No'
                if 'part-time' in p_word.lower():
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
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration_time = 'Months'
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
                    course_data['Duration_Time'] = 'Days'
                    if str(duration) == '1' or str(duration) == '1.0':
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = 'Day'


        except IndexError:
            pass

    # Description
    describe = []
    courseDescription = soup.select(".pt-3 .c-program-content ul")
    if courseDescription:
        for ea in courseDescription:
            describe.append(ea.text.strip().replace("\n", " "))
    else:
        courseDescription = soup.select(
            "body > div.u-main-wrapper__content > div.c-program-content.py-3 > div > div > div > ul ")
        if courseDescription:
            for ea in courseDescription:
                describe.append(ea.text.strip().replace("\n", " "))
    course_data['Description'] = ' '.join(describe)

    # Career Outcome
    careers = []
    careerDetails = soup.select("#career-outcomes > div > div > div > div > ul > li")
    if careerDetails:
        for each_career in careerDetails:
            careers.append(each_career.text.replace("\n","").strip())

    course_data['Career_Outcomes/path'] = ', '.join(careers).strip()

    # International Fees
    try:
        btn_international = soup.select(
            "body > div.u-main-wrapper__content > div.c-program-summary.p-4 > div > div:nth-child(1) > div > "
            "a:nth-child(2)")
        if btn_international:
            int_button = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/a[2]")
            if int_button:
                int_button.click()
                browser.current_url
                courses_int = browser.page_source
                soup2 = bs4.BeautifulSoup(courses_int, 'lxml')
                time.sleep(5)

                course_data['Availability'] = "A"
    
            try:
                Int_amount = soup2.select(
                    "#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > tbody > tr:contains("
                    "'On-campus') > td:nth-child(2)")
                if Int_amount:
                    for each_int in Int_amount:
                        Int_feeRaw = tag_text(each_int)
                        Int_fee = re.findall(currency_pattern, Int_feeRaw)[0]
                        if Int_fee:
                            course_data['Int_Fees'] = Int_fee.replace("AUD", "").strip()

                else:
                    Int_amounts = soup2.select(
                        "#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > tbody > "
                        "tr:contains('External') > td:nth-child(2)")
                    if Int_amounts:
                        for each_ints in Int_amounts:
                            Int_fee_Raw = tag_text(each_ints)
                            Int_fees = re.findall(currency_pattern, Int_fee_Raw)[0]
                            if Int_fees:
                                course_data['Int_Fees'] = Int_fees.replace("AUD", "").strip()
    
            except IndexError:
                course_data['Int_Fees'] = ""
        else:
            course_data['Availability'] = "D"
    except Exception:
        course_data['Availability'] = "D"

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
