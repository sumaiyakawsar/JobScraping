"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 17-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/holmesglen_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/Holmesglen_unordered.csv'

course_data = {'Level_Code': '',
               'University': 'Holmesglen Institute',
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
               'Blended': 'Yes',
               'Remarks': '',
               'Course Delivery Mode': '',
               'FREE TAFE': ''
               }

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


def description(course_description):
    for each_desc in course_description:
        course_data['Description'] = each_desc.text.replace("\n", "").replace("About the course", "").strip()


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


for each_url in course_links_file:
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
        # print(course_name.text.replace("\n","").strip())
        all_info = course_name.text.replace("\n", "").strip()

        # CourseDeliveryMode (Apprenticeships|Traineeships|Normal)
        if "Pre-apprenticeship" in all_info:
            course_data['Course Delivery Mode'] = "Pre-apprenticeship"
        elif "Apprenticeship" in all_info:
            course_data['Course Delivery Mode'] = "Apprenticeship"
        elif "Traineeship" in all_info or "VET" in all_info:
            course_data['Course Delivery Mode'] = "Traineeship"
            # course_data['Local_Fees']
        else:
            course_data['Course Delivery Mode'] = "Normal"

        clean_tags(course_name)
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
    else:
        course_data['Course'] = ""

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    # print(course_data['Course Delivery Mode'])
    # Description
    course_desc = soup.select(".courseDetailPage-secSubtitle")
    if course_desc:
        description(course_desc)
    else:
        course_data['Description'] = "N/A"

    # print(course_data['Course'], "///", course_data['Description'], course_data['Website'])

    # Faculty
    faculty_col = soup.select_one("a:nth-of-type(2) span[itemprop='title']")
    if faculty_col:
        fac = faculty_col.text.replace("1 evening per week", "")
        # print(fac)
        course_data['Faculty'] = fac
    else:
        course_data['Faculty'] = ""

    # Duration
    dura = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblLocalDuration")
    for to in dura:
        p_word = to.text
        durationo(p_word)

    # LOCATION/CITY
    campus = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblLocalCampus")
    campus2 = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl00_PageHeader_lblLocalCampus")
    if campus:
        for camp in campus:
            campu = camp.text.lower()
            # print(campu)
            for i in possible_cities:
                if i in campu:
                    actual_cities.append(possible_cities[i])
    elif campus2:
        for campi in campus2:
            campur = campi.text.lower()
            for i in possible_cities:
                if i in campur:
                    actual_cities.append(possible_cities[i])
    else:
        print("Find city")

    # print(actual_cities, course_data['Website'])

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
        course_data['Local_Fees'] = "NoLocalFee"

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
    # print(course_data['Course Delivery Mode'],course_data['FREE TAFE'],course_data['Local_Fees'], course_data[
    # 'Website'])

    # Career Outcomes
    overview = soup.find("section", id="overview")

    if overview:
        career = overview.find("ul")
        if career:
            course_data['Career_Outcomes/path'] = career.text.strip()
        else:
            course_data['Career_Outcomes/path'] = "None"
    else:
        course_data['Career_Outcomes/path'] = "None"

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
                    else:
                        course_data['Prerequisite_2_grade_2'] = "N/A"
                # Int_fees
                int_money = soup.select("p#p_lt_ctl02_pageplaceholder_p_lt_ctl01_PageHeader_lblIntlFees")
                if money:
                    int_money_r(int_money)

                else:
                    course_data['Int_Fees'] = "No int"

            else:
                course_data['Availability'] = "D"
                course_data['Prerequisite_2_grade_2'] = "Na"
                course_data['Int_Fees'] = "NoIntFee"

    except Exception:
        course_data['Availability'] = "D"

    # print(course_data['Availability'], course_data['Local_Fees'], course_data['Int_Fees'], course_data['Website'],
    #     course_data['Prerequisite_2_grade_2'])

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

    print(actual_cities, course_data['Online'], course_data['Distance'], course_data['Offline'],
          course_data['Face_to_Face'], course_data['Blended'], course_data['Website'])

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
                      'Course Delivery Mode',
                      'FREE TAFE']
# tabulate our data
course_dict_keys = set().union(*(d.keys() for d in course_data_all))

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, course_dict_keys)
    dict_writer.writeheader()
    dict_writer.writerows(course_data_all)

ordered_file = csv_file_path.parent.__str__() + "/Holmesglen_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
