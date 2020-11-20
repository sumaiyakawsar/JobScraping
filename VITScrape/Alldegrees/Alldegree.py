"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/vit_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/vit_unordered.csv'

course_data = {'Level_Code': '',
               'University': 'Victorian Institute of Technology',
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
               'Prerequisite_1': 'IELTS',
               'Prerequisite_2': 'Equivalent AQF Level',
               'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': '',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': '',
               'Description': '',
               'Career_Outcomes/path': '',
               'Country': 'Australia',
               'Online': '',
               'Offline': 'Yes',
               'Distance': '',
               'Face_to_Face': 'Yes',
               'Blended': '',
               'Remarks': ''
               }

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
    for tag in soup_.find_all("span"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        if each_desc is not None:
            course_data['Description'] = each_desc.text.replace("\n"," ").replace("About","").strip()
        else:
            course_data['Description'] = "where"


def local_money_r(loc_money):
    for loc in loc_money:
        local_fee_raw = loc.text.replace("AUD","").replace(" ","").strip()
        #print(local_fee_raw)
        loc_fee = re.search(currency_pattern, local_fee_raw)
        if loc_fee:
            local_fee = loc_fee.group()
            course_data['Local_Fees'] = local_fee.replace("$", "").strip()

        else:
            print("Loco")


def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text.replace("AUD","").replace(" ","").strip()
        #print(int_fee_raw)
        Int_fee = re.search(currency_pattern, int_fee_raw)
        Int_fee_2 = re.search(number,int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            course_data['Int_Fees'] = int_fee.replace("$", "").strip()
        elif Int_fee_2:
            int_fee = Int_fee_2.group()
            course_data['Int_Fees'] = int_fee.strip()
        else:
            print("Wah")


def durationo(p_word):
    try:
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
        course_data['Duration'] = 'ex'
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

    # print(course_data['Course'], "////", course_data['Level_Code'], course_data['Website'])

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
    else:
        pass
        # print("Look")

    #print(course_data['Website'],course_data['Local_Fees'],course_data['Int_Fees'])

    # LOCATION/CITY
    campus = soup.select("tr:contains('Delivery Locations') td.table-data-right")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    else:
        pass
    # print(actual_cities, course_data['Website'], course_data['Level_Code'])

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
    career = soup.select("tr:contains('Employment Pathway') td:nth-of-type(2)")
    career2 = soup.select("div:contains('EMPLOYMENT PATHWAY') div.col-md-12")

    if career:
        for car in career:
            course_data['Career_Outcomes/path'] = car.text.replace("\n",",").strip()
    elif career2:
        for car in career2:
            course_data['Career_Outcomes/path'] = car.text.replace("\n",",").strip()
    else:
        course_data['Career_Outcomes/path'] = "None"


    #Fulltome/Part
    ft_pt = soup.select_one(".in .table-row-5 td.table-data-right")
    if ft_pt:
        ft_pt_lower = ft_pt.text.lower()
        print(ft_pt_lower)
        if 'full time' in ft_pt_lower and 'part time' not in ft_pt_lower:
            course_data['Full_Time'] = 'Yes'
        else:
            course_data['Full_Time'] = 'No'

        if 'part time' in ft_pt_lower or 'part' in ft_pt_lower and 'full time' not in ft_pt_lower:
            course_data['Part_Time'] = 'Yes'
        else:
            course_data['Part_Time'] = 'No'

        if 'part time' in ft_pt_lower or 'part' in ft_pt_lower and 'full time' in ft_pt_lower:
            course_data['Part_Time'] = 'Yes'
            course_data['Full_Time'] = 'Yes'

        if 'online'  in ft_pt_lower:
            course_data['Online'] = "Yes"
        else:
            course_data['Online'] = "No"

        if 'blended' in ft_pt_lower:
            course_data['Blended'] ="Yes"
        else:
            course_data['Blended'] = "No"

    if "Yes" in course_data['Online'] and "Yes" in course_data['Offline']:
        course_data['Blended'] = "Yes"
    if "Yes" in course_data['Online']:
        course_data['Distance'] = "Yes"
    else:
        course_data['Distance'] = "No"









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
                      'Remarks',
                     ]
# tabulate our data
course_dict_keys = set().union(*(d.keys() for d in course_data_all))

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, course_dict_keys)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

ordered_file = csv_file_path.parent.__str__() + "/vit_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
