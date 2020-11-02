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
course_links_file_path = course_links_file_path.__str__() + '/LaTrobe_UG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/LaTrobe_UG_unordered.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hide"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


course_data = {'Level_Code': '',
               'University': 'La Trobe University',
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
               'Prerequisite_2_grade_2': '6.0',
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

possible_cities = {'melbourne': 'Melbourne',
                   'shepparton': 'Shepparton',
                   'mildura': 'Mildura',
                   'bendigo': 'Bendigo',
                   'albury wodongay': 'Albury Wodongay',
                   'other': 'Other',
                   'city':'City'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

for each_url in course_links_file:
    browser.get(each_url)
    each_url = browser.page_source
    soup = bs4.BeautifulSoup(each_url, 'lxml')

    # if the popup shows up force click international for international data
    if soup.find("div", id="popup"):
        browser.find_element_by_xpath("/html/body/div[1]/div/ul/li[2]/button").click()
        browser.implicitly_wait(3)
        continue

    time.sleep(0.5)

    clean_tags(soup)

    faculty_info = soup.select(".breadcrumbs a:nth-of-type(3)")
    for each_fac in faculty_info:
        course_data['Faculty'] = each_fac.text.strip()

    courses_details = soup.findAll("article", class_="UG")
    for ea in courses_details:
        allsites = []
        actual_cities = []
        course_tag = ea.find("a")
        course_data['Course'] = course_tag.text
        course_website = course_tag.get('href')
        course_data['Website'] = course_website
        allsites.append(course_website)

        # DECIDE THE LEVEL CODE
        for i in level_key:
            for j in level_key[i]:
                if j in course_data['Course']:
                    course_data['Level_Code'] = i
        # print(course_data['Course'], course_data['Website'])
        # city atar
        cities = ea.find_all("span", class_="atar")
        if cities:
            for each_city in cities:
                temp_line = each_city.text.lower()
                for i in possible_cities:
                    if i in temp_line:
                        actual_cities.append(possible_cities[i])
                        if has_numbers(temp_line):
                            atar = re.findall(r'\d+\.*\d*', temp_line)[0]
                            course_data['Prerequisite_1_grade_1'] = atar
                        else:
                            course_data['Prerequisite_1_grade_1'] = " "

        # print(course_data['Course'],course_data['Website'])
        for courses in allsites:
            browser.get(courses)
            courses = browser.page_source

            soup2 = bs4.BeautifulSoup(courses, 'lxml')
            time.sleep(10)

            # international_fees
            try:
                moneyColumn = soup2.select("#fees > p:nth-child(3)")
                if moneyColumn:
                    for ea in moneyColumn:
                        int_feeRaw = tag_text(ea)
                        int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                        if int_fee:
                            course_data['Int_Fees'] = int_fee.replace(" ", "")
                        else:
                            course_data['Int_Fees'] = "Cudnt find yet"
                else:
                    moneyColumn = soup2.select("#overview > div.mock-table > div:nth-child(4) > div:nth-child(2)")
                    if moneyColumn:
                        for ea in moneyColumn:
                            int_feeRaw = tag_text(ea)
                            int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                            if int_fee:
                                course_data['Int_Fees'] = int_fee.replace(" ", "")
                            else:
                                course_data['Int_Fees'] = "Where is it"
                    else:
                        moneyColumn = soup2.select("div:nth-of-type(4) div.mock-table-cell:nth-of-type(2)")
                        if moneyColumn:
                            for ea in moneyColumn:
                                int_feeRaw = tag_text(ea)
                                int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                                if int_fee:
                                    course_data['Int_Fees'] = int_fee.replace(" ", "")
                                else:
                                    course_data['Int_Fees'] = "Where is it"
                        else:
                            another_Statement = soup2.select("#overview > h2")
                            if another_Statement:
                                for er in another_Statement:
                                    if "not available for International Students" in er.text:
                                        browser.find_element_by_xpath(
                                            "/html/body/div[2]/main/section/div/div/p/select[2]/option[2]").click()
                                        time.sleep(10)
                                        continue
                                    moneyColumn2 = soup2.select(
                                        "#overview > div.mock-table > div:nth-child(4) > div:nth-child(2)")
                                    if moneyColumn2:
                                        for ea in moneyColumn2:
                                            int_feeRaw2 = tag_text(ea)
                                            int_fee2 = re.findall(currency_pattern, int_feeRaw2)[0]
                                            if int_fee2:
                                                course_data['Int_Fees'] = int_fee2.replace(" ", "")
                                    else:
                                        course_data['Int_Fees'] = "Not Provided"
                            else:
                                course_data['Int_Fees'] = "Not Provided"
            except IndexError:
                course_data['Int_Fees'] = ""
                # local fees

            # Description Check again
            courseDescription = soup2.select("#overview > div:nth-child(4)")
            if courseDescription:
                for ea in courseDescription:
                    course_data['Description'] = ea.text.strip().replace("/n", " ")
            else:
                course_data['Description'] = "Hi cant find you"

            # Duration/Duration Time/FullTime/Parttime/
            course_detail = soup2.select("#overview > div.mock-table > div:nth-child(3) > div:nth-child(2)")
            for ra in course_detail:
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
                        if 'part time' in p_word.lower() or 'part' in p_word.lower() and 'full time' in p_word.lower():
                            course_data['Blended'] = 'Yes'
                            course_data['Full_Time'] = 'Yes'
                            course_data['Part_Time'] = 'Yes'
                        else:
                            course_data['Blended'] = 'No'

                        if 'year' in p_word.__str__().lower():
                            value_conv = DurationConverter.convert_duration(p_word)
                            duration = float(''.join(filter(str.isdigit, str(value_conv)))[0])
                            duration_time = 'Years'
                            course_data['Duration'] = duration
                            course_data['Duration_Time'] = duration_time

                            if str(duration) == '0.5':
                                duration_time = 'Months'
                                course_data['Duration'] = '6'
                                course_data['Duration_Time'] = duration_time
                            elif str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
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

                        else:
                            course_data['Duration'] = " Cant find"
                except IndexError:
                    course_data['Full_Time'] = ''
                    course_data['Part_Time'] = ''
                    course_data['Duration'] = ''
                    course_data['Duration_Time'] = ''
                    # print("this course doesn't have information pertaining to duration")
            # Career Outcome
            careerDetails = soup2.select("#career-outcomes > ul")
            if careerDetails:
                for each_career in careerDetails:
                    course_data['Career_Outcomes/path'] = each_career.text.replace('\n', ' ')
            else:
                careerDetails = soup2.select("#career-outcomes p:nth-of-type(2)")
                if careerDetails:
                    for each_career in careerDetails:
                        course_data['Career_Outcomes/path'] = each_career.text.replace('\n', ' ')
                else:
                    careerDetails = soup2.select("#career-outcomes strong")
                    if careerDetails:
                        for each_career in careerDetails:
                            course_data['Career_Outcomes/path'] = each_career.text.replace('\n', ' ')
                    else:
                        course_data['Career_Outcomes/path'] = "No career outcomes provided"

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

        print(course_data['Int_Fees'], course_data['Duration'], course_data['Duration_Time'],
              course_data['Career_Outcomes/path'], course_data['Website'])

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

ordered_file = csv_file_path.parent.__str__() + "/LaTrobe_UG_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
