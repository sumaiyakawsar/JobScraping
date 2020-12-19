"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import os
import re
import time
import pandas as pd
from pathlib import Path

import DurationConverter
import TemplateData
import bs4 as bs4
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("headless")
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
csv_file = csv_file_path.parent.__str__() + '/LaTrobe_UG_Data.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hide"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


possible_cities = {'melbourne': 'Melbourne',
                   'shepparton': 'Shepparton',
                   'mildura': 'Mildura',
                   'bendigo': 'Bendigo',
                   'albury-wodonga': 'Albury Wodongay',
                   'albury wodongay': 'Albury Wodongay',
                   'sydney': 'Sydney',
                   'other': 'Other',
                   'city': 'City'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels
index = 0
for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'La Trobe University', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': 'Equivalent AQF level',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '6.0', 'Prerequisite_3_grade_3': 'Year 12',
                   'Website': '', 'Course_Lang': 'English', 'Availability': '', 'Description': '',
                   'Career_Outcomes/path': '', 'Country': 'Australia',
                   'Online': 'Yes', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '',
                   'Remarks': '',
                   'Subject_or_Unit_1': '', 'Subject_Objective_1': '', 'Subject_Description_1': '',
                   'Subject_or_Unit_2': '', 'Subject_Objective_2': '', 'Subject_Description_2': '',
                   'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
                   'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
                   'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
                   'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
                   'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
                   'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
                   'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
                   'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
                   'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
                   'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
                   'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
                   'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
                   'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
                   'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
                   'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
                   'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
                   'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
                   'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
                   'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
                   'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
                   'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
                   'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
                   'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
                   'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
                   'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
                   'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
                   'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
                   'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
                   'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
                   'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
                   'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
                   'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
                   'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
                   'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
                   'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
                   'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
                   'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
                   'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''

                   }
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

    courses_details = soup.select("article.UG.I")
    for ea in courses_details:
        all_sites = []
        actual_cities = []

        # Course Name
        course_tag = ea.find("a")
        course_data['Course'] = course_tag.text
        course_level = course_tag.text

        # Course Website
        course_website = course_tag['href']
        course_data['Website'] = course_website
        if course_website not in all_sites:
            all_sites.append(course_website)

        if 'bachelor' in course_level.lower() and 'honours' in course_level.lower():
            course_level = "Bachelor honours"

        # DECIDE THE LEVEL CODE
        for i in level_key:
            for j in level_key[i]:
                if j in course_level:
                    course_data['Level_Code'] = i

        # city atar
        cities = ea.select(".UG.D.I p.course-list-atar")
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

        for courses in all_sites:
            index += 1
            browser.get(courses)
            courses = browser.page_source

            soup2 = bs4.BeautifulSoup(courses, 'lxml')
            time.sleep(0.4)
            try:
                another_Statement = soup2.select("#overview > h2")
                if another_Statement:
                    for er in another_Statement:
                        if "not available" in er.text.lower() or "oops, something went wrong" in er.text:
                            button3 = browser.find_element_by_xpath(
                                "/html/body/div[2]/main/section/div/div/p/select[2]/option[3]")
                            button2 = browser.find_element_by_xpath(
                                "/html/body/div[2]/main/section/div/div/p/select[2]/option[2]")
                            if button3:
                                button3.click()
                                browser.implicitly_wait(3)
                                continue
                            elif button2:
                                button2.click()
                                browser.implicitly_wait(3)
                                continue
            except Exception:
                pass

            # international_fees
            try:
                moneyColumn1 = soup2.select("#fees > p:nth-child(3)")
                moneyColumn2 = soup2.select("#overview > div.mock-table > div:nth-child(4) > div:nth-child(2)")
                moneyColumn3 = soup2.select("div:nth-of-type(4) div.mock-table-cell:nth-of-type(2)")
                moneyColumn4 = soup2.select("div.mock-table-row:nth-of-type(3) div:nth-of-type(2)")
                if moneyColumn1:
                    for ea in moneyColumn1:
                        int_feeRaw = tag_text(ea)
                        int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                        if int_fee:
                            course_data['Int_Fees'] = int_fee.replace(" ", "").replace("A$", "")

                elif moneyColumn2:
                    for ea in moneyColumn2:
                        int_feeRaw = tag_text(ea)
                        int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                        if int_fee:
                            course_data['Int_Fees'] = int_fee.replace(" ", "").replace("A$", "")

                elif moneyColumn3:
                    for ea in moneyColumn3:
                        int_feeRaw = tag_text(ea)
                        int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                        if int_fee:
                            course_data['Int_Fees'] = int_fee.replace(" ", "").replace("A$", "")
                elif moneyColumn4:
                    for ea in moneyColumn4:
                        int_feeRaw = tag_text(ea)
                        int_fee = re.findall(currency_pattern, int_feeRaw)[0]
                        if int_fee:
                            course_data['Int_Fees'] = int_fee.replace(" ", "").replace("A$", "")

                elif another_Statement:
                    for er in another_Statement:
                        if "not available for International Students" in er.text or "oops, something went wrong" in er.text:
                            browser.find_element_by_xpath(
                                "/html/body/div[2]/main/section/div/div/p/select[2]/option[2]").click()
                            time.sleep(10)
                            continue

                        if moneyColumn2:
                            for ea in moneyColumn2:
                                int_feeRaw2 = tag_text(ea)
                                int_fee2 = re.findall(currency_pattern, int_feeRaw2)[0]
                                if int_fee2:
                                    course_data['Int_Fees'] = int_fee2.replace(" ", "").replace("A$", "")


            except IndexError:
                course_data['Int_Fees'] = ""

            # Description Check again
            description_list = []
            courseDescription = soup2.select("#overview > div:nth-child(4)")
            courseDescription2 = soup2.select_one("#overview > div:nth-of-type(3)")

            if courseDescription2:
                description_list.append(courseDescription2.text.strip().replace("\n", " "))

            elif another_Statement:
                for er in another_Statement:
                    if "not available for international students" in er.text.lower():
                        button3 = browser.find_element_by_xpath(
                            "/html/body/div[2]/main/section/div/div/p/select[2]/option[2]").click()
                        time.sleep(2)
                        continue

                    if courseDescription2:
                        for ea in courseDescription2:
                            description_list.append(ea.text.strip().replace("\n", ""))

            course_data['Description'] = ''.join(description_list)

            # Duration/Duration Time/FullTime/Part-time/
            course_detail = soup2.select("#overview > div.mock-table > div:nth-child(3) > div:nth-child(2)")
            if course_detail:
                for ra in course_detail:
                    p_word = ra.text
                    try:
                        if p_word:
                            if 'full-time' in p_word.lower():
                                course_data['Full_Time'] = 'Yes'
                            else:
                                course_data['Full_Time'] = 'No'

                            if 'part-time' in p_word.lower():
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
                                course_data['Duration'] = ''
                                course_data['Duration_Time'] = ""
                    except Exception:
                        course_data['Duration'] = ''
                        course_data['Duration_Time'] = ''

            # Career Outcome
            careerDetails = soup2.select("#career-outcomes > ul > li")
            careerDetails2 = soup2.select("#career-outcomes p:nth-of-type(2)")
            careerDetails3 = soup2.select("#career-outcomes strong")
            career = []
            if careerDetails:
                for each_career in careerDetails:
                    career.append(each_career.text)
            elif careerDetails2:
                for each_career in careerDetails2:
                    career.append(each_career.text)
            elif careerDetails3:
                for each_career in careerDetails3:
                    career.append(each_career.text)
            course_data['Career_Outcomes/path'] = ', '.join(career)

            # Subjects
            subjects = []
            course_structure = soup2.select_one("div.course-structure-content")
            if course_structure:
                subject_header = course_structure.select("table a")
                for each in subject_header:
                    main_link = 'https://www.latrobe.edu.au'
                    sub_links = each['href']
                    if 'https://www.latrobe.edu.au/' not in sub_links:
                        sub_links = main_link + sub_links
                    if sub_links not in subjects:
                        subjects.append(sub_links)

            i = 1
            try:
                for each_link in subjects:
                    browser.get(each_link)
                    each_link = browser.page_source

                    soup3 = bs4.BeautifulSoup(each_link, 'lxml')
                    time.sleep(4)

                    subject_name = soup3.find("h1")
                    if subject_name:
                        course_data[f'Subject_or_Unit_{i}'] = subject_name.text

                    subject_description = soup3.select(".accordion-contrast > div > p:nth-of-type(2)")
                    if subject_description:
                        for ea in subject_description:
                            course_data[f'Subject_Objective_{i}'] = ea.text

                    i += 1
            except Exception:
                pass

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

        if "Yes" in course_data['Offline'] and "Yes" in course_data['Online']:
            course_data['Blended'] = "Yes"
        else:
            course_data['Blended'] = "No"

        for i in actual_cities:
            course_data['City'] = possible_cities[i.lower()]
            course_data_all.append(copy.deepcopy(course_data))
        del actual_cities


print(*course_data_all, sep='\n')

desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty',
                      'Int_Fees', 'Local_Fees', 'Currency', 'Currency_Time',
                      'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                      'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3',
                      'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2', 'Prerequisite_3_grade_3',
                      'Website', 'Course_Lang', 'Availability', 'Description', 'Career_Outcomes/path', 'Country',
                      'Online', 'Offline', 'Distance', 'Face_to_Face', 'Blended', 'Remarks',
                      'Subject_or_Unit_1', 'Subject_Objective_1', 'Subject_Description_1',
                      'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                      'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                      'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                      'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                      'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                      'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                      'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                      'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                      'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                      'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                      'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                      'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                      'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                      'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                      'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                      'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                      'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                      'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                      'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                      'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                      'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                      'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                      'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                      'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                      'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                      'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                      'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                      'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                      'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                      'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                      'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                      'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                      'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                      'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                      'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                      'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                      'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                      'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                      'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']
# tabulate our data
df = pd.DataFrame(course_data_all, columns=desired_order_list)
df.to_csv(csv_file, index=False)

browser.quit()
