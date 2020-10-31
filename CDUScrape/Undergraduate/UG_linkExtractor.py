"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 27-10-20
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
courses_page_url = 'https://www.cdu.edu.au/study'
list_of_groups = []
list_of_links = []
browser.get(courses_page_url)
the_url = browser.page_source

delay_ = 5  # seconds
#browser.find_element_by_xpath("/html/body/div[1]/div/ul/li[2]/button").click()


result_elements = browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/article/div/div[4]/div/div[1]/div/div/ul').\
        find_elements_by_tag_name('li')
for element in result_elements:
    link = element.find_element_by_tag_name('a').get_property('href')
    list_of_groups.append(link)

#print(len(list_of_groups))

for each_url in list_of_groups:
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    courses = browser.find_elements_by_css_selector("#tab-1 [data-year='next'] div.course-list__course-name a")
    if courses:
        for ea in courses:
            course = ea.get_property('href')
            list_of_links.append(course)
print(len(list_of_links))

# SAVE TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/CDU_UG_links.txt'

course_links_file = open(course_links_file_path, 'w')
for link in list_of_links:
    if link is not None and link != "" and link != "\n":
        if link == list_of_links[-1]:
            course_links_file.write(link.strip())
        else:
            course_links_file.write(link.strip() + '\n')
course_links_file.close()

browser.quit()
