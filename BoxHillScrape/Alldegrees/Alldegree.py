"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 11-11-20
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
course_links_file_path = course_links_file_path.__str__() + '/bh_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/BHI_unordered.csv'

course_data = {'Level_Code': '',
               'University': 'Box Hill Institute',
               'City': '',
               'Course': '',
               'Faculty': '',
               'Fees': '',
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

possible_cities = {'box hill': 'Melbourne',
                   'lilydale': 'Melbourne',
                   'melbourne':'Melbourne'
                   }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all(class_="hidden-lg-up"):
        tag.decompose()  # removes unecessary hidden text if called


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def description(course_description):
    for each_desc in course_desc:
        course_data['Description'] = each_desc.text.replace("\n", "").replace("About the course", "").strip()


def durationo(p_word):
    if p_word:
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

        elif 'months' in p_word.__str__().lower():
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

        else:
            course_data['Duration'] = ""
            course_data['Duration_Time'] = ''
    else:
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''
        course_data['Full_Time'] = ""
        course_data['Part_Time'] = ""


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
        course_title = tag_text(course_name)
        course_data['Course'] = course_title
    else:
        course_data['Course'] = ""

        # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i

    # print(course_data['Course'], course_data['Website'], course_data['Level_Code'],course_data['Faculty'])

    # Description
    course_desc = soup.select(".course-intro__details")
    if course_desc:
        description(course_desc)
        # print(course_desc.text)
    else:
        course_data['Description'] = "N/A"

    faculty_col = soup.find("h2", class_="body-1")
    if faculty_col:
        fac = faculty_col.text.split(", ")
        # print(fac)
        course_data['Faculty'] = fac[0]
    else:
        course_data['Faculty'] = ""

    # print(course_data['Course'],course_data['Website'],course_data['Faculty'])

    del_mode = soup.select("#banner > div.banner__left > ul")
    if del_mode:
        for ea in del_mode:
            all_info = ea.text.strip().replace("\n", " ").replace(course_data['Course'], ""). \
                replace(course_data['Faculty'], "").strip()
            # print(all_info)
            # FREE TAFE
            if "Free TAFE" in all_info or "Free tafe" in all_info:
                course_data['FREE TAFE'] = "Yes"
            else:
                course_data['FREE TAFE'] = "No"
            if "Blended Learning" in all_info:
                course_data['Blended'] = "Yes"
                course_data['Online'] = "Yes"
                course_data['Offline'] = "Yes"
                course_data['Face_to_Face'] = "Yes"
                course_data['Distance'] = "Yes"
            else:
                course_data['Blended'] = ""
                course_data['Online'] = ""
                course_data['Offline'] = ""
                course_data['Face_to_Face'] = ""
                course_data['Distance'] = ""

            if "Online Learning" in all_info:
                course_data['Online'] = "Yes"

            # CourseDeliveryMode|Apprenticeships|Traineeships|Normal
            if "Pre-apprenticeship" in all_info:
                course_data['Course Delivery Mode'] = "Pre-apprenticeship"
            elif "Apprenticeship" in all_info:
                course_data['Course Delivery Mode'] = "Apprenticeship"
            elif "Traineeship" in all_info:
                course_data['Course Delivery Mode'] = "Traineeship"
            else:
                course_data['Course Delivery Mode'] = "Normal"

            # city
            if "Lilydale Lakeside Campus" in all_info:
                actual_cities.append("Melbourne")
            if "Box Hill Campus - Nelson" in all_info:
                actual_cities.append("Melbourne")
            if "Box Hill Campus - Elgar" in all_info:
                actual_cities.append("Melbourne")
            if "City Campus" in all_info:
                actual_cities.append("Melbourne")

    if pure_url.endswith("-d/"):
        course_data['Availability'] = "D"
    elif pure_url.endswith("-i/"):
        course_data['Availability'] = "I"
    else:
        course_data['Availability'] = "A"

    # print(actual_cities, course_data['Website'],course_data['Course Delivery Mode'],course_data['Availability'])

    # Duration/Duration Time/FullTime/Parttime/
    course_detail = soup.find(id="main").find("div", class_="wrapper").find("div", class_="module tabbed-content")
    if course_detail:
        tabs = course_detail.find("ul", class_="tabbed-content__list").find_all("li", class_="headline")
        content = course_detail.find("div", class_="tabbed-content__details").find_all("div",
                                                                                       class_="tabbed-content__detail")
        if tabs:
            for ea in tabs:
                for eo in content:
                    if ea.text in eo.text:
                        datas = eo.find("div", class_="tabbed-content__content")
                        # Duration
                        if "Course Length" in datas.text:
                            course_len = datas.find_all("div", class_="rich-text")
                            for ro in course_len:
                                ft_pt = ro.text

                                if ft_pt:
                                    if 'full time' in ft_pt.lower() or 'ft' in ft_pt.lower() and 'part time' not in ft_pt.lower():
                                        course_data['Full_Time'] = 'Yes'
                                    else:
                                        course_data['Full_Time'] = 'No'

                                    if 'part time' in ft_pt.lower() or 'part' in ft_pt.lower() and 'full time' not in ft_pt.lower() or 'ft' in ft_pt.lower():
                                        course_data['Part_Time'] = 'Yes'
                                    else:
                                        course_data['Part_Time'] = 'No'
                                try:
                                    p_word = ro.text.replace(ea.text, "").replace("27", "").replace("2020", ""). \
                                        replace("2021", "").replace("3rd", ""). \
                                        replace("June 9, July 21, August 14, September 4 and October 9", ""). \
                                        replace(
                                        "The next course starts  April  but we do have rolling enrolments, so you can enrol throughout the year",
                                        ""). \
                                        replace("You can enrol throughout the year", ""). \
                                        replace("Online: any time throughout the year", ""). \
                                        replace("On campus course: Next intake October 2019 (Term 4). "
                                                "Term 4 intake is being 'fast tracked'. Students will attend"
                                                " 4 days in term 4 in 2019 and 2 days per week for Semester 1 in  Traineeship: "
                                                "any time throughout the year", ""). \
                                        replace("20 April - City Campus 5 October - Elgar Campus", ""). \
                                        replace("Two options are available: ", ""). \
                                        replace("Elgar: February and July (full time day classes)"
                                                " Lilydale: July (part time day classes) City: January and July "
                                                "(blended delivery: 2 evenings a week)", "").strip()
                                    durationo(p_word)

                                except Exception:
                                    course_data['Duration'] = ''
                                    course_data['Duration_Time'] = ''

                        # Career Outcomes
                        if "Career" in datas.text:
                            if datas:
                                career_det = datas.find_all("div", class_="rich-text")
                                for each_carer in career_det:
                                    course_data['Career_Outcomes/path'] = each_carer.text.strip().replace("\n", "")
                            elif eo:
                                course_data['Career_Outcomes/path'] = eo.text.strip()
                            else:
                                course_data['Career_Outcomes/path'] = "NA"

                        # Fees
                        if "Fees" in datas.text:
                            # print(ea.text, datas.text)
                            if datas:
                                money_table = datas.find("table", class_="table-course-fees")
                                if money_table:
                                    rea = money_table.select(
                                        "tr:contains('Payable Estimate (at commencement)') td:nth-of-type(2)")
                                    money = money_table.select("tr:contains('Estimated') td:nth-of-type(2)")
                                    if rea:
                                        for sea in rea:
                                            # mone = sea.text
                                            Int_feeRa = tag_text(sea)
                                            Int_fee = re.search(currency_pattern, Int_feeRa)
                                            if Int_fee:
                                                int_feer = Int_fee.group()
                                                course_data['Fees'] = int_feer.replace("$", "").strip()
                                            # print(course_data['Fees'], course_data['Website'])
                                    elif money:
                                        for hea in money:
                                            Int_feeRa = tag_text(hea)
                                            Int_fee2 = re.search(currency_pattern, Int_feeRa)
                                            if Int_fee2:
                                                int_feer = Int_fee2.group()
                                                course_data['Fees'] = int_feer.replace("$", "").strip()
                                            # print(course_data['Fees'], course_data['Website'])
                                    else:
                                        print("None", course_data['Website'])
                                elif "contact your secondary school regarding fees for this program" in datas.text:
                                    course_data['Fees'] = "Secondary School"
                                else:
                                    try:
                                        money_data = datas.find("div", class_="accordion__content").p
                                        if money_data:
                                            int_raw = money_data.text
                                            Int_ee = re.search(currency_pattern, int_raw)
                                            if Int_ee:
                                                int_iu = Int_ee.group()
                                                course_data['Fees'] = int_iu.replace("$", "").strip()
                                            else:
                                                course_data['Fees'] = "NA"
                                        else:
                                            course_data['Fees'] = "NA"
                                    except IndexError:
                                        course_data['Fees'] = "NA"

                            else:
                                print("NNNNN")

                        # IELTS
                        if "English" in ea.text:
                            ielts_amount = eo.text.strip()
                            if has_numbers(ielts_amount):
                                ielts = re.findall(r'\d+(?:\.*\d*)?', ielts_amount)[0]
                                course_data['Prerequisite_2_grade_2'] = ielts
                            else:
                                course_data['Prerequisite_2_grade_2'] = "N/A"
        else:
            course_data['Career_Outcomes/path'] = "NA"
            course_data['Prerequisite_2_grade_2'] = "NA"
    # print(course_data['Prerequisite_2_grade_2'], course_data['Website'])

    #print(course_data['Duration'], course_data['Duration_Time'], course_data['Website'])
    # print(course_data['Career_Outcomes/path'],course_data['Website'])
    # print(course_data['Fees'], course_data['Website'])

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

    # print(course_data['Website'], course_data['Local_Fees'],course_data['Prerequisite_1_grade_1'])
    if "Yes" in course_data['FREE TAFE']:
        course_data['Fees'] = "0"
    print(course_data['Fees'],course_data['Description'])

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
                      'Fees',
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

ordered_file = csv_file_path.parent.__str__() + "/bh_ordered.csv"
with open(csv_file, 'r', encoding='utf-8') as infile, open(ordered_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)

browser.quit()
