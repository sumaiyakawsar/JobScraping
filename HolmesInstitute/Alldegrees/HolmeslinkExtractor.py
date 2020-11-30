"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 27-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import os
from pathlib import Path
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
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
courses_page_url = 'https://www.holmes.edu.au/pages/schools-and-faculties/higher-education/courses'
list_of_links = []


browser.get(courses_page_url)


def all_study_areas():
    result_elements = browser.find_elements_by_css_selector("#slider_S33 a")
    for element in result_elements:
        link = element.get_property('href')
        # print(link)
        if link not in list_of_links:
            if "holmes" in link:
                list_of_links.append(link)
            else:
                del link
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
                course_links_file.write(link.strip() + "\n")
    course_links_file.close()


all_study_areas()

save_courses(list_of_links, '/Holmes_links.txt')

browser.quit()
