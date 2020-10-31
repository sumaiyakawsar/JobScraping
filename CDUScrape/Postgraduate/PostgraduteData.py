"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
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
course_links_file_path = course_links_file_path.__str__() + '/CDU_PG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/CDU_UG_unordered.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("em"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'Charles Darwin University',
               'City': '',
               'Course': '',
               'Faculty': '',
               'Int_Fees': '',
               'Local_Fees': '',
               'Currency': 'AUD',
               'Currency_Time': 'Years',
               'Duration': '',
               'Duration_Time': '',
               'Full_Time': 'Yes',
               'Part_Time': 'No',
               'Prerequisite_1': '',
               'Prerequisite_2': '',
               'Prerequisite_3': '',
               'Prerequisite_1_grade_1': '',
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
               'Blended': 'Yes',
               'Remarks': ''}

possible_cities = {'palmerston': 'Darwin',
                   'casuarina': 'Darwin',
                   'alice springs': 'Adelaide',
                   'sydney': 'Sydney',
                   'darwin':'Darwin',
                   'adelaide':'Adelaide',
                   'online': 'Online'}

currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

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
    courseName = soup.find("div", class_="container section-header__content")
    if courseName:
        course = courseName.find("h1").text.strip()
        course_data['Course'] = course

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    # print(course_data['Course'], course_data['Website'],course_data['Level_Code'])

    # Description
    courseDescription = soup.select(
        "#course-overview > div.grid > div > div.grid__col.grid--col-7.grid--offset-1 > div.field.field-ds-chainsnode-course-content-field-course-course-overview.field-type-ds.field-label-hidden > div > div > div > p:nth-child(1)")
    if courseDescription:
        for ea in courseDescription:
            course_data['Description'] = ea.text.strip()
    else:
        course_data['Description'] = ""
    # print(course_data['Course'],course_data['Website'],course_data['Description'])

    # international_fees
    try:
        moneyColumn = soup.select(".field-international-fee-value .field-item div")
        if moneyColumn:
            for ea in moneyColumn:
                int_feeRaw = tag_text(ea)
                int_fee = re.findall(currency_pattern, int_feeRaw)[0].replace("$", "").strip()
                if int_fee:
                    course_data['Int_Fees'] = int_fee
                    course_data['Availability'] = "A"
        else:
            information = soup.select(".field-international-admissions-in div.field-item")
            if information:
                for ea in information:
                    if "No" in ea.text:
                        course_data['Int_Fees'] = "N/A"
                        course_data['Availability'] = "D"
            else:
                course_data['Int_Fees'] = "cudntcatch"
    except IndexError:
        course_data['Int_Fees'] = "umm error"

    # print(course_data['Int_Fees'], course_data['Website'], course_data['Availability'])

    # local fees
    course_data['Local_Fees'] = "CSP supported"

    # DECIDE THE FACULTY
    facultyCell = soup.select(".field-faculty div")
    if facultyCell:
        for ea in facultyCell:
            faculty = ea.text.strip()
            course_data['Faculty'] = faculty



    # Duration/Duration Time
    course_detail = soup.select(".field-duration-ft div")
    for ra in course_detail:
        try:
            course_duration = ra.text
            if course_duration:
                p_word = course_duration.__str__().strip()
                if 'year' in p_word.__str__().lower():
                    value_conv = DurationConverter.convert_duration(p_word)
                    duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                    duration_time = 'Years'
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = duration_time

                    if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                        duration_time = 'Year'
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = duration_time
                    elif 'month' in duration_time.__str__().lower():
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                        duration_time = 'Months'
                        if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                            duration_time = 'Month'
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = duration_time
        except IndexError:
            course_data['Duration'] = 'error'
            course_data['Duration_Time'] = ''



    # Career Outcome
    careerDetails = soup.select(".field-career-opportunities")
    if careerDetails:
        for ea in careerDetails:
            course_data['Career_Outcomes/path'] = ea.text.strip().replace("\n", " ")
    else:
        course_data['Career_Outcomes/path'] = "Not provided in the website"
    #print(course_data['Career_Outcomes/path'])
    """
    # Fulltime/Parttime
    fulltime = soup.find("div",class_="grid__col grid--col-4").find_all(text="Full-time")
    parttime = soup.find("div",class_="grid__col grid--col-4").find_all(text="Part-time")
    if fulltime:
        course_data['Full_Time'] = "Yes"
    else:
        course_data['Full_Time'] = "No"
    if parttime:
        course_data['Part_Time'] = "Yes"
    else:
        course_data['Part_Time'] = "No"

    #print(course_data['Course'], course_data['Full_Time'], course_data['Part_Time'],course_data['Website'])
    """

    # Online/Offline/Face to face/Distance
    city_present = soup.select("div.grid--col-4")
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
                course_data['Offline'] = "No"
                course_data['Online'] = "Yes"
                if 'online' in tempLine:
                    course_data['Online'] = "Yes"
                else:
                    course_data['Online'] = "No"
    print(actual_cities,course_data['Website'])
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

ordered_file = csv_file_path.parent.__str__() + "/CDU_PG_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.close()
