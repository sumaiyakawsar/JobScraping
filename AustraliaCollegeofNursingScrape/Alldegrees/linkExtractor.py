"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 25-11-20
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
courses_page_url = 'https://www.acn.edu.au/education#areas-of-study'
list_of_study_areas = []
list_of_links = []
list_of_single_unit = []
list_of_cpd = []
list_of_short_course = []

browser.get(courses_page_url)


def all_study_areas():
    result_elements = browser.find_elements_by_css_selector(".wpb_animate_when_almost_visible a")
    for element in result_elements:
        link = element.get_property('href')
        # print(link)
        if link not in list_of_study_areas:
            list_of_study_areas.append(link)
        else:
            del link

    print(len(list_of_study_areas))
    print(list_of_study_areas)


def all_course_areas(list_):
    for each_url in list_:
        browser.get(each_url)

        result_course = browser.find_element_by_css_selector("div.wpb_column:nth-of-type(1) div.vc_column-inner"). \
            find_elements_by_tag_name("a")
        for element in result_course:
            link = element.get_property('href')
            if link not in list_of_links:
                if "#" in link or "members.acn.edu.au" in link or "cnnect.acn.edu.au" in link or "training.digitalhealth" in link :
                    del link
                elif "single-unit-of-study" in link:
                    if link not in list_of_single_unit:
                        list_of_single_unit.append(link)
                    else:
                        del link
		elif "cpd" in link:
		    if link not in list_of_single_unit:
			list_of_cpd.append(link)
		    else:
			del link
                elif "short-course" in link or "307" in link or "306" in link:
                    if link not in list_of_short_course:						
			list_of_short_course.append(link)
		    else:								
			del link
                else:
                    list_of_links.append(link)
            else:
                del link

        print(len(list_of_links))

    print(list_of_single_unit)
    print(list_of_short_course)
    print(len(list_of_single_unit), len(list_of_short_course))

    print(list_of_links)
    print(len(list_of_links), "course links are added")


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
save_courses(list_of_links, '/ACN_links.txt')
save_courses(list_of_single_unit, '/ACN_single_unit.txt')

browser.quit()
