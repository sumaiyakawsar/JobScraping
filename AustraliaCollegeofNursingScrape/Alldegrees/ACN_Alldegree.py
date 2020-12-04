"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 26-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import os
import re
import pandas as pd
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

course_data = {'Level_Code': '', 'University': 'Australian College of Nursing', 'City': '',
               'Course': '', 'Faculty': '',
               'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
               'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
               'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_1_grade_1': '',
               'Prerequisite_2_grade_2': '',
               'Website': '', 'Course_Lang': 'English', 'Availability': '', 'Description': '',
               'Career_Outcomes/path': '', 'Country': 'Australia',
               'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '', 'Remarks': '',
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
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': ''
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


def nm_unit_fee_r(amount):
    nm_unit_fee_raw = amount.text
    nm_unit_fee = re.search(currency_pattern, nm_unit_fee_raw)
    if nm_unit_fee:
        nm_unit_fees = nm_unit_fee.group()
    return nm_unit_fees.replace("$", "").strip()


def m_unit_fee_r(amount):
    unit_fee_raw = amount.text
    unit_fee = re.search(currency_pattern, unit_fee_raw)
    if unit_fee:
        unit_fees = unit_fee.group()
    return unit_fees.replace("$", "").strip()


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
    course_data = {'Level_Code': '', 'University': 'Australian College of Nursing', 'City': '',
                   'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_1_grade_1': '',
                   'Prerequisite_2_grade_2': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': '', 'Description': '',
                   'Career_Outcomes/path': '', 'Country': 'Australia',
                   'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '', 'Remarks': '',
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
                   'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': ''
                   }
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
        course_title = tag_text(course_name).strip().replace("HLT64115", "")
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

    # All_units
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

    all_unlist = []
    i = 1
    tab = soup.select(".tablepress .column-2 a")
    if tab:
        for ta in tab:
            all_units = ta['href']
            if all_units not in all_unlist:
                all_unlist.append(all_units)
    try:

        if i <= len(all_unlist):
            for to in all_unlist:
                browser.get(to)
                new_url = browser.page_source

                soup2 = bs4.BeautifulSoup(new_url, 'lxml')
                time.sleep(2)

                course_name = soup2.find("div", class_="uvc-sub-heading")
                course_data[f'Subject_or_Unit_{i}'] = course_name.text

                subject_objective = soup2.select(".vc_active .wpb_wrapper > p")
                for each_desc in subject_objective:
                    course_data[f'Subject_Objective_{i}'] = each_desc.text.replace("\n", "").strip()

                fee = soup2.select("tr:contains('Fee') td:nth-of-type(2)")
                for so in fee:
                    if so:
                        so_fee = so.text
                        table = soup2.find("table", class_="tablepress")
                        if "Tier 1" in so_fee:
                            non_member_amount = table.find(class_="row-2").find("td", class_="column-5")
                            member_amount = table.find(class_="row-2").find("td", class_="column-4")

                            non_member = nm_unit_fee_r(non_member_amount)
                            member = m_unit_fee_r(member_amount)
                        elif "Tier 2" in so_fee:
                            non_member_amount = table.find(class_="row-3").find("td", class_="column-5")
                            member_amount = table.find(class_="row-3").find("td", class_="column-4")

                            non_member = nm_unit_fee_r(non_member_amount)
                            member = m_unit_fee_r(member_amount)
                        elif "Tier 3" in so_fee:
                            non_member_amount = table.find(class_="row-4").find("td", class_="column-5")
                            member_amount = table.find(class_="row-4").find("td", class_="column-4")

                            non_member = nm_unit_fee_r(non_member_amount)
                            member = m_unit_fee_r(member_amount)
                        elif "Tier 4" in so_fee:
                            non_member_amount = table.find(class_="row-5").find("td", class_="column-5")
                            member_amount = table.find(class_="row-5").find("td", class_="column-4")

                            member = m_unit_fee_r(member_amount)
                            non_member = nm_unit_fee_r(non_member_amount)
                        course_data[
                            f'Subject_Description_{i}'] = f"Member fee = {member}\nNon-member fee = {non_member}"
                    else:
                        course_data[f'Subject_Description_{i}'] = ""

                print(i, course_data[f'Subject_or_Unit_{i}'], course_data[f'Subject_Description_{i}'])
                i = i + 1

        else:
            if "Graduate Certificate in Nursing (Bridging and Re-entry)" in course_data['Course']:
                subject_1 = soup.select(".standard-arrow p strong")
                for to in subject_1:
                    course_data[f'Subject_or_Unit_{i}'] = to.text
                    subject_desc = soup.select(".standard-arrow p:nth-of-type(2)")
                    for so in subject_desc:
                        course_data[f'Subject_Objective_{i}'] = so.text
                    i = i + 1

                course_data[f'Subject_Description_{i}'] = ""
            elif "Advanced Diploma of Nursing" in course_data['Course']:
                course_data[f'Subject_or_Unit_{i}'] = ""
                course_data[f'Subject_Objective_{i}'] = ""
                course_data[f'Subject_Description_{i}'] = ""

    except Exception:
        pass
    print(len(all_unlist), course_data['Website'])


    course_data_all.append(copy.deepcopy(course_data))

print(*course_data_all, sep='\n')

desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty',
                      'Int_Fees', 'Local_Fees', 'Currency', 'Currency_Time',
                      'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                      'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2',
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
                      'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30'
                      ]
# tabulate our data
df = pd.DataFrame(course_data_all, columns=desired_order_list)
df.to_csv(csv_file, index=False)

browser.quit()
