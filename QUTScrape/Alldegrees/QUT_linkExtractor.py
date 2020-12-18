"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 05-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import os
import time
from pathlib import Path
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
#option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://www.qut.edu.au/study/postgraduate'
list_of_groups = []
list_of_links = []
list_of_courses = []
browser.get(courses_page_url)


def all_faculty():
    result_elements = browser.find_element_by_xpath('//*[@id="content"]/div[4]/div/div/div[2]/ul'). \
        find_elements_by_css_selector(".list-links a")

    for element in result_elements:
        link = element.get_property('href')
        if "languages" in link:
            del link
        else:
            list_of_groups.append(link)
    print(len(list_of_groups))
    print(list_of_groups)


def area(list_):
    for each_url in list_:
        browser.get(each_url)
        course_area = browser.find_elements_by_css_selector("a.tab:nth-of-type(n+2)")
        if course_area:
            for ea in course_area:
                area_link = ea.get_property('href') + "?postgraduate"
                list_of_links.append(area_link.strip())

        print(len(list_of_links))
    print(list_of_links)


def course_add(sel):
    for ea in sel:
        course_website = ea.find_element_by_tag_name("a").get_property("href")
        course_link = course_website + "?international"
        if course_link not in list_of_courses:
            if "online-courses" not in course_link:
                list_of_courses.append(course_link)
            elif "online-courses" in course_website:
                del course_website

        elif course_link in list_of_courses:
            del course_link
            del course_website


def courses(list_):
    for each_url in list_:
        browser.get(each_url)

        time.sleep(3)

        courses_col = browser.find_elements_by_css_selector(".open div.card")
        if courses_col:
            course_add(courses_col)

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


all_faculty()
area(list_of_groups)
try:
    browser.find_element_by_xpath('//*[@id="course-filter-audience-international"]').click
    browser.find_element_by_xpath('//*[@id="course-category-listing-filters"]/form/div[2]/div/label').click
except NoSuchElementException:
    print('NoSuchElement to be clicked')
    pass
except TimeoutException:
    print("Timeout")
    pass
courses(list_of_links)
save_courses(list_of_courses, '/QUT_link.txt')

browser.quit()
