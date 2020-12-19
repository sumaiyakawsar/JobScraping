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
browser = webdriver.Chrome(executable_path=exec_path, options=option)  # , options=option

# MAIN ROUTINE
courses_page_url = 'https://www.ecu.edu.au/degrees/courses?query=!padrenull&profile=ecu2020&f.Tabs=&collection=ecu-web&num_ranks=50&f.Tabs%7Cecu-fs-courses=Courses&f.Degree%20type%7Ce=Undergraduate&sort=title'
list_of_links = []
browser.get(courses_page_url)
delay_ = 5  # seconds


# KEEP CLICKING NEXT UNTIL THERE IS NO BUTTON COLLECT THE LINKS
def course():
    condition = True
    while condition:
        result_elements = browser.find_element_by_xpath('//*[@id="mainContent"]/main/div/div[2]/div[5]') \
            .find_elements_by_tag_name('h3')
        for element in result_elements:
            link = element.find_element_by_tag_name('a').get_property('href')
            if link not in list_of_links:
                list_of_links.append(link)
        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Next'))))
        except TimeoutException:
            condition = False

    print(len(list_of_links))
    print(list_of_links)


# SAVE TO FILE
def save_course(list_, filename_):
    course_links_file_path = os.getcwd().replace('\\', '/') + filename_
    course_links_file = open(course_links_file_path, 'w')
    for link in list_:
        if link is not None and link != "" and link != "\n":
            if link == list_[-1]:
                course_links_file.write(link.strip())
            else:
                course_links_file.write(link.strip() + '\n')
    course_links_file.close()


course()
save_course(list_of_links, '/ECU_UG_links.txt')

browser.close()
