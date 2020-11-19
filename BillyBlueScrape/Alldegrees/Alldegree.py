"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 19-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import csv
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
course_links_file_path = course_links_file_path.__str__() + '/BillyBlue_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/BBC_unordered.csv'

course_data = {'Level_Code': '',
               'University': 'Billy Blue College',
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
               'Prerequisite_3': 'Equivalent AQF level',
               'Prerequisite_1_grade_1': 'No ATAR needed',
               'Prerequisite_2_grade_2': '',
               'Prerequisite_3_grade_3': '',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': 'A',
               'Description': '',
               'Career_Outcomes/path': '',
               'Country': 'Australia',
               'Online': '',
               'Offline': '',
               'Distance': '',
               'Face_to_Face': '',
               'Blended': '',
               'Remarks': ''
               }

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


def local_money_r(loc_money):
    for loc in loc_money:
        local_fee_raw = loc.text
        loc_fee = re.search(currency_pattern, local_fee_raw)
        if loc_fee:
            local_fee = loc_fee.group()
            course_data['Local_Fees'] = local_fee.replace("$", "").strip()


def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text
        Int_fee = re.search(currency_pattern, int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            course_data['Int_Fees'] = int_fee.replace("$", "").strip()


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
                course_data['Duration'] = ""
                course_data['Duration_Time'] = ''
        else:
            course_data['Duration'] = ''
            course_data['Duration_Time'] = ''

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
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name #page-title h1
    course_name = soup.find(id="page-title")
    try:
        if course_name:
            course_title = course_name.find("h1")
            if course_title:
                course_data['Course'] = course_title.text.strip()
            else:
                course_data['Course'] = course_name.text.strip()
        else:
            course_data['Course'] = "Na"
    except AttributeError:
        course_data['Course'] = " Why"

    # print(course_data['Course'],course_data['Website'])

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    # Description.container > p:nth-of-type(1)
    course_desc = soup.find("p", class_="branded-fashion-text")
    course_des = soup.select(".container > p:nth-of-type(1)")
    if course_desc:
        course_data['Description'] = course_desc.text.replace("\n", "").strip()
    elif course_des:
        description(course_des)
    else:
        course_data['Description'] = "N/A"

    # print(course_data['Course'], "/////", course_data['Level_Code'], "///", course_data['Description'],
    # course_data['Website'])

    # Duration
    dura = soup.select("div:nth-of-type(4) ul.accord-open")
    for to in dura:
        p_word = to.text.strip().replace("4 trimesters", "").replace("2 trimesters", "").strip()
        durationo(p_word)
    # print(course_data['Duration'], course_data['Duration_Time'], course_data['Full_Time'], course_data['Part_Time'],
    # course_data['Website'])

    study_options = soup.select(".text-white div.col-sm-6:nth-of-type(1)")
    study_options2 = soup.select("table:nth-of-type(1) tr:nth-of-type(6) td:nth-of-type(2)")
    if study_options:
        for so in study_options:
            s_word = so.text.strip().lower()
            # print(s_word)
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
            # print(st_word)
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

    if actual_cities is not None:
        course_data['Offline'] = "Yes"
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Offline'] = "No"
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Blended']:
        course_data['Online'] = "Yes"
        course_data['Distance'] = "Yes"
    # print(course_data['Website'], actual_cities,course_data['Online'],course_data['Offline'],course_data['Blended'],
    # course_data['Distance'],course_data['Face_to_Face'])

    # IELTS
    iel = soup.select("#international-admissions-criteria > div > div > ul > li:nth-child(2)")
    iels = soup.select("#international-admissions-criteria > div > div > ul > li:nth-child(3)")
    iel3 = soup.select(
        "#sectionMainInner > div > div > table:nth-child(16) > tbody > tr:nth-child(4) > td:nth-child(2)")
    if iel:
        ielts(iel)
    elif iels:
        ielts(iels)
    elif iel3:
        ielts(iel3)
    else:
        course_data['Prerequisite_2_grade_2'] = "N"

    # print(course_data['Prerequisite_2_grade_2'], course_data['Website'])

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
    else:
        course_data['Career_Outcomes/path'] = "None2"

    # print(course_data['Career_Outcomes/path'],course_data['Website'])

    course_data["Faculty"] = "College of Design"

    if "GCERT" in course_data['Level_Code'] or "MST" in course_data['Level_Code']:
        course_data['Prerequisite_3_grade_3'] = "Bachelor's Degree"
    else:
        course_data['Prerequisite_3_grade_3'] = "Year 12"

    print(course_data['Course'])

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
                      'Local_Fees',
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

ordered_file = csv_file_path.parent.__str__() + "/BBC_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
