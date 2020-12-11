"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 17-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import os
import re
import time
from pathlib import Path
import pandas as pd
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
course_links_file_path = course_links_file_path.__str__() + '/chisholm_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/chisholm_all_degrees.csv'

possible_cities = {'frankston': 'Melbourne',
                   'dandenong': 'Melbourne',
                   'berwick': 'Melbourne',
                   'workplace': 'Workplace',
                   'mornington peninsula': 'Melbourne',
                   'bass coast': 'Melbourne',
                   'traralgon': 'Melbourne',
                   'chisholm': 'Melbourne',
                   'melbourne': 'Melbourne'
                   }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("span"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.replace("\n", "").replace("About the course", "").strip()


def local_money_r(loc_money):
    for loc in loc_money:
        local_fee_raw = loc.text.strip()
        loc_fee = re.search(currency_pattern, local_fee_raw)
        if loc_fee:
            local_fee = loc_fee.group()
            money = local_fee.replace("$", "").replace(",","").strip()
            course_data['Local_Fees'] = float(money)
        else:
            course_data['Local_Fees'] = "N/A"


def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text.replace(" ", "").strip()
        Int_fee = re.search(currency_pattern, int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            money = int_fee.replace("$", "").replace(",","").strip()
            course_data['Int_Fees'] = float(money)
        else:
            course_data['Int_Fees'] = "N/A"


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


def iels(ielts):
    for ie in ielts:
        ielts_amount = ie.text.strip().replace("Year 11", ""). \
            replace("Year 12 ", ""). \
            replace("FNS40615", "").replace("FNS40215", "").replace("FNSSS00014", "").strip()
        if has_numbers(ielts_amount):
            ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
            if ielts:
                course_data['Prerequisite_2_grade_2'] = ielts
            else:
                course_data['Prerequisite_2_grade_2'] = "Nol"
        else:
            course_data['Prerequisite_2_grade_2'] = "N/A"


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'Chisholm Institute', 'City': '', 'Course': '', 'Faculty': '',
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
    time.sleep(1)

    # Course-Website
    course_data['Website'] = pure_url

    # Course-name
    course_name = soup.find("h1")
    if course_name:
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
    else:
        course_data['Course'] = ""

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j.lower() in course_data['Website']:
                course_data['Level_Code'] = i

    # CourseDeliveryMode (Apprenticeships|Traineeships|Normal)
    info = soup.find(class_="coursecode")
    if info:
        all_info = info.text.strip()
        if "Preapprenticeship" in all_info:
            course_data['Course Delivery Mode'] = "Pre-apprenticeship"
        elif "Apprenticeship" in all_info:
            course_data['Course Delivery Mode'] = "Apprenticeship"
        elif "Traineeship" in all_info or "VET" in all_info or 'traineeship' in course_data['Website']:
            course_data['Course Delivery Mode'] = "Traineeship"
        else:
            course_data['Course Delivery Mode'] = "Normal"

    # Description
    course_desc = soup.select(".paragraph-print-content")
    if course_desc:
        description(course_desc)
    else:
        course_data['Description'] = "N/A"

    # Duration
    dura = soup.select("dt:contains('Length') + dd")
    if dura:
        for to in dura:
            p_word = to.text
            durationo(p_word)
    else:
        course_data['Duration'] = "Find"
        course_data['Duration_Time'] = "flow"

    # Availability
    availability = soup.select("dt:contains('International') + dd")
    if availability:
        for st in availability:
            sto = st.text.lower()
            if "not available for international students" in sto:
                course_data['Availability'] = "D"
            elif "go to international students page" in sto:
                course_data['Availability'] = "A"
            elif "apply now" in sto:
                course_data['Availability'] = "I"
    else:
        pass

    # Online
    online = soup.select("dt:contains('Online') + dd")
    if online:
        for on in online:
            onl = on.text.lower()
            if "not available online" in onl:
                course_data['Online'] = "No"
                course_data['Offline'] = "Yes"
            elif 'applications open' in onl or 'go to online page' in onl:
                course_data['Online'] = "Yes"
    else:
        course_data['Online'] = "No"

    # Cities
    campus = soup.find("dd", class_="campuslist")
    if campus:
        campu = campus.text.lower()
        for i in possible_cities:
            if i in campu:
                actual_cities.append(possible_cities[i])
    else:
        pass

    if "D" in course_data['Availability'] or "A" in course_data['Availability']:
        money = soup.select("#fees > table > tbody > tr.totals > td[colspan]")
        money2 = soup.select("#fees > table > tbody > tr:nth-child(6) > td:nth-child(4)")
        money3 = soup.select("#fees")
        if money:
            local_money_r(money)
            for mo in money:
                mon = mo.text
                if "N/A" in mon:
                    money4 = soup.select("#fees > table > tbody > tr.totals > td:nth-child(3)")
                    local_money_r(money4)
        elif money2:
            local_money_r(money2)
        elif money3:
            local_money_r(money3)
        else:
            course_data['Local_Fees'] = "N/A"
    elif "I" in course_data['Availability']:
        int_money = soup.select("#fees")
        if int_money:
            int_money_r(int_money)
        else:
            course_data['Int_Fees'] = "/"

    if "D" in course_data['Availability']:
        course_data['Int_Fees'] = "N/A"
        course_data['Prerequisite_2_grade_2'] = "N/A"
    elif "I" in course_data['Availability']:
        course_data['Local_Fees'] = "N/A"
        # IELTS
        iel = soup.select("#prerequisites > p")
        if iel:
            iels(iel)
        else:
            course_data['Prerequisite_2_grade_2'] = "N/A"
    elif "A" in course_data['Availability']:
        try:
            if browser.find_element_by_xpath('//*[@id="content"]/div[2]/section[1]/section[1]/dl/dd[4]'):
                browser.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/section[1]/section[1]/dl/dd[4]').click()
                time.sleep(1)
                int_uurl = browser.current_url
                if "/international" in int_uurl:
                    browser.get(int_uurl)
                    int_url = browser.page_source
                    soup2 = bs4.BeautifulSoup(int_url, 'lxml')

                    # IELTS
                    iel = soup2.select("#prerequisites > p")
                    if iel:
                        iels(iel)
                    else:
                        course_data['Prerequisite_2_grade_2'] = "N/A2"

                    # Int_fees
                    inter_money = soup2.select("div#fees")
                    if inter_money:
                        int_money_r(inter_money)
                    else:
                        course_data['Int_Fees'] = "No int"


            else:
                course_data['Prerequisite_2_grade_2'] = "N/A"
                course_data['Int_Fees'] = "NoIntFee3"
        except Exception:
            pass

    # Free_TAFE
    free_tafe = soup.find("p", class_="alert__content")
    if free_tafe:
        all_info = free_tafe.text.lower().strip()
        # FREE TAFE
        if "free" in all_info:
            course_data['FREE TAFE'] = "Yes"
        else:
            course_data['FREE TAFE'] = "No"
    else:
        course_data['FREE TAFE'] = "No"

    if "Yes" in course_data['FREE TAFE']:
        course_data['Local_Fees'] = "0"

    # Career Outcomes
    overview = soup.find("div", id="career-pathways")
    professions = []
    if overview:
        career = overview.find_all("li", class_="no-border")
        for car in career:
            prof = car.text.strip()
            professions.append(prof)
            course_data['Career_Outcomes/path'] = ', '.join(professions).strip()
    else:
        course_data['Career_Outcomes/path'] = "N/A"

    course_subjects = []

    course_subject = soup.find(id="study-units")
    if course_subject:
        unit = course_subject.select("td:nth-of-type(1)")
        unit_desc = course_subject.select("td:nth-of-type(2)")

        i = 1
        for so in unit:
            course_subjects.append(so.text)
            course_data[f'Subject_or_Unit_{i}'] = so.text.replace("\n", "").strip()
            i = i + 1

        t = 1
        for to in unit_desc:
            course_data[f'Subject_Objective_{t}'] = to.text.strip()
            t = t + 1

    if actual_cities is not None:
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

desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty',
                      'Int_Fees', 'Local_Fees', 'Currency', 'Currency_Time',
                      'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                      'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3',
                      'Prerequisite_1_grade_1', 'Prerequisite_2_grade_2', 'Prerequisite_3_grade_3',
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
