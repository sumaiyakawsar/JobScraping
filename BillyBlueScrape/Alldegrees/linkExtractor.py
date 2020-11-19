"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 19-11-20
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
courses_page_url = 'https://www.billyblue.edu.au/courses'
list_of_courses = []

browser.get(courses_page_url)


# Extracting all courses link
def all_courses():
    result_elements = browser.find_elements_by_css_selector(".col-lg-3 > a")
    for element in result_elements:
        link = element.get_property('href')
        # print(element.text.strip().replace("\n", " "))

        if link not in list_of_courses:
            list_of_courses.append(link)
        else:
            del link

        if 'short' in link:
            list_of_courses.remove(link)
        if 'bachelor-of-creative-technologies-game-art' in link:
            list_of_courses.remove(link)

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


# call all functions
all_courses()
save_courses(list_of_courses, '/BillyBlue_links.txt')

browser.quit()
