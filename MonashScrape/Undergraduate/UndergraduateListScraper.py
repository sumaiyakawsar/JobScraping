"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
    * description:This program extracts the specific course links on each page of the given URL.
     The end results are fed to another program that tabulates the given data

"""
from pathlib import Path
from selenium import webdriver
import os


# selenium web driver - extracts the links faster
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
list_of_courses = []
courses_page_url = 'https://www.monash.edu/study/courses/find-a-course?f.Tabs%7CcourseTab=Undergraduate&f.InterestAreas%7CcourseInterestAreas='
browser.get(courses_page_url)
the_url = browser.page_source


def all_courses():
    result_elements = browser.find_elements_by_css_selector("a.box-featured__heading-link")
    for element in result_elements:
        link = element.get_property('title')
        link = link.replace("domestic", "international")
        list_of_courses.append(link)

    print(len(list_of_courses))
    print(list_of_courses)


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
save_courses(list_of_courses, '/Monash_UGinks.txt')

browser.quit()

