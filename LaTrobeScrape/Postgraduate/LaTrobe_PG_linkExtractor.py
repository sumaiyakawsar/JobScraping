"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 30-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://www.latrobe.edu.au/courses'
list_of_groups = []
list_of_links = []
browser.get(courses_page_url)
the_url = browser.page_source

delay_ = 5  # seconds


def click_btn():
    browser.find_element_by_xpath("/html/body/div[1]/div/ul/li[2]/button").click()


def all_faculty():
    result_elements = browser.find_element_by_xpath('//*[@id="bodyContent"]/div[2]/div[3]/div/ol'). \
        find_elements_by_tag_name('li')
    for element in result_elements:
        link = element.find_element_by_tag_name('a').get_property('href')
        if "help" in link:
            del link
        else:
            link = link + "/all?study_level=pg"
            list_of_groups.append(link)


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


click_btn()
all_faculty()
save_courses(list_of_groups, '/LaTrobe_PG_links.txt')

browser.close()
