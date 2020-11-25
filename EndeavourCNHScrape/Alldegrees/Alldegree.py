"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 25-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/Endeavour_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/Endeavour_allCourses.csv'

course_data = {'Level_Code': '',
               'University': 'Endeavour College of Natural Health',
               'City': '',
               'Course': '',
               'Faculty': 'College of Natural Health',
               'Int_Fees': '',
               'Local_Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': '',
               'Full_Time': '',
               'Part_Time': '',
               'Prerequisite_1': 'Equivalent AQF',
               'Prerequisite_2': 'IELTS',
               'Prerequisite_1_grade_1': 'Year 12',
               'Prerequisite_2_grade_2': '',
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
               'Blended': 'Yes',
               'Remarks': ''
               }

possible_cities = {'brisbane': 'Brisbane',
                   'sydney': 'Sydney',
                   'adelaide': 'Adelaide',
                   'gold coast': 'Gold coast',
                   'perth': 'Perth',
                   'melbourne': 'Melbourne',
                   'online': 'Online'
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


for each_url in course_links_file:
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

    # Description
    course_desc = soup.select(".rich-text h3")
    if course_desc:
        description(course_desc)
    else:
        course_data['Description'] = "N/A"

    # Duration
    dura = soup.select("div.outline-elem:nth-of-type(1) .outline-body > p")
    for to in dura:
        p_word = to.text.strip()
        durationo(p_word)

    # LOCATION/CITY
    campus = soup.select("div:nth-of-type(2) .outline-body")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    else:
        print("Find city")

    # IELTS
    iels = soup.select(
        "body > main > div:nth-child(1) > div.row-1-2 > div:nth-child(1) > section > div:nth-child(3) > div.outline-body > div > p:nth-child(5)")
    iels2 = soup.select(
        "body > main > div:nth-child(1) > div.row-1-2 > div:nth-child(1) > section > div:nth-child(3) > div.outline-body > div > p:nth-child(6)")
    iels3 = soup.select(
        "body > main > div:nth-child(1) > div.row-1-2 > div:nth-child(1) > section > div:nth-child(3) > div.outline-body > div > ul > li:nth-child(3)")
    for ielt in iels:
        if "english" in ielt.text.lower():
            ielts_amount = ielt.text.lower()
            if has_numbers(ielts_amount):
                ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                course_data['Prerequisite_2_grade_2'] = ielts

        elif iels2:
            for ielt2 in iels2:
                if "english" in ielt2.text.lower():
                    ielts_amount = ielt2.text.lower()
                    if has_numbers(ielts_amount):
                        ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                        course_data['Prerequisite_2_grade_2'] = ielts

        elif iels3:
            for ielt3 in iels3:
                if "english" in ielt3.text.lower():
                    ielts_amount = ielt3.text.lower()
                    if has_numbers(ielts_amount):
                        ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                        course_data['Prerequisite_2_grade_2'] = ielts

    # Career Outcomes
    overview = soup.select("#course-callout-card div")
    if overview:
        for ov in overview:
            course_data['Career_Outcomes/path'] = ov.text.strip()
    else:
        course_data['Career_Outcomes/path'] = "N/A"

    # Online
    if 'Online' in actual_cities:
        course_data['Online'] = "Yes"
        course_data['Offline'] = "No"
    elif 'Online' not in actual_cities:
        course_data['Online'] = "Yes"
        course_data['Offline'] = "Yes"

    course_nam = course_data['Course'].lower()

    # Local_fee from (https://acnm.s3-ap-southeast-2.amazonaws.com/pub/DOCID-2102554854-15567.pdf)
    # International fee from (https://acnm.s3-ap-southeast-2.amazonaws.com/pub/DOCID-2102554854-15571.pdf)
    if "massage" in course_nam:
        fee = soup.select(
            "body > main > div:nth-child(1) > div.row-1-2 > div:nth-child(1) > section > div:nth-child(5) > div.outline-body > p:nth-child(1)")
        local_money_r(fee)
        int_money_r(fee)
    elif "diploma of health science" in course_nam:
        course_data['Local_Fees'] = 17636
        course_data['Availability'] = "A"
        course_data['Int_Fees'] = 13224
    elif "complementary medicine" in course_nam:
        course_data['Local_Fees'] = 35918
        course_data['Availability'] = "A"
        course_data['Int_Fees'] = 35194
    elif "acupuncture" in course_nam:
        course_data['Local_Fees'] = 70690
        course_data['Availability'] = "A"
        course_data['Int_Fees'] = 82678
    elif "myotherapy" in course_nam:
        course_data['Local_Fees'] = 56470
        course_data['Availability'] = "N"
        course_data['Int_Fees'] = 66541
    elif "naturopathy" in course_nam:
        course_data['Local_Fees'] = 70539
        course_data['Availability'] = "A"
        course_data['Int_Fees'] = 73562
    elif "nutritional" in course_nam:
        course_data['Local_Fees'] = 52908
        course_data['Availability'] = "A"
        course_data['Int_Fees'] = 59819

    if "Yes" in course_data['Online']:
        course_data['Distance'] = "Yes"
    else:
        course_data['Distance'] = "No"

    if "Yes" in course_data['Offline']:
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Offline'] and "Yes" in course_data['Online']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    print(actual_cities, course_data['Online'], course_data['Distance'], course_data['Offline'],
          course_data['Face_to_Face'], course_data['Blended'], course_data['Website'])

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
                      'Prerequisite_1_grade_1',
                      'Prerequisite_2_grade_2',
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
with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

browser.quit()
