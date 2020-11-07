"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 04-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/QUT_link.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/QUT_unordered.csv'

course_data = {'Level_Code': '',
               'University': 'Queensland University of Technology',
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
               'Prerequisite_3': 'Equivalent ',
               'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': '',
               'Prerequisite_3_grade_3': 'Year 12',
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
               'Remarks': ''}

possible_cities = {'kelvin grove': 'Brisbane',
                   'gardens point': 'Brisbane',
                   'sydney': 'Sydney',
                   'canberra': 'Canberra',
                   'brisbane': 'Brisbane'
                   }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hidden-lg-up"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.strip().replace("\n", " ").strip()


for each_url in course_links_file:
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip().replace("?international", "").strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.select(
        "body > div.header__wrapper > div.hero__header.course__page > div.hero__header__container.container > div > h1 > span")
    if course_name:
        for course in course_name:
            course_title = tag_text(course)
            course_data['Course'] = course_title
    else:
        course_name2 = soup.find("h1")
        if course_name2:
            print(course_name2)
            course_data['Course'] = course_name2.text.strip()
        else:
            course_data['Course'] = ""

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    if "/" in course_data['Course']:
        course_data['Faculty'] = "Double Degree"

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # print(course_data['Course'], course_data['Website'], course_data['Faculty'], course_data['Level_Code'])

    # city/study mode
    temp_line = soup.select(".push-md-1[data-course-audience='INT'] dl")  # li
    temp_city = soup.select(".campus-icon.push-md-1 dl")
    if temp_line:
        for each_mode in temp_line:
            delivery = each_mode.text.lower()

            if 'online' in delivery or 'external' in delivery:
                course_data['Online'] = "Yes"
            else:
                course_data['Online'] = "No"

            for i in possible_cities:
                if i in delivery:
                    actual_cities.append(possible_cities[i])
    elif temp_city:
        for each_mode in temp_city:
            delivery = each_mode.text.lower()
            if 'online' in delivery or 'external' in delivery:
                course_data['Online'] = "Yes"
            else:
                course_data['Online'] = "No"

            for i in possible_cities:
                if i in delivery:
                    actual_cities.append(possible_cities[i])

    if actual_cities is not "":
        course_data['Offline'] = "Yes"
        course_data['Face_to_Face'] = "Yes"

    else:
        course_data['Offline'] = "No"
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Face_to_Face'] and "Yes" in course_data['Online']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    if "Yes" in course_data['Online']:
        course_data['Distance'] = "Yes"
    else:
        course_data['Distance'] = "No"

    # Duration/Duration Time/FullTime/Parttime/
    # course_detail = soup.select("dt:contains('Duration') + .col-sm-12 li")
    course_detail = soup.select("div.duration-icon")
    for ra in course_detail:
        try:
            course_duration = ra.text
            if course_duration:
                p_word = course_duration.__str__().strip()
                if p_word:
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

                    if 'year' in p_word.__str__().lower():
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                        duration_time = value_conv[1]

                        if str(duration) == '1' or str(duration) == '1.0':
                            duration_time = 'Year'
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time
                        elif 'month' in duration_time.__str__().lower():
                            value_conv = DurationConverter.convert_duration(p_word)
                            duration_time = 'Months'
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time
                        else:
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time

                    elif 'months' in p_word.__str__().lower():
                        value_conv = DurationConverter.convert_duration(p_word)
                        duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = 'Months'
                    else:
                        course_data['Duration'] = "Find it"
                        course_data['Duration_Time'] = ''
                else:
                    course_data['Duration'] = "Not Provided"
                    course_data['Duration_Time'] = ''
            else:
                course_data['Duration'] = "Not Shown"
                course_data['Duration_Time'] = ''
        except IndexError:
            course_data['Full_Time'] = ''
            course_data['Part_Time'] = ''
            course_data['Duration'] = ''
            course_data['Duration_Time'] = ''
            print(course_data['Course'] + "this course doesn't have information pertaining to duration")
    print(course_data['Duration'], course_data['Duration_Time'], course_data['Full_Time'], actual_cities,
          course_data['Part_Time'], course_data['Website'])
    # print(actual_cities,
    #      course_data['Website'], "Duration:", course_data['Duration'], course_data['Duration_Time'],
    #     "Parttime:", course_data['Part_Time'], "Fulltime:",course_data['Full_Time'],
    #      "Online:", course_data['Online'], "Offline:", course_data['Offline'])

    # Description
    course_highlights = soup.select("[data-course-audience='INT'] .panel-content ul")
    courseDescription0 = soup.select(
        "body > div.header__wrapper > div.hero__header.course__page > div.hero__header__container.container > div > div > p")
    courseDescription1 = soup.select(
        "body > div.header__wrapper > div > div.hero__header__container.container > div > div")
    courseDescription2 = soup.select("#what-to-expect-tab > div > div.panel-content.row > div")
    if course_highlights:
        description(course_highlights)
    elif courseDescription0:
        description(courseDescription0)
    elif courseDescription1:
        description(courseDescription1)
    elif courseDescription2:
        description(courseDescription2)
    else:
        course_data['Description'] = "N/A"

    # career Outcome
    career = soup.select(".course-possible-careers ul")
    if career:
        for each_career in career:
            course_data['Career_Outcomes/path'] = each_career.text.strip().replace("\n", ", ")
    else:
        course_data['Career_Outcomes/path'] = "No career outcomes provided"

    # IELTS
    try:
        ielts_col = soup.select("td#elt-overall.IELTS")
        if ielts_col:
            for ea in ielts_col:
                ielts_amount = ea.text.strip()
                if has_numbers(ielts_amount):
                    ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                    course_data['Prerequisite_2_grade_2'] = ielts
                else:
                    course_data['Prerequisite_2_grade_2'] = "N/A"
        else:
            course_data['Prerequisite_2_grade_2'] = "N/A"
    except AttributeError:
        course_data['Prerequisite_2_grade_2'] = "N/A"

    # print(course_data['Prerequisite_2_grade_2'], course_data['Career_Outcomes/path'], course_data['Website'],
    #      course_data['Description'])

    # Int fees
    try:
        int_amount = soup.select(
            "#fees-tab > div > div.panel-content.row > div > div.row.full-panel.boxed-heading-panel.boxes-with-block-heading-panel.course_tab_content.course_tab_content__fees.panel-no-pt.panel-no-pb.panel-white.grey-titles.active > div > div > div:nth-child(2) > div > div.box-content > p:nth-child(1)")
        if int_amount:
            for each_int in int_amount:
                Int_feeRa = tag_text(each_int)
                int_fee = Int_feeRa.split(" ")
                Int_feeRaw = int_fee[1]
                Int_fee = re.findall(currency_pattern, Int_feeRaw)[0]
                if Int_fee:
                    course_data['Int_Fees'] = Int_fee.replace("$", "").strip()
        else:
            course_data['Int_Fees'] = "N/A"

    except IndexError:
        course_data['Int_Fees'] = "N/A"

    # Find button for domestic values
    try:
        if browser.find_element_by_xpath("//a[contains(@href, '?domestic')]"):
            browser.find_element_by_xpath("//a[contains(@href, '?domestic')]").click()
            time.sleep(5)
            browser.get(browser.current_url)
            dom_url = browser.page_source

            soup2 = bs4.BeautifulSoup(dom_url, 'lxml')

    except Exception:
        pass

    # Local_fee
    try:
        latest_local = soup2.select(
            "#fees-tab > div > div.panel-content.row > div > div.row.full-panel.boxed-heading-panel.boxes-with-block-heading-panel.course_tab_content.course_tab_content__fees.panel-no-pt.panel-no-pb.panel-white.grey-titles.active > div > div > div:nth-child(1) > div > div.box-content > p")
        local_amount = soup2.select("[data-course-audience='DOM'] .box-content p")
        if latest_local:
            for each_local in latest_local:
                local_feeRaw = tag_text(each_local)
                local_fee = re.findall(currency_pattern, local_feeRaw)[0]
                if local_fee:
                    course_data['Local_Fees'] = local_fee
                else:
                    course_data['Local_Fees'] = "N/A"
        elif local_amount:
            for each_loc in local_amount:
                local_feeRaw = tag_text(each_loc)
                local_fee = re.findall(currency_pattern, local_feeRaw)[0]
                if local_fee:
                    course_data['Local_Fees'] = local_fee
                else:
                    course_data['Local_Fees'] = "N/A"
        else:
            course_data['Local_Fees'] = "N/A"

    except IndexError:
        another_local = soup2.select("[data-course-audience='DOM'] .box-content p:nth-of-type(1)")
        if another_local:
            for each_local in another_local:
                local_feeRaw = tag_text(each_local)
                local_fee = re.findall(currency_pattern, local_feeRaw)
                if local_fee:
                    course_data['Local_Fees'] = local_fee[0]
                else:
                    course_data['Local_Fees'] = "N/A"
        else:
            course_data['Local_Fees'] = "N/A"

    # Prerequisites 1
    try:
        pre_req_1 = soup2.find("dl", class_="quick-box-scores").find("dd", class_="rank")
        if pre_req_1:
            atar_value = pre_req_1.text
            if has_numbers(atar_value):
                atar = re.findall(r'\d+(?:\.*\d*)?', atar_value)[0]
                course_data['Prerequisite_1_grade_1'] = atar
            else:
                course_data['Prerequisite_1_grade_1'] = "N/A"
        else:
            course_data['Prerequisite_1_grade_1'] = "N/A"  # RN
    except AttributeError:
        course_data['Prerequisite_1_grade_1'] = "N/A"

    # print(course_data['Website'], course_data['Local_Fees'],course_data['Prerequisite_1_grade_1'])

    # print(course_data['Int_Fees'],course_data['Description'])

    # Availability
    av = soup2.select(".dom-int-tabs-message.hidden-md-down span")
    if av:
        for va in av:
            if "only available for Australian and New Zealand" in va.text:
                course_data['Availability'] = "D"
            elif "only available for international" in va.text:
                course_data['Availability'] = "I"
            else:
                course_data['Availability'] = "A"
    else:
        print("Cant Find", course_data['Website'])

    if "D" in course_data['Availability']:
        course_data['Int_Fees'] = " N/A"
    elif "I" in course_data['Availability']:
        course_data['Local_Fees'] = "N/A"

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


ordered_file = csv_file_path.parent.__str__() + "/QUT_alldegrees_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)


