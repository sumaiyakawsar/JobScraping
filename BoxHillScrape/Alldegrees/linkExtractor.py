"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 10-11-20
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
# option.add_argument("headless")
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
            print(link)
            list_of_courses.append(link)

        else:
            del link


def all_courses(list_):
    for each_url in list_:
        browser.get(each_url)

        if browser.find_element_by_xpath('//*[@id="main"]/div[1]/div[4]/div[2]/div/div/div/header/div/ul/li[4]/button'):
            browser.find_element_by_xpath(
                '//*[@id="main"]/div[1]/div[4]/div[2]/div/div/div/header/div/ul/li[4]/button').click()

        condition = True
        while condition:
            courses = browser.find_element_by_css_selector(
                "#main > div.wrapper > div:nth-child(5) > div.flexible-tile-list.module.divider > div")
            course(courses)
            try:
                browser.execute_script("arguments[0].click();", WebDriverWait(courses, delay_).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'>')]"))))
            except TimeoutException:
                condition = False

            """
            try:
                pagination = courses.find_element_by_css_selector("div > div > div > div.ais-Pagination > ul")
                if pagination:
                    page2 = pagination.find_element_by_xpath("//a[contains(text(),'2')]")

                    if page2:
                        try:
                            browser.execute_script("arguments[0].click();", WebDriverWait(pagination, delay_).until(
                                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'2')]"))))
                            
                        except TimeoutException:
                            condition = False
            except TimeoutException:
                condition = False
            except StaleElementReferenceException:
                condition = False
            """

            """
                next_classbtn = courses.find_element_by_xpath("//li[contains(.,'›')]").get_attribute("class")
                if "ais-Pagination-item--disabled" not in next_classbtn:
                    print(WebDriverWait(courses, delay_).until(EC.presence_of_element_located((By.LINK_TEXT, '>'))))
                else:
                    condition = False
            """

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
save_courses(list_of_courses, '/bh_links.txt')

browser.quit()
