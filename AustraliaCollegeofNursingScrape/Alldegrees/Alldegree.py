"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 26-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/ACN_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/ACN_allcourses.csv'

# Subject details
csv_file_single_path = Path(os.getcwd().replace('\\', '/'))
csv_file_single_path = csv_file_single_path.__str__() + '/ACN_single_unit_study.csv'
csv_file_single_unit = open(csv_file_single_path, 'r')
"""
for each in csv_file_single_unit:
    print(csv_file_single_unit.readline())
"""
course_data = {'Level_Code': '',
               'University': 'Australian College of Nursing',
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
               'Prerequisite_1_grade_1': '',
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
               'Blended': '',
               'Remarks': '',
               'Subjects_or_Units': '',
               }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("h3"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.replace("\n", "").strip()


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


def online(word_):
    for study in word_:
        study_mod = study.text.lower()
        if 'online' in study_mod:
            course_data['Online'] = "Yes"
        else:
            course_data['Online'] = "No"
        if 'face to face' in study_mod:
            course_data['Offline'] = "Yes"
        else:
            course_data['Offline'] = "No"


for each_url in course_links_file:
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find("div", class_="uvc-sub-heading")
    if course_name:
        clean_tags(course_name)
        course_title = tag_text(course_name).strip()
        course_data['Course'] = course_title
    else:
        course_data['Course'] = ""

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Duration
    dura = soup.select(
        "#overview > div.vc_tta-panel-body > div.vc_row.wpb_row.vc_inner.vc_row-fluid.vc_column-gap-35 > div:nth-child(1) > div > div > div.wpb_text_column.wpb_content_element > div > p")
    for to in dura:
        p_word = to.text
        # print(p_word)
        durationo(p_word)
    # print(course_data['Course'],course_data['Level_Code'],course_data['Website'],course_data['Duration'],course_data['Duration_Time'])

    # Description
    course_desc3 = soup.select(".vc_active div:nth-of-type(5) div")
    course_desc = soup.select(".vc_active div:nth-of-type(6)")
    course_desc2 = soup.select(".ult-vc-hide-row div.wpb_text_column:nth-of-type(1) p")
    course_desc4 = soup.select(".vc_active div:nth-of-type(7) p")
    if course_desc4:
        description(course_desc4)
    elif course_desc3:
        description(course_desc3)
    elif course_desc:
        description(course_desc)
    elif course_desc2:
        description(course_desc2)

    else:
        course_data['Description'] = "N/A"
    # print(course_data['Course'], "///", course_data['Description'], course_data['Website'])

    # OnlineOffline
    study_mode = soup.select("div.vc_col-sm-3:nth-of-type(2) p")
    study_mode2 = soup.select("div.vc_col-sm-6:nth-of-type(2) p")
    study_mode3 = soup.select("div.vc_col-sm-4:nth-of-type(2) p")
    if study_mode:
        online(study_mode)
    elif study_mode3:
        online(study_mode3)
    elif study_mode2:
        online(study_mode2)

    # Career Outcomes
    overview = soup.select("#overview > div.vc_tta-panel-body > div:nth-child(11) > div > p")
    overview2 = soup.select("#overview > div.vc_tta-panel-body > div:nth-child(12) > div > p")
    if overview:
        for career in overview:
            course_data['Career_Outcomes/path'] = career.text.strip()
    elif overview2:
        for career in overview2:
            course_data['Career_Outcomes/path'] = career.text.strip()
    else:
        course_data['Career_Outcomes/path'] = "N/A"

    # tablepress-149-scroll-wrapper
    tab = soup.find(class_="tablepress", text="")
    all_unlist = []

    if "Graduate Certificate in Nursing (Bridging and Re-entry)" in course_data['Course']:
        course_data['Subjects_or_Units'] = "305 – Clinical Nursing Practice in the Australian Healthcare Context," \
                                           "\n304 – Professional Nursing Concepts in Australian Health Care Context "
    elif "Advanced Diploma of Nursing" in course_data['Course']:
        course_data['Subjects_or_Units'] = "N/A"
    elif tab:

        all_course = tab.find_all(class_="column-2")
        for ta in all_course:
            all_units = ta.text
            all_un = all_units.replace("Unit name", "").replace("& pricing", ""). \
                replace("Tier 1", "").replace("Tier 3", "").replace("Tier 2", "").replace("Tier 4", "").strip()
            if all_un is not None:
                all_unlist.append(all_un)

            course_data['Subjects_or_Units'] = all_unlist.__str__().replace("['',","").replace("]","").strip()

    else:
        course_data['Subjects_or_Units'] = "N/A"

    print(course_data['Website'], course_data['Subjects_or_Units'])

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

    course_data_all.append(copy.deepcopy(course_data))

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
                      'Subjects_or_Units'
                      ]
# tabulate our data

with open(csv_file, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

browser.quit()
