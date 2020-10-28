"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 27-10-20
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
course_links_file_path = course_links_file_path.__str__() + '/UNE_UG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/UNE_UG_unordered.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("em"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'University of New England',
               'City': 'Armidale',
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
               'Prerequisite_2': '',
               'Prerequisite_3': '',
               'Prerequisite_1_grade_1': '0',
               'Prerequisite_2_grade_2': '',
               'Prerequisite_3_grade_3': '',
               'Website': '',
               'Course_Lang': 'English',
               'Availability': '',
               'Description': '',
               'Career_Outcomes/path': '',
               'Country': 'Australia',
               'Online': 'Yes',
               'Offline': 'Yes',
               'Distance': 'Yes',
               'Face_to_Face': 'Yes',
               'Blended': 'Yes',
               'Remarks': ''}


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
    try:
        courseName = soup.select('#main-content > div > div:nth-child(2) > h2')
        if courseName:
            for course in courseName:
                course_title = tag_text(course)
                course_data['Course'] = course_title
                course_data['Availability'] = "A"
    except IndexError:
        anothername = soup.select('#main-content > div > h2')
        if anothername:
            for course in anothername:
                course_title = tag_text(course)
                course_data['Course'] = course_title
                course_data['Availability'] = "N"
    """
      if 'Bachelor' in course_data['Course'] and 'Honours' in course_data['Course']:
        course_level = "Bachelor Honours"
    elif 'Bachelor' in course_data['Course']:
        course_level = "Bachelor"
    
    """
    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    #print(course_data['Course'],course_data['Level_Code'], course_data['Faculty'])

    # Description
    degree_details = soup.select('#overviewTab-leftColumn p:nth-of-type(1) ')
    if degree_details:
        for ea in degree_details:
            describe = ea.text
            course_data['Description'] = describe
            if 'no longer' in describe:
                course_data['Availability'] = 'N'

    # Career Outcome
    careerOptions = soup.select('h4')
    for each in careerOptions:
        if 'Career Opportunities' in each.text:
            careerDetails = soup.select("#overviewTab-leftColumn > p:nth-child(10) ")
            for ra in careerDetails:
                course_data['Career_Outcomes/path'] = ra.text

    coursedetails = soup.find(id="furtherInformationTable").find('tbody').find_all('tr')
    for ra in coursedetails:
        try:
            courseduration = soup.select("tr:contains('Course Duration') td:nth-of-type(2) ul li")
            if courseduration:
                p_word = courseduration.__str__().strip().replace("<li>","")\
                    .replace("</li>","").replace('[','').replace(']','').strip()

                if 'full-time' in p_word.lower() and 'part-time' not in p_word.lower():
                    course_data['Full_Time'] = 'Yes'
                else:
                    course_data['Full_Time'] = 'No'
                if 'part-time' in p_word.lower() or 'part' in p_word.lower() and 'full-time' not in p_word.lower():
                    course_data['Part_Time'] = 'Yes'
                else:
                    course_data['Part_Time'] = 'No'
                if "Yes" in course_data['Full_Time'] and "Yes" in course_data['Part_Time']:
                    course_data['Blended'] = 'Yes'
                else:
                    course_data['Blended'] = 'No'

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
                        # print('DURATION + DURATION TIME: ', duration, duration_time)
                    elif str(duration) == '0.5':
                        duration_time = 'Months'
                        course_data['Duration'] = '6'
                        course_data['Duration'] = duration_time
                    elif 'month' in duration_time.__str__().lower():
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                        duration_time = 'Months'
                        if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                            duration_time = 'Month'
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = duration_time

        except IndexError:
            course_data['Full_Time'] = ''
            course_data['Part_Time'] = ''
            course_data['Duration'] = ''
            course_data['Duration_Time'] = ''
            print("this course doesn't have information pertaining to duration")

    #print(course_data['Duration'], course_data['Duration_Time'])

    moredetails = soup.find(id="overviewTab-snapshotDiv")
    if moredetails:
        atar = moredetails.select("#overviewTab-snapshotDiv > p:nth-child(7)")
        if atar:
            for ea in atar:
                try:
                    if ea:
                        atar_raw = ea.text
                        atar_value = re.findall(r'\d{2}\.\d{2}', atar_raw)[0]
                        course_data['Prerequisite_1_grade_1'] = atar_value
                except IndexError:
                    course_data['Prerequisite_1_grade_1'] = " "

    #print(course_data['Prerequisite_1_grade_1'])

    factsHeader = soup.select('#overviewTab-snapshotDiv > p:nth-child(10)')
    for ia in factsHeader:
        tempLine = ia.text.lower()
        if 'online' in tempLine:
            course_data['Online'] = "Yes"
            course_data['Distance'] = "Yes"
        if 'on campus' in tempLine:
            course_data['Offline'] = "Yes"
            course_data['Face_to_Face'] = "Yes"
    #print(course_data['Online'],course_data['Offline'],course_data['Face_to_Face'])

    # Course fees
    """
    try:
        moneyColumn = soup.select("tr:contains('Fees') li")
        
        if moneyColumn:
            for ea in moneyColumn:
                int_feeRaw = tag_text(ea)
                int_fee = re.findall(currency_pattern, int_feeRaw)[0].replace('AUD', '')
                if int_fee:
                    course_data['Int_Fees'] = int_fee
                else:
                    course_data['Int_Fees'] = " "

    except IndexError:
        course_data['Int_Fees'] = ""
    """
    print(course_data['Course'], course_data['Website'])

    course_data_all.append(copy.deepcopy(course_data))

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

ordered_file = csv_file_path.parent.__str__() + "/UNC_UG_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
