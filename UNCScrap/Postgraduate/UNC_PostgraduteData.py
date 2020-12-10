"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
import pandas as pd
import DurationConverter
import TemplateData

# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument('--no-sandbox')
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/UNC_PG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/UNC_PG_courses.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("em"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


possible_cities = {'newcastle': 'Newcastle',
                   'central coast': 'Central Coast',
                   'sydney': 'Sydney',
                   'singapore': 'Singapore',
                   'online': 'Online'
                   }
currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels

faculty_key = TemplateData.faculty_key  # dictionary of course levels


def int_money_r(int_money):
    for int in int_money:
        int_fee_raw = int.text
        Int_fee = re.search(currency_pattern, int_fee_raw)
        if Int_fee:
            int_fee = Int_fee.group()
            course_data['Int_Fees'] = int_fee.replace("AUD", "").strip()
        else:
            course_data['Int_Fees'] = ""


def durations(duration_location):
    try:
        p_word = duration_location.text.strip().replace("\n", " ").strip()
        if 'full-time' in p_word.__str__().lower():
            course_data['Full_Time'] = 'Yes'
        else:
            course_data['Full_Time'] = 'No'
        if 'part-time' in p_word.__str__().lower():
            course_data['Part_Time'] = 'Yes'
        else:
            course_data['Part_Time'] = 'No'

        if 'year' in p_word.__str__().lower():
            value_conv = DurationConverter.convert_duration(p_word)
            duration = float(''.join(filter(str.isdigit, str(value_conv[0]))))
            duration_time = value_conv[1]

            if str(duration) == '1' or str(duration) == '1.00' or str(duration) == '1.0':
                duration_time = 'Year'
                course_data['Duration'] = duration
                course_data['Duration_Time'] = duration_time
            elif 'month' in duration_time.__str__().lower():
                course_data['Duration'] = duration
                course_data['Duration_Time'] = value_conv[1]

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
            course_data['Duration_Time'] = value_conv[1]
            if str(duration) == '1' or str(duration) == '1.0':
                course_data['Duration'] = duration
                course_data['Duration_Time'] = 'Day'
    except IndexError:
        course_data['Full_Time'] = ''
        course_data['Part_Time'] = ''
        course_data['Duration'] = ''
        course_data['Duration_Time'] = ''


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'University of Newcastle', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': '', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': '',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': '', 'Description': '',
                   'Career_Outcomes/path': '', 'Country': '',
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
                   'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(0.1)

    # COURSE URL
    course_data['Website'] = pure_url

    # COURSE
    courseName = soup.find('h1')
    if courseName:
        course_title = courseName.text
        course_data['Course'] = course_title

    course_level = course_title

    # Description
    descript = []
    degree_description = soup.select(".body-content > div.grid-content div:nth-of-type(1) p")
    degree_description2 = soup.select(".landing-page-intro")
    degree_description3 = soup.select("#degree-details > p:nth-of-type(1)")
    if degree_description:
        for deg in degree_description:
            descript.append(deg.text)
            course_data['Description'] = ' '.join(descript).strip()
    elif degree_description2:
        for deg in degree_description2:
            descript.append(deg.text)
            course_data['Description'] = ' '.join(descript).strip()
    elif degree_description3:
        for deg in degree_description3:
            descript.append(deg.text)
            course_data['Description'] = ' '.join(descript).strip()
    else:
        course_data['Description'] = "None"

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_level:
                course_data['Level_Code'] = i

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i

    career_path = []
    # Career Outcome
    career = soup.select(".about-tab li")
    career2 = soup.select("#career-opportunities p:nth-of-type(1)")
    if career:
        for car in career:
            career_path.append(car.text)
        career_path = ', '.join(career_path)
        course_data['Career_Outcomes/path'] = career_path

    elif career2:
        for car in career2:
            career_path.append(car.text)
        career_path = ', '.join(career_path)
        course_data['Career_Outcomes/path'] = career_path
    else:
        course_data['Career_Outcomes/path'] = " "

    availability = []
    ti2 = soup.select("tr:contains('Duration') td")
    if ti2:
        for time1 in ti2:
            availability.append(time1.text)
            durations(time1)
    #Cities
    factsHeader = soup.find('div', class_="fast-facts-header")
    city_ = soup.select(".degree-template > div.uon-snapshot select")
    if factsHeader:
        available = factsHeader.find('nav', class_="fast-fact-toggle").findAll('a')
        for a in available:
            tempLine = a.text.lower()
            for i in possible_cities:
                if i in tempLine:
                    actual_cities.append(possible_cities[i])
    elif city_:
        for a in city_:
            tempLine = a.text.lower()
            for i in possible_cities:
                if i in tempLine:
                    actual_cities.append(possible_cities[i])

    # Course fees
    try:
        moneyColumn = soup.select("tr:contains('Fees') li")
        money1 = soup.select(
            "#panel > div.fast-facts.ff-in-header.fast-facts-pg > div > div.fast-facts-content > div.fast-fact-items.visible > div:nth-child(1) > div:nth-child(3)")

        if money1:
            int_money_r(money1)


    except IndexError:
        course_data['Int_Fees'] = ""

    # IELTS
    ieltsvalue = soup.select('.inner div.flex-inner:nth-of-type(2) li:nth-of-type(1)')
    for a in ieltsvalue:
        raw_ielts = tag_text(a)
        ielts = re.findall(r'\d+\.*\d*', raw_ielts)[0]
        course_data['Prerequisite_2_grade_2'] = ielts

    # Online/Offline/Blended
    if "Newcastle" in actual_cities or "Central Coast" in actual_cities or "Sydney" in actual_cities:
        course_data['Offline'] = "Yes"
    else:
        course_data['Offline'] = "No"

    if "Online" in actual_cities:
        course_data['Online'] = "Yes"
    else:
        course_data['Online'] = "No"

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

    # All courses
    courses_detail = []
    courses = browser.find_elements_by_css_selector(".title a.popup-link")
    course111 = browser.find_elements_by_css_selector(".course-requirement-group .title a")
    if course111:
        for te in course111:
            subs_link = te.get_property("href")
            if subs_link not in courses_detail:
                courses_detail.append(subs_link)
            else:
                del subs_link
    elif courses:
        for te in courses:
            subs_link = te.get_property("href")
            if subs_link not in courses_detail:
                courses_detail.append(subs_link)
            else:
                del subs_link

    try:
        button = browser.find_element_by_link_text("View the full course list")
        if button:
            button.click()
            time.sleep(2)
            handbook_url = browser.current_url
            browser.get(handbook_url)
            handbook_url = browser.page_source
            soup2 = bs4.BeautifulSoup(handbook_url, 'lxml')

            moneyColumn = soup2.select("tr:contains('Fees') li")
            if moneyColumn:
                int_money_r(moneyColumn)

            duration_availability = soup2.select("tr:contains('Duration') td")
            if duration_availability:
                for time1 in duration_availability:
                    availability.append(time1.text)
                    durations(time1)

            course1 = browser.find_elements_by_css_selector(".subject_hass .title a")
            course2 = browser.find_elements_by_css_selector("#section-core-courses-required .title a")
            course3 = browser.find_elements_by_css_selector("div.course-list:nth-of-type(1) .title a")
            course4 = browser.find_elements_by_css_selector(".course-requirement-group .title a")  # .title a.popup-link

            if course2:
                for to in course2:
                    subs_link = to.get_property('href')
                    if subs_link not in courses_detail:
                        courses_detail.append(subs_link)
                    else:
                        del subs_link
            elif course1:
                for to in course2:
                    subs_link = to.get_property('href')
                    if subs_link not in courses_detail:
                        courses_detail.append(subs_link)
                    else:
                        del subs_link

            elif course3:
                for to in course3:
                    subs_link = to.get_property('href')
                    if subs_link not in courses_detail:
                        courses_detail.append(subs_link)
                    else:
                        del subs_link
            elif course4:
                for te in course4:
                    subs_link = te.get_property('href')
                    if subs_link not in courses_detail:
                        courses_detail.append(subs_link)
                    else:
                        del subs_link
    except Exception:
        pass

    i = 1
    for each_link in courses_detail:
        browser.get(each_link)
        each_link = browser.page_source
        subject_details_soup = bs4.BeautifulSoup(each_link, 'lxml')
        time.sleep(0.5)
        try:
            # Course-name
            course_name = subject_details_soup.find("h1")
            if course_name:
                course_code = course_name.small.text
                course_title = course_name.text
                if course_code:
                    course_data[f'Subject_or_Unit_{i}'] = course_title.replace(course_code, course_code + " ")
                else:
                    course_data[f'Subject_or_Unit_{i}'] = course_name.text
            else:
                course_data[f'Subject_or_Unit_{i}'] = " "

            # Description
            course_desc = subject_details_soup.select("#course-details > p:nth-of-type(1)")

            if course_desc:
                for each_desc in course_desc:
                    course_data[f'Subject_Objective_{i}'] = each_desc.text.replace("\n", " ").strip()

            else:
                course_data[f'Subject_Objective_{i}'] = ""

            subs_availability = subject_details_soup.find("div", class_="fast-facts-header")
            if subs_availability:
                avail = subs_availability.text.lower()
                if "not currently offered" in avail:
                    course_data[f'Subject_Description_{i}'] = "Not currently Offered"
                elif "available" in avail:
                    course_data[f'Subject_Description_{i}'] = "Available"
            else:
                course_data[f'Subject_Description_{i}'] = ""
        except Exception:
            course_data[f'Subject_or_Unit_{i}'] = ""
            course_data[f'Subject_Objective_{i}'] = ""
            course_data[f'Subject_Description_{i}'] = ""

        i += 1
        if i == 40:
            break

    if "Au" in course_data['Int_Fees']:
        course_data['Int_Fees'] = ""

    for avail in availability:
        if "australian" in avail.lower() and "international" in avail.lower():
            course_data['Availability'] = "A"
        elif "australian" in avail.lower() and "international" not in avail.lower():
            course_data['Availability'] = "D"
        elif "international" in avail.lower() and "australian" not in avail.lower():
            course_data['Availability'] = "I"
        else:
            course_data['Availability'] = "N"

    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i.lower()]
        # Country
        if "Singapore" in course_data['City']:
            course_data['Country'] = "Singapore"
        else:
            course_data['Country'] = "Australia"
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
                      'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40'
                      ]

# tabulate our data
df = pd.DataFrame(course_data_all, columns=desired_order_list)
df.to_csv(csv_file, index=False)

browser.quit()
