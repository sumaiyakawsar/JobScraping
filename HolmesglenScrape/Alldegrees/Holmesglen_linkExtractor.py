"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 16-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import os
from pathlib import Path
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://holmesglen.edu.au/Courses/'
list_of_study_areas = []
list_of_links = []
list_of_course_areas = []

browser.get(courses_page_url)


def all_study_areas():
    result_elements = browser.find_elements_by_css_selector("a.courseNavigation-title")
    for element in result_elements:
        link = element.get_property('href')
        if link not in list_of_study_areas:
            list_of_study_areas.append(link)
        else:
            del link

    print(len(list_of_study_areas))
    print(list_of_study_areas)


def all_course_areas(list_):
    for each_url in list_:
        browser.get(each_url)

        result_course = browser.find_elements_by_css_selector("a.subHubListing-course")
        for element in result_course:
            link = element.get_property('href')
            if link not in list_of_course_areas:
                list_of_course_areas.append(link)
            else:
                del link

    print(len(list_of_course_areas))
    print(list_of_course_areas)


def all_course_links(list_):
    for each_url_link in list_:
        browser.get(each_url_link)

        result_links = browser.find_elements_by_css_selector("a.linkOverlay")
        for elem in result_links:
            link = elem.get_property('href')
            if link not in list_of_links:
                list_of_links.append(link)
            else:
                del link
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
                course_links_file.write(link.strip() + '\n')
    course_links_file.close()


all_study_areas()
all_course_areas(list_of_study_areas)
all_course_links(list_of_course_areas)
save_courses(list_of_links, '/holmesglen_links.txt')  # 228

browser.quit()
