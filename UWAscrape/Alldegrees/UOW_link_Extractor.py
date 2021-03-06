"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 09-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import os
from pathlib import Path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://coursefinder.uow.edu.au/search-results/index.html'
list_of_courses = []
browser.get(courses_page_url)
the_url = browser.page_source
delay_ = 5


def all_courses():
    condition = True
    while condition:
        result_elements = browser.find_elements_by_css_selector(".course-listing li")
        for element in result_elements:
            link = element.find_element_by_css_selector('a.course-title').get_property('href')
            if link not in list_of_courses:
                list_of_courses.append(link)
            else:
                del link

        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'>')]"))))
        except TimeoutException:
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


all_courses()
save_courses(list_of_courses, '/uow_links.txt')

browser.quit()
