"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 10-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import os
import time
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://www.boxhill.edu.au/search/?view=search'
list_of_study_areas = []
list_of_links = []
list_of_courses = []

browser.get(courses_page_url)
delay_ = 5


def all_study_areas():
    result_elements = browser.find_elements_by_css_selector("a.listing__link")
    for element in result_elements:
        link = element.get_property('href')
        # print(link)
        if link not in list_of_study_areas:
            list_of_study_areas.append(link)
        else:
            del link

    print(len(list_of_study_areas))
    print(list_of_study_areas)


def course(courses):
    result_elements = courses.find_elements_by_css_selector(".ais-Hits-item a")

    for element in result_elements:
        link = element.get_property('href')

        if link not in list_of_courses:
            list_of_courses.append(link)
        else:
            del link


def all_courses(list_):
    for each_url in list_:
        browser.get(each_url)

        condition = True
        while condition:
            courses = browser.find_element_by_css_selector("ul.ais-Hits-list")
            course(courses)

            try:
                browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
                    EC.presence_of_element_located(By.CSS_SELECTOR,
                                                   ".flexibile-tile-list__container .ais-Pagination-item--nextPage a")))
            except Exception:
                condition = False

            print(len(list_of_courses))
        print(list_of_courses)


# SAVE TO FILE
def save_courses(link_list, filename_):
    course_links_file_path = os.getcwd().replace('\\', '/') + filename_

    course_links_file = open(course_links_file_path, 'w')
    for link in link_list:
        if link is not None and link != "" and link != "\n":
            if link == link_list[-1]:
                course_links_file.write(link.strip())
            else:
                course_links_file.write(link.strip() + '\n')
    course_links_file.close()


all_study_areas()
all_courses(list_of_study_areas)
# save_courses(list_of_courses, '/BH_links.txt')

browser.quit()
