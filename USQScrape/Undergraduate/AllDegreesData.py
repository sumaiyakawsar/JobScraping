"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
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
# option.add_argument('--no-sandbox')
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/USQ_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/USQ_unordered.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hide"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'University of Southern Queensland',
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
               'Prerequisite_2_grade_2': '6.5',
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

possible_cities = {'springfield': 'Ipswich',
                   'toowoomba': 'Toowoomba',
                   'ipswich': 'Ipswich',
                   'stanthorpe': 'Stanthorpe'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

for each_url in course_links_file:
    browser.get(each_url)
    each_url = browser.page_source
    soup = bs4.BeautifulSoup(each_url, 'lxml')

    time.sleep(0.5)

    # clean_tags(soup)

    faculty_info = soup.find("h1")
    course_data['Faculty'] = faculty_info.text.strip()

    courses_details = soup.findAll("tr", class_="c-program-table__row")
    for ea in courses_details:
        allsites = []
        actual_cities = []
        course_tag = ea.find("a", class_="c-program-table__program-link")
        course_data['Course'] = course_tag.text.strip().replace("\n", " ")
        course_website = course_tag.get('href')
        course_data['Website'] = course_website
        allsites.append(course_website)

        # DECIDE THE LEVEL CODE
        for i in level_key:
            for j in level_key[i]:
                if j in course_data['Course']:
                    course_data['Level_Code'] = i

        # city/study mode
        studymode = ea.select("td:nth-of-type(2)")
        if studymode:
            for each_mode in studymode:
                if 'Online' in tag_text(each_mode) or 'External' in tag_text(each_mode):
                    course_data['Online'] = "Yes"

                else:
                    course_data['Online'] = "No"
                if 'On-campus' in tag_text(each_mode):
                    course_data['Offline'] = "Yes"
                    course_data['Face_to_Face'] = "Yes"
                    cities = ea.select("td:nth-of-type(3)")
                    if cities:
                        for each_city in cities:
                            temp_line = each_city.text.lower()
                            for i in possible_cities:
                                if i in temp_line:
                                    actual_cities.append(possible_cities[i])
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

        for courses in allsites:
            browser.get(courses)
            courses = browser.page_source

            soup2 = bs4.BeautifulSoup(courses, 'lxml')
            time.sleep(0.5)

            # Local fee
            try:
                localCSP = soup2.select("#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > "
                                        "tbody > tr:contains('Domestic full') > td:nth-child(2)")
                if localCSP:
                    for each_local in localCSP:
                        local_feeRaw = tag_text(each_local)
                        local_fee = re.findall(currency_pattern, local_feeRaw)[0]
                        if local_fee:
                            course_data['Local_Fees'] = local_fee.replace("AUD", "").strip()
                            # print(course_data['Local_Fees'])

                        else:
                            course_data['Local_Fees'] = ""
                            # print(course_data['Local_Fees'])

                else:
                    course_data['Local_Fees'] = "Not provided"
                    localCSP = soup2.select(
                        "#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > "
                        "tbody > tr:contains('Domestic full') > td:nth-child(2)")
                    # print(course_data['Local_Fees'], course_data['Website'])
                    break
            except IndexError:
                course_data['Local_Fees'] = ""

            # Prerequisites 1
            pre_req_1 = soup2.select(
                "#entry-requirements > div:nth-child(2) > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > span")
            if pre_req_1:
                for grade in pre_req_1:
                    if has_numbers(grade):
                        atar = re.findall(r'\d+(?:\.*\d*)?', grade)[0]
                        course_data['Prerequisite_1_grade_1'] = atar
                    else:
                        course_data['Prerequisite_1_grade_1'] = ""
                        break

        #print(course_data['Course'], course_data['Website'], course_data['Prerequisite_1_grade_1'])

        # Duration/Duration Time/FullTime/Parttime/

        course_detail = soup2.select(".col-md-3 li.c-program-summary__list-item")
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
                    if 'full-time' not in p_word.lower() and 'or part-time' in p_word.lower():
                        course_data['Full_Time'] = 'Yes'
                        course_data['Part_Time']= 'Yes'
                    else:
                        course_data['Full_Time'] = 'No'
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
                        course_data['Duration'] = duration
                        course_data['Duration_Time'] = duration_time

                        if duration == '1' or duration == '1.0':
                            duration_time = 'Year'
                            course_data['Duration_Time'] = duration_time
                        elif 'month' in duration_time.__str__().lower():
                            value_conv = DurationConverter.convert_duration(p_word)
                            duration_time = 'Months'
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time

                    else:
                        courses_detail = soup2.select("div:nth-of-type(6) li.c-program-summary__list-item")
                        for ra in courses_detail:
                            try:
                                course_duration = ra.text
                                if course_duration:
                                    p_word = course_duration.__str__().strip()
                                    if 'full time' in p_word.lower() and 'part time' not in p_word.lower():
                                        course_data['Full_Time'] = 'Yes'
                                    else:
                                        course_data['Full_Time'] = 'No'
                                    if 'part time' in p_word.lower() or 'part' in p_word.lower() and 'full time' not in p_word.lower():
                                        course_data['Part_Time'] = 'Yes'
                                    else:
                                        course_data['Part_Time'] = 'No'
                                    if 'full-time' not in p_word.lower() and 'or part-time' in p_word.lower():
                                        course_data['Full_Time'] = 'Yes'
                                        course_data['Part_Time'] = 'Yes'
                                    else:
                                        course_data['Full_Time'] = 'No'
                                    if 'part time' in p_word.lower() or 'part' in p_word.lower() and 'full time' in p_word.lower():
                                        course_data['Blended'] = 'Yes'
                                        course_data['Full_Time'] = 'Yes'
                                        course_data['Part_Time'] = 'Yes'
                                    else:
                                        course_data['Blended'] = 'No'

                                    if 'year' in p_word.__str__().lower():
                                        value_conv = DurationConverter.convert_duration(p_word)
                                        duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                                        duration_time = value_conv[1]
                                        course_data['Duration'] = duration
                                        course_data['Duration_Time'] = duration_time

                                        if duration == '1' or duration == '1.0':
                                            duration_time = 'Year'
                                            course_data['Duration_Time'] = duration_time
                                        elif 'month' in duration_time.__str__().lower():
                                            value_conv = DurationConverter.convert_duration(p_word)
                                            duration_time = 'Months'
                                            course_data['Duration'] = duration
                                            course_data['Duration_Time'] = duration_time

                                    else:
                                        course_data['Duration'] = "Not Provided"
                                        course_data['Duration_Time'] = ''

                            except IndexError:
                                course_data['Full_Time'] = ''
                                course_data['Part_Time'] = ''
                                course_data['Duration'] = ''
                                course_data['Duration_Time'] = ''
                                # print("this course doesn't have information pertaining to duration")

            except IndexError:
                course_data['Full_Time'] = ''
                course_data['Part_Time'] = ''
                course_data['Duration'] = ''
                course_data['Duration_Time'] = ''
                # print("this course doesn't have information pertaining to duration")

        # Description
        courseDescription = soup2.select("#overview > div > div > div:nth-child(1) > div > ul > li:nth-child(1)")
        if courseDescription:
            for ea in courseDescription:
                course_data['Description'] = ea.text.strip().replace("\n", " ")
        else:
            courseDescription = soup2.select(
                "body > div.u-main-wrapper__content > div.c-program-content.py-3 > div > div > div > ul > li")
            if courseDescription:
                for ea in courseDescription:
                    course_data['Description'] = ea.text.strip().replace("\n", " ")
            else:
                course_data['Description'] = ""

        # Career Outcome
        careerDetails = soup2.select("#career-outcomes > div > div > div > div > ul > li")
        if careerDetails:
            for each_career in careerDetails:
                course_data['Career_Outcomes/path'] = each_career.text.replace('\n', ' ')
        else:
            course_data['Career_Outcomes/path'] = "No career outcomes provided"

        # print(course_data['Course'], course_data['Career_Outcomes/path'], course_data['Website'])

        try:
            btn_international = soup2.select("body > div.u-main-wrapper__content > div.c-program-summary.p-4 > div > div:nth-child(1) > div > a:nth-child(2)")
            if btn_international:
                int_button = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/a[2]")
                if int_button:
                    int_button.click()
                    browser.current_url
                    courses_int = browser.page_source
                    soup3 = bs4.BeautifulSoup(courses_int, 'lxml')
                    time.sleep(5)
                    #browser.save_screenshot(course_data['Course'] + ".png")

                    course_data['Availability'] = "A"

                try:
                    Int_amount = soup3.select(
                        "#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > tbody > tr:contains('On-campus') > td:nth-child(2)")
                    if Int_amount:
                        for each_int in Int_amount:
                            Int_feeRaw = tag_text(each_int)
                            Int_fee = re.findall(currency_pattern, Int_feeRaw)[0]
                            if Int_fee:
                                course_data['Int_Fees'] = Int_fee.replace("AUD", "").strip()
                            else:
                                course_data['Int_Fees'] = ""
                    else:
                        Int_amounts = soup3.select(
                            "#fees-scholarships > div.c-program-content.pb-3 > div > div > div > table > tbody > tr:contains('External') > td:nth-child(2)")
                        if Int_amounts:
                            for each_ints in Int_amounts:
                                Int_fee_Raw = tag_text(each_ints)
                                Int_fees = re.findall(currency_pattern, Int_fee_Raw)[0]
                                if Int_fees:
                                    course_data['Int_Fees'] = Int_fees.replace("AUD", "").strip()
                                else:
                                    course_data['Int_Fees'] = ""
                        else:
                            course_data['Int_Fees'] = " "

                except IndexError:
                    course_data['Int_Fees'] = ""
            else:
                course_data['Availability'] = "D"
        except Exception:
            course_data['Availability'] = "D"

        #print(course_data['Availability'], course_data['Website'],course_data['Int_Fees'],course_data['Local_Fees'],actual_cities)
            
        for i in actual_cities:
            course_data['City'] = possible_cities[i.lower()]
            course_data_all.append(copy.deepcopy(course_data))
        del actual_cities

        #print(course_data['Int_Fees'], course_data['Duration'], course_data['Duration_Time'],
              #course_data['Career_Outcomes/path'], course_data['Website'])

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

ordered_file = csv_file_path.parent.__str__() + "/USQ_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
