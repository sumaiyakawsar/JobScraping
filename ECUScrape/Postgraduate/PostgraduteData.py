"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 28-10-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
from bs4 import Comment
import requests
import os
import copy
import DurationConverter
import TemplateData

# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument('--no-sandbox')
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/ECU_pG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/ECU_PG_unordered.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("em"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'Edith Cowan University',
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
               'Prerequisite_1': 'Academic Requirement',
               'Prerequisite_2': 'IELTS',
               'Prerequisite_3': ' ',
               'Prerequisite_1_grade_1': 'Bachelor degree',
               'Prerequisite_2_grade_2': '6.5',
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
               'Blended': 'Yes',
               'Remarks': ''}

possible_cities = {'joondalup': 'Perth',
                   'mount lawley': 'Perth',
                   'south west': 'Bunbury',
                   'perth': 'Perth',
                   'bunbury': 'Bunbury'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

for each_url in course_links_file:
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(0.1)

    # COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE & course level
    courseName = soup.find("nav", class_="heroBanner__breadcrumbs")
    if courseName:
        for tag in courseName.find_all("a"):
            tag.decompose()
        course = courseName.get_text(" ", strip=True).replace("/", " ").strip()
        course_data['Course'] = course
    else:
        course_data['Course'] = soup.find("h1").text

    # Description
    courseDescription = soup.find("div", class_="bannerContent bannerContent--wide")
    courseDesc2 = soup.select(".overviewbody p")
    if courseDescription:
        course_data['Description'] = courseDescription.text.strip().replace("\n", "")
    else:
        for ea in courseDesc2:
            course_data['Description'] = ea.text.strip()

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # local fees
    try:
        localmoney = soup.select(
            "#overview > div.quickReference.audience__panel--domestic > div:nth-child(4) > p:nth-child(2) > span > strong")
        if localmoney:
            for local in localmoney:
                local_feeRaw = tag_text(local)
                local_fee = re.findall(currency_pattern, local_feeRaw)[1].replace('$', '')
                if local_fee:
                    course_data['Local_Fees'] = local_fee
                else:
                    course_data['Local_Fees'] = "cant find you"
        else:
            more_Local = soup.select(".progdetails li:nth-of-type(4)")
            if more_Local:
                for ea in more_Local:
                    local_rawfee = tag_text(ea)
                    local_fees = re.findall(currency_pattern, local_rawfee)[1].replace('$', '')
                    if local_fees:
                        course_data['Local_Fees'] = local_fees
            else:
                course_data['Local_Fees'] = 'Research training program'
    except IndexError:
        course_data['Local_Fees'] = ""

    # international_fees
    try:
        moneyColumn = soup.select(
            "#overview > div.quickReference.audience__panel--international > div:nth-child(4) > p:nth-child(2) > span > strong")
        if moneyColumn:
            for ea in moneyColumn:
                int_feeRaw = tag_text(ea)
                int_fee = re.findall(currency_pattern, int_feeRaw)[1].replace('$', '')
                if int_fee:
                    course_data['Int_Fees'] = int_fee
                else:
                    course_data['Int_Fees'] = "cant"
        else:
            Int_money = soup.select(".audience__panel--international strong")
            if Int_money:
                for ea in Int_money:
                    int_raw_fee = tag_text(ea)
                    int_fees = re.findall(currency_pattern, int_raw_fee)[1].replace('$', '')
                    if int_fees:
                        course_data['Int_Fees'] = int_fees

            else:
                more_int = soup.select(".progdetails li:nth-of-type(4)")
                if more_int:
                    for ea in more_int:
                        int_raw_fee = tag_text(ea)
                        int_fees = re.findall(currency_pattern, int_raw_fee)[1].replace('$', '')
                        if int_fees:
                            course_data['Int_Fees'] = int_fees
                else:
                    course_data['Int_Fees'] = 'No fee'
    except IndexError:
        course_data['Int_Fees'] = ""

    if 'No fee' in course_data['Int_Fees']:
        course_data['Availability'] = "D"
    else:
        course_data['Availability'] = "A"
    # print(course_data['Int_Fees'],course_data['Local_Fees'], course_data['Website'],course_data['Availability'])

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    # print(course_data['Faculty'], course_data['Course'],course_data['Website'])

    # Duration/Duration Time/FullTime/Parttime/
    course_detail = soup.select(
        "#overview > div.quickReference.audience__panel--international > div:nth-child(5) > p:nth-child(2)")
    # print(course_detail)
    for ra in course_detail:
        try:
            course_duration = ra.text
            if course_duration:
                p_word = course_duration.__str__().strip()
                if 'full-time' in p_word.lower() and 'part-time' not in p_word.lower():
                    course_data['Full_Time'] = 'Yes'
                else:
                    course_data['Full_Time'] = 'No'
                if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' not in p_word.lower():
                    course_data['Part_Time'] = 'Yes'
                else:
                    course_data['Part_Time'] = 'No'
                if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' in p_word.lower():
                    course_data['Blended'] = 'Yes'
                    course_data['Full_Time'] = 'Yes'
                    course_data['Part_Time'] = 'Yes'
                else:
                    course_data['Blended'] = 'No'

                if 'year' in p_word.__str__().lower() or 'years' in p_word.__str__().lower():
                    value_conv = DurationConverter.convert_duration(p_word)
                    duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                    duration_time = 'Years'
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = duration_time

                    if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                        duration_time = 'Year'
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = duration_time
                        # print('DURATION + DURATION TIME: ', duration, duration_time)

                    elif 'month' in duration_time.__str__().lower():
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                        duration_time = 'Months'
                        if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                            duration_time = 'Month'
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = duration_time

                else:
                    another_place = soup.select(".audience__panel--international div:nth-of-type(4) p:nth-of-type(1)")
                    for ro in another_place:
                        try:
                            course_duration2 = ro.text
                            if course_duration2:
                                p_word = course_duration2.__str__().strip()
                                if 'full-time' in p_word.lower() and 'part-time' not in p_word.lower():
                                    course_data['Full_Time'] = 'Yes'
                                else:
                                    course_data['Full_Time'] = 'No'
                                if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' not in p_word.lower():
                                    course_data['Part_Time'] = 'Yes'
                                else:
                                    course_data['Part_Time'] = 'No'
                                if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' in p_word.lower():
                                    course_data['Blended'] = 'Yes'
                                    course_data['Full_Time'] = 'Yes'
                                    course_data['Part_Time'] = 'Yes'
                                else:
                                    course_data['Blended'] = 'No'

                                if 'year' in p_word.__str__().lower() or 'years' in p_word.__str__().lower():

                                    value_conv = DurationConverter.convert_duration(p_word)

                                    duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                                    duration_time = 'Years'
                                    course_data['Duration'] = duration
                                    course_data['Duration_Time'] = duration_time
                                    # print(duration)

                                    if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                                        duration_time = 'Year'
                                        course_data['Duration'] = duration
                                        course_data['Duration_Time'] = duration_time
                                        # print('DURATION + DURATION TIME: ', duration, duration_time)
                                    elif 'month' in duration_time.__str__().lower():
                                        value_conv = DurationConverter.convert_duration(p_word)
                                        duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                                        duration_time = 'Months'
                                        if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                                            duration_time = 'Month'
                                        course_data['Duration'] = duration
                                        course_data['Duration_Time'] = duration_time
                                else:
                                    course_data['Duration'] = ''
                                    course_data['Duration_Time'] = ''
                            if "not offered" in course_duration2:
                                course_data['Availability'] = 'D'
                                course_data['Full_Time'] = 'Yes'
                                course_data['Part_Time'] = 'Yes'
                            else:
                                course_data['Availability'] = 'A'
                        except IndexError:
                            course_data['Full_Time'] = ''
                            course_data['Part_Time'] = ''
                            course_data['Duration'] = ''
                            course_data['Duration_Time'] = ''
                            print(course_data['Course'], "this course doesn't have information pertaining to duration")

            if "not offered" in course_duration:
                course_data['Availability'] = 'D'
                course_data['Full_Time'] = 'Yes'
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Availability'] = 'A'
        except IndexError:
            course_data['Full_Time'] = ''
            course_data['Part_Time'] = ''
            course_data['Duration'] = ''
            course_data['Duration_Time'] = ''
            print("this course doesn't have information pertaining to duration")

    # print(course_data['Duration'], course_data['Duration_Time'])

    # Career Outcome
    careerDetails = soup.select("#careerOpportunities p:nth-of-type(2)")
    if careerDetails:
        for ea in careerDetails:
            course_data['Career_Outcomes/path'] = ea.text
    else:
        another_career_data = soup.select("#careerOpportunities p")
        if another_career_data:
            for ea in another_career_data:
                course_data['Career_Outcomes/path'] = ea.text
        else:
            another_one = soup.select(".col-full.header_only ul")
            if another_one:
                for ea in another_one:
                    course_data['Career_Outcomes/path'] = ea.text.strip().replace('\n', ', ').strip()
            else:
                course_data['Career_Outcomes/path'] = "Not provided in the website"
    # print(course_data['Website'], course_data['Career_Outcomes/path'])

    # Online/Offline/Face to face/Distance
    city_present = soup.select("#courseDetails > div.audience__panel.audience__panel--domestic > p:nth-child(2)")
    for each in city_present:
        tempLine = each.text.lower()

        for i in possible_cities:
            if i in tempLine and 'online' not in tempLine:

                course_data['Online'] = "No"
                if i in tempLine:
                    actual_cities.append(possible_cities[i])

                if 'online' not in tempLine:
                    course_data['Online'] = "No"
                else:
                    course_data['Online'] = "Yes"

            elif 'online' in tempLine and i in tempLine:

                course_data['Online'] = "Yes"
                if i in tempLine:
                    actual_cities.append(possible_cities[i])

                if 'online' in tempLine:
                    course_data['Online'] = "Yes"
                else:
                    course_data['Online'] = "No"

            elif 'online' in tempLine and i not in tempLine:
                course_data['Online'] = "Yes"
                if 'online' in tempLine:
                    course_data['Online'] = "Yes"
                else:
                    course_data['Online'] = "No"

    if actual_cities:
        course_data['Offline'] = "Yes"
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Offline'] = "No"
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Online']:
        course_data['Distance'] = "Yes"
    else:
        course_data['Distance'] = "No"

    #print(course_data['Website'], actual_cities,"Online:", course_data['Online'],"Offline:", course_data['Offline'],"Facetoface:", course_data['Face_to_Face'],"Distance", course_data['Distance'])

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
                      'Local_Fees',
                      'Int_Fees',
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

ordered_file = csv_file_path.parent.__str__() + "/ECU_PG_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.close()
