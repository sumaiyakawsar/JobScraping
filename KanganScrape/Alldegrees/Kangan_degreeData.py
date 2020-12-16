"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 24-11-20
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
option.add_argument('--no-sandbox')
option.add_argument("start-maximized")
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/kangan_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/kangan_all_courses.csv'

possible_cities = {'broadmeadows': 'Melbourne',
                   'docklands': 'Melbourne',
                   'richmond': 'Melbourne',
                   'essendon': 'Melbourne',
                   'workplace': 'Workplace',
                   'moorabbin': 'Melbourne',
                   'moonee ponds': 'Melbourne',
                   'craigieburn': 'Melbourne',
                   'melbourne': 'Melbourne',
                   'bendigo': 'Bendigo',
                   'online': 'Online'
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


def durationo(word):
    try:
        p_word = word.replace("day", "").replace("1 year, 6 months", "1.5 year")
        if p_word:
            if 'full-time' in p_word.lower():
                course_data['Full_Time'] = 'Yes'
            else:
                course_data['Full_Time'] = 'No'

            if 'part-time' in p_word.lower():
                course_data['Part_Time'] = 'Yes'
            else:
                course_data['Part_Time'] = 'No'

            if 'flexible' in p_word.lower():
                course_data['Part_Time'] = "Yes"
                course_data['Full_Time'] = "Yes"

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


index = 0
for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'Kangan Batman Institute', 'City': '', 'Course': '', 'Faculty': '',
                   'Non-Apprentice_Government_Subsidised_Fee': '', 'Non-Apprentice_Concession_Fees': '',
                   'Non-Apprentice_Full_Fees': '',
                   'Apprentice_Government_Subsidised_Fee': '', 'Apprentice_Concession_Fees': '',
                   'Apprentice_Full_Fees': '',
                   'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': '',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': '',
                   'Description': '', 'Career_Outcomes/path': '', 'Country': 'Australia',
                   'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '', 'Blended': '', 'Remarks': '',
                   'Course Delivery Mode': '', 'FREE TAFE': '',
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
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source
    index += 1
    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find("span", class_="h2_text")
    if course_name:
        course_title = tag_text(course_name)
        course_data['Course'] = course_title

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Description
    description = []
    course_desc = soup.select("#divtab1 p:nth-of-type(n+5)")
    if course_desc:
        for each_desc in course_desc:
            description.append(each_desc.text.replace("\n", "").strip())
        course_data['Description'] = ''.join(description)
    else:
        course_data['Description'] = "N/A"

    # Faculty
    faculty_col = soup.select_one("span#content_0_lbldepartment")
    if faculty_col:
        fac = faculty_col.text
        course_data['Faculty'] = fac
    else:
        course_data['Faculty'] = ""

    # Duration
    dura = soup.find("span", id="content_0_lblduration")
    if dura:
        p_word = dura.text
        durationo(p_word)

    # Fees
    gov_subsidised = soup.select("div.fees_div:nth-of-type(2) div.fees_div2")
    if gov_subsidised:
        for govt in gov_subsidised:
            raw_fee = govt.text.strip()
            gov_loc = re.match(currency_pattern, raw_fee)
            if gov_loc:
                govt_fee = gov_loc.group()
                course_data['Non-Apprentice_Government_Subsidised_Fee'] = govt_fee.replace("$", "").strip()

    concession_fee = soup.select("div.fees_div:nth-of-type(2) div.fees_div3")
    if concession_fee:
        for fee in concession_fee:
            fee_raw = fee.text.strip()
            conc_loc_fee = re.search(currency_pattern, fee_raw)
            if conc_loc_fee:
                concession_fe = conc_loc_fee.group()
                course_data['Non-Apprentice_Concession_Fees'] = concession_fe.replace("$", "").strip()

    full_money = soup.select("div.fees_div:nth-of-type(2) div.fees_div4")
    if full_money:
        for loc in full_money:
            local_fee_raw = loc.text.strip()
            loc_fee = re.search(currency_pattern, local_fee_raw)
            if loc_fee:
                local_fee = loc_fee.group()
                course_data['Non-Apprentice_Full_Fees'] = local_fee.replace("$", "").strip()

    a_gov_subsidised = soup.select("div.fees_div:nth-of-type(3) div.fees_div2")
    if a_gov_subsidised:
        for a_govt in a_gov_subsidised:
            raw_fee = a_govt.text.strip()
            gov_loc = re.search(currency_pattern, raw_fee)
            if gov_loc:
                govt_fee = gov_loc.group()
                course_data['Apprentice_Government_Subsidised_Fee'] = govt_fee.replace("$", "").strip()

    a_concession_fee = soup.select("div.fees_div:nth-of-type(3) div.fees_div3")
    if a_concession_fee:
        for fee in a_concession_fee:
            fee_raw = fee.text.strip()
            conc_loc_fee = re.search(currency_pattern, fee_raw)
            if conc_loc_fee:
                concession_fe = conc_loc_fee.group()
                course_data['Apprentice_Concession_Fees'] = concession_fe.replace("$", "").strip()

    a_full_money = soup.select("div.fees_div:nth-of-type(3) div.fees_div4")
    if a_full_money:
        for ap_loc in a_full_money:
            local_fee_raw = ap_loc.text.strip()
            loc_fee = re.search(currency_pattern, local_fee_raw)
            if loc_fee:
                local_fee = loc_fee.group()
                course_data['Apprentice_Full_Fees'] = local_fee.replace("$", "").strip()

    # FREE TAFE
    del_mode = soup.find("span", id="content_0_lblinterestarea")
    if del_mode:
        all_info = del_mode.text.lower().strip()
        if "free tafe" in all_info:
            course_data['FREE TAFE'] = "Yes"
        else:
            course_data['FREE TAFE'] = "No"
    else:
        course_data['FREE TAFE'] = "No"

    # LOCATION/CITY
    campus = soup.select("span#content_0_lblcampus")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])

    career_outcome = []
    # Career Outcomes#divtab5 p:nth-of-type(3), #divtab5 ul:nth-of-type(1) li
    overview = soup.select("#divtab5 p:nth-of-type(3), #divtab5 ul:nth-of-type(1) li")
    if overview:
        for ca in overview:
            career_outcome.append(ca.text.replace("\n", "").strip().replace("N/A", ""))

    course_data['Career_Outcomes/path'] = ' '.join(career_outcome)

    subjects = []
    nominal_hours = []
    course_table = soup.select("table.data")
    if course_table:
        for each_table in course_table:
            course_row = each_table.select("tr:nth-of-type(n+2)")
            for row in course_row:
                subject_code = row.select("td:nth-of-type(1)")
                subject_name = row.select("td:nth-of-type(2)")
                nomin = row.select("td:nth-of-type(3)")
                for sub_cod in subject_code:
                    for sub_nam in subject_name:
                        for no in nomin:
                            subject = sub_cod.text + " " + sub_nam.text.replace(sub_cod.text, "").strip().replace("()",
                                                                                                                  "")
                            subjects.append(subject)
                            nominal = "Nominal Hours = " + no.text
                            nominal_hours.append(nominal)
    i = 1
    for subs in subjects:
        course_data[f'Subject_or_Unit_{i}'] = subs
        i += 1
        if i == 41:
            break
    h = 1
    for hour in nominal_hours:
        course_data[f'Subject_Objective_{h}'] = hour
        h += 1
        if h == 41:
            break

    if 'Online' in actual_cities:
        course_data['Online'] = "Yes"
    else:
        course_data['Online'] = "No"

    if 'Melbourne' in actual_cities or 'Workplace' in actual_cities or 'Bendigo' in actual_cities:
        course_data['Offline'] = "Yes"
    else:
        course_data['Offline'] = "No"

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

    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

print(*course_data_all, sep='\n')

desired_order_list = ['Level_Code','University','City','Course','Faculty',
                      'Non-Apprentice_Government_Subsidised_Fee','Non-Apprentice_Concession_Fees',
                      'Non-Apprentice_Full_Fees',
                      'Apprentice_Government_Subsidised_Fee','Apprentice_Concession_Fees',
                      'Apprentice_Full_Fees',
                      'Currency','Currency_Time','Duration','Duration_Time','Full_Time','Part_Time',
                      'Prerequisite_1','Prerequisite_2','Prerequisite_3',
                      'Prerequisite_1_grade_1','Prerequisite_2_grade_2','Prerequisite_3_grade_3',
                      'Website','Course_Lang','Availability','Description','Career_Outcomes/path',
                      'Country','Online','Offline','Distance','Face_to_Face','Blended','Remarks',
                      'Course Delivery Mode','FREE TAFE',
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
                      'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40'
                      ]
# tabulate our data
df = pd.DataFrame(course_data_all, columns=desired_order_list)
df.to_csv(csv_file, index=False)

browser.quit()
