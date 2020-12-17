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
import pandas as pd
import os
import copy
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
course_links_file_path = course_links_file_path.__str__() + '/CDU_UG_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/CDU_UG_Allcourses.csv'


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("strong"):
        tag.decompose()


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


possible_cities = {'palmerston': 'Darwin',
                   'casuarina': 'Darwin',
                   'alice springs': 'Adelaide',
                   'sydney': 'Sydney',
                   'darwin': 'Darwin',
                   'adelaide': 'Adelaide',
                   'online': 'Online'}

currency_pattern = r"(?:[\£\$\€\(AUD)\]{1}[,\d]+.?\d*)"

course_data_all = []

level_key = TemplateData.level_key  # dictionary of course levels


def durations(course_detail):
    for ra in course_detail:
        try:
            course_duration = ra.text
            if course_duration:
                p_word = course_duration.__str__().strip()
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

        except IndexError:
            course_data['Duration'] = 'error'
            course_data['Duration_Time'] = ''


for each_url in course_links_file:
    course_data = {'Level_Code': '', 'University': 'Charles Darwin University', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years',
                   'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
                   'Prerequisite_1': 'ATAR', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': 'Equivalent AQF Level ',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '6.0', 'Prerequisite_3_grade_3': 'Year 12',
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
    time.sleep(0.1)

    # COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE & course level
    courseName = soup.find("div", class_="container section-header__content")
    if courseName:
        course = courseName.find("h1").text.strip()
        course_data['Course'] = course
        course_level = course

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_level:
                course_data['Level_Code'] = i
            if "bachelor" in course_level.lower() and "diploma" in course_level.lower():
                course_data['Level_Code'] = "DIP&BA"
            if "bachelor" in course_level.lower() and "master" in course_level.lower():
                course_data['Level_Code'] = "BA&MST"
            if "bachelor" in course_level.lower() and "honours" in course_level.lower():
                course_data['Level_Code'] = "BAH"

    describe = []
    # Description
    courseDescription = soup.select(
        "#course-overview > div.grid > div > div.grid__col.grid--col-7.grid--offset-1 > "
        "div.field.field-ds-chainsnode-course-content-field-course-course-overview.field-type-ds.field-label-hidden > "
        "div > div > div ")
    if courseDescription:
        for ea in courseDescription:
            describe.append(ea.text.replace("\n", " ").strip())
        course_data['Description'] = ' '.join(describe)

    # international_fees
    try:
        moneyColumn = soup.select(".field-international-fee-value .field-item div")
        if moneyColumn:
            for ea in moneyColumn:
                int_feeRaw = tag_text(ea)
                int_fee = re.findall(currency_pattern, int_feeRaw)[0].replace("$", "").strip()
                if int_fee:
                    course_data['Int_Fees'] = int_fee
                    course_data['Availability'] = "A"
                else:
                    course_data['Int_Fees'] = ""
        else:
            information = soup.select(".field-international-admissions-in div.field-item")
            if information:
                for ea in information:
                    if "No" in ea.text:
                        course_data['Int_Fees'] = ""
                        course_data['Availability'] = "D"
            else:
                course_data['Int_Fees'] = ""
    except IndexError:
        course_data['Int_Fees'] = ""

    # DECIDE THE FACULTY
    facultyCell = soup.select(".field-faculty div")
    field = soup.select(".field-sector div")
    if facultyCell:
        for ea in facultyCell:
            faculty = ea.text.strip()
            course_data['Faculty'] = faculty
    elif field:
        for ea in field:
            field = ea.text.strip()
            course_data['Faculty'] = field

    # Availability
    ava = soup.select(".js-shortlist div[data-student-type='international']")
    for so in ava:
        availa = so.text.strip().lower()
        if "not available to international students" in availa:
            course_data['Availability'] = "D"
        elif "add to shortlist" in availa:
            course_data['Availability'] = "A"
        else:
            course_data['Availability'] = "N"

    # Duration/Duration Time
    course_detail = soup.select(".field-duration-ft div")
    if course_detail:
        durations(course_detail)
    else:
        course_detail2 = soup.select(".field-duration-ft-vet p")
        durations(course_detail2)

    # Full-time/Part-time
    statement = soup.find("div", class_="grid--col-4")
    if statement:
        state = statement.find_all("div", class_="fable__row")
        if state:
            for st in state:
                label = st.text.strip().lower().strip().replace("\n", "").strip()
                if "full-time" in label:
                    if "not available" in label:
                        course_data['Full_Time'] = "No"
                    else:
                        course_data['Full_Time'] = "Yes"
                elif "part-time" in label:
                    if "not available" in label:
                        course_data['Part_Time'] = "No"
                    else:
                        course_data['Part_Time'] = "Yes"

    course_dur = soup.find("div", class_="course--duration-vet")
    if course_dur:
        course_time = course_dur.text.strip()
        if "full time" in course_time:
            course_data['Full_Time'] = "Yes"
        else:
            course_data['Full_Time'] = "Yes"
        course_data['Part_Time'] = "Yes"

    # Career Outcome
    careerDetails = soup.select(".field-career-opportunities")
    if careerDetails:
        for ea in careerDetails:
            course_data['Career_Outcomes/path'] = ea.text.strip().replace("\n", " ")
    else:
        course_data['Career_Outcomes/path'] = ""

    # Online/Offline/Face to face/Distance
    city_present = soup.select("div.grid--col-4")
    for each in city_present:
        tempLine = each.text.lower()
        for i in possible_cities:
            if i in tempLine:
                actual_cities.append(possible_cities[i])

    if "Online" in actual_cities:
        course_data['Online'] = "Yes"
    else:
        course_data['Online'] = "No"

    if "Darwin" in actual_cities or "Adelaide" in actual_cities or "Sydney" in actual_cities:
        course_data['Offline'] = "Yes"
    else:
        course_data['Offline'] = "No"

    if "Yes" in course_data['Offline']:
        course_data['Face_to_Face'] = "Yes"
    else:
        course_data['Face_to_Face'] = "No"

    if "Yes" in course_data['Online']:
        course_data['Distance'] = "Yes"
    else:
        course_data['Distance'] = "No"

    if "Yes" in course_data['Online'] and  "Yes" in course_data['Offline']:
        course_data['Blended'] = "Yes"
    else:
        course_data['Blended'] = "No"

    subject_links = []
    subjects = []
    all_links = soup.select("div.table--responsive:nth-of-type(2) a")
    if all_links:
        for lin in all_links:
            link = lin["href"]
            if link not in subject_links:
                if 'learnline' in link:
                    del link
                else:
                    subject_links.append(link)

    if len(subject_links) == 0:
        linksss = soup.select("td a")
        subs_2 = soup.select(".field-course-structure table:nth-of-type(1) tr:nth-of-type(n+3)")
        if linksss:
            for link_ in linksss:
                link = link_['href']
                if link not in subject_links:
                    subject_links.append(link)
        elif subs_2:
            for each in subs_2:
                sub_codes = each.select("td:nth-of-type(1)")
                sub_names = each.select("td:nth-of-type(2)")
                for seach in sub_codes:
                    for each_su in sub_names:
                        clean_tags(each_su)
                        clean_tags(seach)
                        subject_nam = each_su.text.strip()
                        subject_code = seach.text.strip().replace("(Select 4)", "").replace("(Select 5)", ""). \
                            replace("(compulsory)", "").replace("(Total of 6)", "").replace("(0 units)", ""). \
                            replace("Electives", "").replace("(1 units)", "").replace("(Select 7)", ""). \
                            replace("(select 5 from the following)", "").strip()
                        if subject_code is not '' and subject_nam is not '':
                            subject = subject_code + " - " + subject_nam
                            subjects.append(subject)
    s = 1
    for sub in subjects:
        course_data[f'Subject_or_Unit_{s}'] = sub
        s += 1

    i = 1
    for each_links in subject_links:
        browser.get(each_links)
        unit_url = browser.page_source
        u_url = each_links.strip()
        unit_soup = bs4.BeautifulSoup(unit_url, 'lxml')
        time.sleep(0.2)

        unit_name = unit_soup.select_one("span#P21_UNIT_HEADING")
        if unit_name:
            name_unit = unit_name.text.strip()
            if name_unit is not '':
                course_data[f'Subject_or_Unit_{i}'] = name_unit

        unit_description = unit_soup.find("span", id="P21_UNIT_DESCRIPTION_HE")
        if unit_description:
            description_unit = unit_description.text
            if description_unit is not '':
                course_data[f'Subject_Description_{i}'] = description_unit

        learning_outcomes = unit_soup.find("div", id="LearningOutcomes")
        if learning_outcomes:
            outcomes = learning_outcomes.text
            if outcomes is not '':
                course_data[f'Subject_Objective_{i}'] = outcomes
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
