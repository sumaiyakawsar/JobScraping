"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 02-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""

import os
from pathlib import Path
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_argument("start-maximized")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://www.usq.edu.au/study'
list_of_groups = []
list_of_links = []
browser.get(courses_page_url)


def all_faculty():
    result_elements = browser.find_element_by_xpath('/html/body/div[1]/section[2]/div[2]/div/div/div/div[2]/div'). \
        find_elements_by_css_selector(".no-gutter a")
    for element in result_elements:
        link = element.get_property('href')
        if "help" in link:
            del link
        else:
            list_of_groups.append(link)
    print(len(list_of_groups))
    print(list_of_groups)


def all_courses(list_):
    for each_url in list_:
        browser.get(each_url)
        courses = browser.find_elements_by_css_selector(".c-program-table__program-link")

        for element in courses:
            course_link = element.get_property('href')
            if course_link not in list_of_links:
                list_of_links.append(course_link)
            else:
                del course_link
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


all_faculty()
all_courses(list_of_groups)
save_courses(list_of_links, '/USQ_link.txt')

browser.quit()
