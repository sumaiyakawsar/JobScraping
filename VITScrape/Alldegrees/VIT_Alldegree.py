"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/vit_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/vit_all_courses.csv'

possible_cities = {'adelaide': 'Adelaide',
                   'sydney': 'Sydney',
                   'abottsford': 'Abottsford',
                   'melbourne': 'Melbourne'
                   }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"
course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("strong"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        if each_desc is not None:
            course_data['Description'] = each_desc.text.replace("\n", " ").replace("About", "").strip()
        else:
            course_data['Description'] = "where"


def local_money_r(loc_money):
    for loc in loc_money:
        local_fee_raw = loc.text.replace("AUD", "").replace(" ", "").strip()
        loc_fee = re.search(currency_pattern, local_fee_raw)
        if loc_fee:
            local_fee = loc_fee.group()
            course_data['Local_Fees'] = local_fee.replace("$", "").strip()



def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text.replace("AUD", "").replace(" ", "").strip()
        Int_fee = re.search(currency_pattern, int_fee_raw)
        Int_fee_2 = re.search(number, int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            course_data['Int_Fees'] = int_fee.replace("$", "").strip()
        elif Int_fee_2:
            int_fee = Int_fee_2.group()
            course_data['Int_Fees'] = int_fee.strip()



def durationo(p_word):
    try:
        if p_word:
            s_word = p_word.lower()
            if 'full time' in s_word:
                course_data['Full_Time'] = 'Yes'

            if 'part time' in s_word:
                course_data['Part_Time'] = 'Yes'

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
                duration_time = value_conv[1]
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time
                if str(duration) == '1' or str(duration) == '1.0':
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Day'
            elif 'hour' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                duration_time = value_conv[1]
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time
                if str(duration) == '1' or str(duration) == '1.0':
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Hour'
            else:
                course_data['Duration'] = "bbbbb"
                course_data['Duration_Time'] = ''
        else:
            course_data['Duration'] = 'ssss'
            course_data['Duration_Time'] = ''

    except Exception:
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''


def subject_add(subs):
    subject_code = subs.select("td:nth-of-type(1)")
    subject_u = subs.select("td:nth-of-type(2)")
    if subs.text is not "":
        for sub in subject_code:
            for sub_u in subject_u:
                subjects___ = sub.text + " " + sub_u.text
                if subjects___ not in subject_unit:
                    subject_unit.append(subjects___)
                else:
                    del subjects___


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'Victorian Institute of Technology', 'City': '',
                   'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': 'Yes', 'Part_Time': 'Yes',
                   'Prerequisite_1': 'IELTS', 'Prerequisite_2': 'Equivalent AQF Level', 'Prerequisite_3': '',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': 'A', 'Description': '',
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
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find("h1")
    if course_name:
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
    else:
        course_data['Course'] = ""

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Duration
    dura = soup.select("tr:contains('Duration') td.table-data-right")
    for to in dura:
        p_word = to.text.strip()
        durationo(p_word)

    # Fees
    cost = soup.select("tr:contains('Cost') td.table-data-right")
    local_money = soup.select(
        "#domestic > div > div > table > tbody > tr:contains('Course Fee') > td.table-data-right.col-md-9")
    int_money = soup.select(
        "#international > div > div > table > tbody > tr:contains('Course Fee') > td.table-data-right.col-md-9")
    if local_money:
        local_money_r(local_money)
        if int_money:
            int_money_r(int_money)
    elif cost:
        int_money_r(cost)
        local_money_r(cost)

    # LOCATION/CITY
    campus = soup.select("tr:contains('Delivery Locations') td.table-data-right")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])

    # Description
    course_desc = soup.select("#single-page > div > div:nth-child(3) > div:nth-child(1)")
    course_desc2 = soup.select("tr:contains('Outline') td.table-data-right")
    if course_desc2:
        description(course_desc2)
    elif course_desc:
        description(course_desc)
    else:
        course_data['Description'] = "N/A"

    # Career Outcomes
    career_dic = []
    career = soup.select("tr:contains('Employment Pathway') td:nth-of-type(2)")
    career2 = soup.select("div:contains('EMPLOYMENT PATHWAY') div:nth-of-type(7) p")
    if career:
        for car in career:
            career_dic.append(car.text.replace("\n", ",").strip())
        course_data['Career_Outcomes/path'] = ''.join(career_dic)
    elif career2:
        for car in career2:
            career_dic.append(car.text.strip().replace("\n", "").strip())
        course_data['Career_Outcomes/path'] = ''.join(career_dic)
    else:
        course_data['Career_Outcomes/path'] = "None"

    # Full_time/Part_time/Online/Blended/
    ft_pt = soup.select_one(".in .table-row-5 td.table-data-right")
    if ft_pt:
        ft_pt_lower = ft_pt.text.lower()
        if 'full time' in ft_pt_lower:
            course_data['Full_Time'] = 'Yes'

        if 'part time' in ft_pt_lower:
            course_data['Part_Time'] = 'Yes'

        if 'online' in ft_pt_lower:
            course_data['Online'] = "Yes"
        else:
            course_data['Online'] = "No"

        if 'blended' in ft_pt_lower:
            course_data['Blended'] = "Yes"
        else:
            course_data['Blended'] = "No"
    if "Sydney" in actual_cities or "Melbourne" in actual_cities or "Abottsford" in actual_cities or "Adelaide" in actual_cities:
        course_data['Offline'] = "Yes"
    else:
        course_data['Offline'] = "No"

    if "Yes" in course_data['Blended']:
        course_data['Online'] = "Yes"
        course_data['Offline'] = "Yes"

    if "Yes" in course_data['Online'] and "Yes" in course_data['Offline']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    if "Yes" in course_data['Online']:
        course_data['Distance'] = "Yes"
    else:
        course_data['Distance'] = "No"

    if "Yes" in course_data['Offline']:
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Face_to_Face'] = "No"

    # Subject units
    subject_unit = []
    course_nameee = course_data['Course'].lower()
    if "diploma of hospitality management" in course_nameee or \
            "patisserie" in course_nameee or \
            "certificate iv in commercial cookery" in course_nameee or \
            "information technology" in course_nameee or \
            "business administration (mba)" in course_nameee:
        subject_table = soup.select("[border] tr:nth-of-type(n+4)")
        for so in subject_table:
            soooo = so.text.strip().lower()
            if "training pathway" in soooo or "employment pathway" in soooo or "assessment methods" in soooo or \
                    "recognition of prior learning" in soooo or "patisserie pathway" in soooo or \
                    "commercial cookery pathway" in soooo:
                del soooo
            else:
                subject_add(so)
    elif "certificate iii in carpentry" in course_nameee:
        subject_table = soup.select(".carpentry tr:nth-of-type(n+2)")
        for so in subject_table:
            subject_add(so)
    elif "certificate iii in commercial cookery" in course_nameee:
        subject_table = soup.select(".carpentry tr:nth-of-type(n+5)")
        for so in subject_table:
            soooo = so.text.strip().lower()
            if "training pathway" in soooo or "employment pathway" in soooo or "assessment methods" in soooo or \
                    "recognition of prior learning" in soooo or "patisserie pathway" in soooo or \
                    "commercial cookery pathway" in soooo:
                del soooo
            else:
                subject_add(so)

    i = 1
    for each_subs in subject_unit:
        course_data[f'Subject_or_Unit_{i}'] = each_subs
        i += 1
        if i == 41:
            break

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
