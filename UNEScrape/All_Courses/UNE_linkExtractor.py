"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 26-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
each_url = 'https://www.une.edu.au/search?form=wrapper&f.Tabs|une-courses-push=Courses&profile=_default&f.Level+of+study|StudyLevels=Bachelor+Honours&f.Level+of+study|StudyLevels=Postgraduate&f.Level+of+study|StudyLevels=Postgraduate+Research&f.Level+of+study|StudyLevels=Undergraduate&f.Level+of+study|StudyLevels=Foundation+Studies&fmo=true&collection=une-push-meta'
browser.get(each_url)
list_of_courses = []
delay_ = 9


def courses():
    condition = True
    while condition:
        result_elements = browser.find_elements_by_css_selector("div.panel-description")
        for element in result_elements:
            link = element.find_element_by_css_selector('.panel-description__header-main a').get_property('href')
            if link not in list_of_courses:
                if "bespokecourses" in link:
                    del link
                else:
                    list_of_courses.append(link)
            else:
                del link
        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(.,'Next Page')]"))))
        except TimeoutException:
            condition = False

    print(len(list_of_courses))
    print(list_of_courses)


def save_file(list_, filename_):
    course_links_file_path = os.getcwd().replace('\\', '/') + filename_
    course_links_file = open(course_links_file_path, 'w')
    for link in list_:
        if link is not None and link != "" and link != "\n":
            if link == list_[-1]:
                course_links_file.write(link.strip())
            else:
                course_links_file.write(link.strip() + '\n')
    course_links_file.close()


courses()
save_file(list_of_courses, '/UNE_links.txt')

browser.quit()
