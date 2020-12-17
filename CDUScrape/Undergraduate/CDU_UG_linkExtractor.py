"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 27-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
import os

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://www.cdu.edu.au/study'
list_of_study_areas = []
list_of_links = []
browser.get(courses_page_url)


def all_study_areas():
    result_elements = browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/article/div/div[4]/div/div[1]/div/div/ul'). \
        find_elements_by_tag_name('li')
    for element in result_elements:
        link = element.find_element_by_tag_name('a').get_property('href')
        if link not in list_of_study_areas:
            list_of_study_areas.append(link)
        else:
            del link

    print(len(list_of_study_areas))
    print(list_of_study_areas)


def all_course_areas(list_):
    for each_url in list_:
        browser.get(each_url)

        courses = browser.find_elements_by_css_selector("#tab-1 [data-year='next'] div.course-list__course-name a")
        if courses:
            for ea in courses:
                course = ea.get_property('href')
                if course not in list_of_links:
                    list_of_links.append(course)
                else:
                    del course

    print(len(list_of_links))
    print(list_of_links)


# SAVE TO FILE
def save_courses(link_list, filename_):
    course_links_file_path = os.getcwd().replace('\\', '/') + filename_

    course_links_file = open(course_links_file_path, 'w')
    for link in link_list:
        if link is not None and link != "" and link != "\n":
            if link == link_list[-1]:
                course_links_file.write(link.strip())
            else:
                course_links_file.write(link.strip() + "\n")
    course_links_file.close()


all_study_areas()
all_course_areas(list_of_study_areas)
save_courses(list_of_links, '/CDU_UG_links.txt')

browser.quit()
