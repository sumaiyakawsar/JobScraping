"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 17-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import pandas as pd
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
course_links_file_path = course_links_file_path.__str__() + '/holmesglen_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/Holmesglen_all_courses.csv'


possible_cities = {'st kilda': 'Melbourne',
                   'chadstone': 'Melbourne',
                   'glen waverley': 'Melbourne',
                   'workplace': 'Workplace',
                   'moorabbin': 'Melbourne',
                   'melbourne': 'Melbourne',
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


def local_money_r(loc_money):
    for loc in loc_money:
        local_fee_raw = loc.text
        loc_fee = re.search(currency_pattern, local_fee_raw)
        if loc_fee:
            local_fee = loc_fee.group()
            course_data['Local_Fees'] = local_fee.replace("$", "").strip()


def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text
        Int_fee = re.search(currency_pattern, int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            course_data['Int_Fees'] = int_fee.replace("$", "").strip()


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
                if str(duration) == '1' or str(duration) == '1.0':
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Month'
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
                course_data['Duration_Time'] = value_conv[1]
                if str(duration) == '1' or str(duration) == '1.0':
                    course_data['Duration'] = duration
                    course_data['Duration_Time'] = 'Day'
            elif 'hour' in p_word.__str__().lower():
                value_conv = DurationConverter.convert_duration(p_word)
                duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
                course_data['Duration'] = duration
                course_data['Duration_Time'] = value_conv[1]
            else:
                course_data['Duration'] = p_word
                course_data['Duration_Time'] = ''
        else:
            course_data['Duration'] = p_word
            course_data['Duration_Time'] = ''

    except Exception:
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''


index = 0
for each_url in course_links_file:
    index += 1
    course_data = {'Level_Code': '', 'University': 'Holmesglen Institute', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': '',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English',
                   'Availability': '', 'Description': '', 'Career_Outcomes/path': '', 'Country': 'Australia',
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

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(0.3)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find("h1")
    if course_name:
        all_info = course_name.text.replace("\n", "").strip()

        # CourseDeliveryMode (Apprenticeships|Traineeships|Normal)
        if "Pre-apprenticeship" in all_info:
            course_data['Course Delivery Mode'] = "Pre-apprenticeship"
        elif "Apprenticeship" in all_info:
            course_data['Course Delivery Mode'] = "Apprenticeship"
        elif "Traineeship" in all_info or "VET" in all_info:
            course_data['Course Delivery Mode'] = "Traineeship"
        else:
            course_data['Course Delivery Mode'] = "Normal"

        clean_tags(course_name)
        course_title = tag_text(course_name)
        course_data['Course'] = course_title

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # Description
    description_course = []
    course_desc = soup.select(".courseDetailPage-secSubtitle")
    course_desc2 = soup.select("#overview p:nth-of-type(n+4)")
    if course_desc:
        for each_desc in course_desc:
            describe = each_desc.text.strip()
            description_course.append(describe)

    if course_desc2:
        for each_desc in course_desc2:
            describe = each_desc.text.strip()
            description_course.append(describe)

    course_data['Description'] = ''.join(description_course)

    # Faculty
    faculty_col = soup.select_one("a:nth-of-type(2) span[itemprop='title']")
    if faculty_col:
        fac = faculty_col.text.replace("1 evening per week", "")
        course_data['Faculty'] = fac
    else:
        course_data['Faculty'] = ""

    # Duration
    dura = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblLocalDuration")
    dura2 = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl00_PageHeader_lblLocalDuration")
    if dura:
        for to in dura:
            p_word = to.text.replace("3 days a week", "").replace("1 evening per week, over", ""). \
                replace("five four-hour", '5 days').replace("five 4-hour", '5 days').replace("two 4-hour", '2 days')
            durationo(p_word)
    elif dura2:
        for to in dura2:
            p_word = to.text.replace("20 hours per week ", "")
            durationo(p_word)

    # LOCATION/CITY
    campus = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblLocalCampus")
    campus2 = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl00_PageHeader_lblLocalCampus")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    elif campus2:
        for campi in campus2:
            campur = campi.text.lower()
            for i in possible_cities:
                if i in campur:
                    actual_cities.append(possible_cities[i])

    # Local fee
    money = soup.select("tr:contains('Full Fee') td:nth-of-type(2)")
    money2 = soup.select("tr:contains('Gov. subsidised Apprenticeship') td:nth-of-type(2)")
    money3 = soup.select("tr:contains('Government subsidised') td:nth-of-type(2)")
    if money:
        local_money_r(money)

    elif money2:
        local_money_r(money2)

    elif money3:
        local_money_r(money3)

    else:
        course_data['Local_Fees'] = ""

    #Free Tafe
    del_mode = soup.select("tr:contains('Free TAFE eligible student') td:nth-of-type(2)")
    if del_mode:
        for ea in del_mode:
            all_info = ea.text.strip()
            # FREE TAFE
            if "FREE" in all_info:
                course_data['FREE TAFE'] = "Yes"
            else:
                course_data['FREE TAFE'] = "No"
    else:
        course_data['FREE TAFE'] = "No"

    # Career Outcomes
    career_outcome = []
    overview = soup.find("section", id="overview")
    if overview:
        career = overview.find("ul")
        if career:
            car = career.find_all("li")
            for each_career in car:
                career_outcome.append(each_career.text.strip())
    course_data['Career_Outcomes/path'] = ', '.join(career_outcome)

    # International data
    try:
        if browser.find_element_by_xpath('//*[@id="p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_courseIntlLink"]'):
            browser.find_element_by_xpath(
                '//*[@id="p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_courseIntlLink"]').click()
            time.sleep(1)
            int_uurl = browser.current_url
            if "/international" in int_uurl:
                browser.get(int_uurl)
                int_url = browser.page_source
                soup2 = bs4.BeautifulSoup(int_url, 'lxml')
                course_data['Availability'] = "A"

                # IELTS
                iel = soup2.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblIntlEntryRequirement")
                for ie in iel:
                    ielts_amount = ie.text.strip()
                    if has_numbers(ielts_amount):
                        ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                        course_data['Prerequisite_2_grade_2'] = ielts

                # Int_fees
                int_money = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblIntlFees")
                if money:
                    int_money_r(int_money)

            else:
                course_data['Availability'] = "D"
                course_data['Prerequisite_2_grade_2'] = ""
                course_data['Int_Fees'] = ""

    except Exception:
        course_data['Availability'] = "D"

    # Online/Offline/Blended etc
    if 'Online' in actual_cities:
        course_data['Online'] = "Yes"
    elif 'Online' not in actual_cities:
        course_data['Online'] = "No"

    if 'Melbourne' in actual_cities or 'Workplace' in actual_cities:
        course_data['Offline'] = "Yes"
    elif 'Melbourne' not in actual_cities or 'Workplace' not in actual_cities:
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

    # Subjects
    subject_unit = []
    subject_table = soup.select_one(".accordionItem-content")
    if subject_table:
        subject_rows = subject_table.select("tbody tr")
        for to in subject_rows:
            subject_code = to.select("td:nth-of-type(1)")
            subject_ = to.select("td:nth-of-type(2)")

            for subs_code in subject_code:
                for each_subject_ in subject_:
                    subject_detail = subs_code.text.strip() + " " + each_subject_.text.strip()

                    if subject_detail not in subject_unit:
                        subject_unit.append(subject_detail)
                    else:
                        del subject_detail
    i = 1
    for each_subject in subject_unit:
        course_data[f'Subject_or_Unit_{i}'] = each_subject
        i += 1
        if i == 41:
            break

    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

print(*course_data_all, sep='\n')
desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty',
                      'Int_Fees', 'Local_Fees', 'Currency', 'Currency_Time',
                      'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                      'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2',
                      'Website', 'Course_Lang', 'Availability', 'Description', 'Career_Outcomes/path', 'Country',
                      'Online', 'Offline', 'Distance', 'Face_to_Face', 'Blended', 'Remarks',
                      'Course Delivery Mode', 'FREE TAFE',
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
