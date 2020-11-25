"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 24-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import csv
import os
import re
import time
import timeit
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
course_links_file_path = course_links_file_path.__str__() + '/kangan_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/kangan_all_courses.csv'

course_data = {'Level_Code': '',
               'University': 'Kangan Batman Institute',
               'City': '',
               'Course': '',
               'Faculty': '',
               'Non-Apprentice_Government_Subsidised_Fee': '',
               'Non-Apprentice_Concession_Fees': '',
               'Non-Apprentice_Full_Fees': '',
               'Apprentice_Government_Subsidised_Fee': '',
               'Apprentice_Concession_Fees': '',
               'Apprentice_Full_Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': '',
               'Full_Time': '',
               'Part_Time': '',
               'Prerequisite_1': 'ATAR',
               'Prerequisite_2': 'IELTS',
               'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': '',
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
               'Blended': 'Yes',
               'Remarks': '',
               'Course Delivery Mode': '',
               'FREE TAFE': ''
               }

possible_cities = {'broadmeadows': 'Melbourne',
                   'docklands': 'Melbourne',
                   'richmond': 'Melbourne',
                   'essendon': 'Melbourne',
                   'workplace': 'Workplace',
                   'moorabbin': 'Melbourne',
                   'moonee ponds': 'Melbourne',
                   'craigieburn': 'Melbourne',
                   'melbourne': 'Melbourne',
                   'bendigo': 'Bendigo',
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


def durationo(word):
    try:
        p_word = word.replace("day", "")
        if p_word:
            if 'full-time' in p_word.lower() and 'part-time' not in p_word.lower():
                course_data['Full_Time'] = 'Yes'
            else:
                course_data['Full_Time'] = 'No'

            if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' not in p_word.lower():
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Part_Time'] = 'No'

            if 'flexible' in p_word.lower():
                course_data['Part_Time'] = "Yes"
                course_data['Full_Time'] = "Yes"

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
    course_name = soup.find("span", class_="h2_text")
    if course_name:
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
    else:
        course_data['Course'] = "....."

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Description
    course_desc = soup.select("#divtab1 p:nth-of-type(4)")
    if course_desc:
        description(course_desc)
    else:
        course_data['Description'] = "N/A"

    # Faculty
    faculty_col = soup.select_one("span#content_0_lbldepartment")
    if faculty_col:
        fac = faculty_col.text
        # print(fac)
        course_data['Faculty'] = fac
    else:
        course_data['Faculty'] = ""

    # Duration
    dura = soup.find("span", id="content_0_lblduration")
    p_word = dura.text
    # print(p_word)
    durationo(p_word)

    # Fees
    gov_subsidised = soup.select("div.fees_div:nth-of-type(2) div.fees_div2")
    if gov_subsidised:
        for govt in gov_subsidised:
            raw_fee = govt.text.strip()
            # print(raw_fee)
            gov_loc = re.match(currency_pattern, raw_fee)
            # print(gov_loc)
            if gov_loc:
                govt_fee = gov_loc.group()
                course_data['Non-Apprentice_Government_Subsidised_Fee'] = govt_fee.replace("$", "").strip()

    concession_fee = soup.select("div.fees_div:nth-of-type(2) div.fees_div3")
    if concession_fee:
        for fee in concession_fee:
            fee_raw = fee.text.strip()
            # print(fee_raw)
            conc_loc_fee = re.search(currency_pattern, fee_raw)
            if conc_loc_fee:
                concession_fe = conc_loc_fee.group()
                course_data['Non-Apprentice_Concession_Fees'] = concession_fe.replace("$", "").strip()

    full_money = soup.select("div.fees_div:nth-of-type(2) div.fees_div4")
    if full_money:
        for loc in full_money:
            local_fee_raw = loc.text.strip()
            # print(local_fee_raw)
            loc_fee = re.search(currency_pattern, local_fee_raw)
            if loc_fee:
                local_fee = loc_fee.group()
                course_data['Non-Apprentice_Full_Fees'] = local_fee.replace("$", "").strip()

    a_gov_subsidised = soup.select("div.fees_div:nth-of-type(3) div.fees_div2")
    if a_gov_subsidised:
        for a_govt in a_gov_subsidised:
            raw_fee = a_govt.text.strip()
            # print(raw_fee)
            gov_loc = re.search(currency_pattern, raw_fee)
            if gov_loc:
                govt_fee = gov_loc.group()
                course_data['Apprentice_Government_Subsidised_Fee'] = govt_fee.replace("$", "").strip()

    a_concession_fee = soup.select("div.fees_div:nth-of-type(3) div.fees_div3")
    if a_concession_fee:
        for fee in a_concession_fee:
            fee_raw = fee.text.strip()
            # print(fee_raw)
            conc_loc_fee = re.search(currency_pattern, fee_raw)
            if conc_loc_fee:
                concession_fe = conc_loc_fee.group()
                course_data['Apprentice_Concession_Fees'] = concession_fe.replace("$", "").strip()

    a_full_money = soup.select("div.fees_div:nth-of-type(3) div.fees_div4")
    if a_full_money:
        for ap_loc in a_full_money:
            local_fee_raw = ap_loc.text.strip()
            loc_fee = re.search(currency_pattern, local_fee_raw)
            if loc_fee:
                local_fee = loc_fee.group()
                course_data['Apprentice_Full_Fees'] = local_fee.replace("$", "").strip()

    # FREE TAFE
    del_mode = soup.find("span", id="content_0_lblinterestarea")
    if del_mode:
        all_info = del_mode.text.lower().strip()
        if "free tafe" in all_info:
            course_data['FREE TAFE'] = "Yes"
        else:
            course_data['FREE TAFE'] = "No"
    else:
        course_data['FREE TAFE'] = "No"

    # LOCATION/CITY
    campus = soup.select("span#content_0_lblcampus")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            # print(campu)
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    else:
        print("Find city")

    # Career Outcomes
    overview = soup.select("#divtab5 p:nth-of-type(3)")
    if overview:
        for ca in overview:
            course_data['Career_Outcomes/path'] = ca.text.strip()
    else:
        course_data['Career_Outcomes/path'] = "None"

    if 'Online' in actual_cities:
        course_data['Online'] = "Yes"
    elif 'Online' not in actual_cities:
        course_data['Online'] = "No"

    if 'Melbourne' in actual_cities or 'Workplace' in actual_cities or 'Bendigo' in actual_cities:
        course_data['Offline'] = "Yes"
    elif 'Melbourne' not in actual_cities or 'Workplace' not in actual_cities or 'Bendigo' not in actual_cities:
        course_data['Offline'] = "No"

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
                      'Non-Apprentice_Government_Subsidised_Fee',
                      'Non-Apprentice_Concession_Fees',
                      'Non-Apprentice_Full_Fees',
                      'Apprentice_Government_Subsidised_Fee',
                      'Apprentice_Concession_Fees',
                      'Apprentice_Full_Fees',
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
                      'Remarks',
                      'Course Delivery Mode',
                      'FREE TAFE']
# tabulate our data

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

browser.quit()
