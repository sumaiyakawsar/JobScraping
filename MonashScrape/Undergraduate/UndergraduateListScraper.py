"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 20-10-20
    * description:This program extracts the specific course links on each page of the given URL as specified by \n
     \t CourseTypeLinkExtractor.py. The end results are fed to another program that tabulates the given data
"""
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re


def get_page(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return bs4.BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        pass
    return None


# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)


# MAIN ROUTINE
course_type_links = []
course_links = []
each_url = 'https://www.monash.edu/study/courses/find-a-course?f.Tabs%7CcourseTab=Undergraduate&f.InterestAreas%7CcourseInterestAreas='
browser.get(each_url)
pure_url = each_url.strip()
each_url = browser.page_source

soup = bs4.BeautifulSoup(each_url, 'html.parser')

each_courses_links = soup.find_all('a', class_='box-featured__heading-link')

for tag in each_courses_links:
    var = tag['title'].replace("domestic", "international")
    course_links.append(var)

course_links_file_path = os.getcwd().replace('\\', '/') + '/monash_undergraduate_links.txt'
course_links_file = open(course_links_file_path, 'w')

print(len(each_courses_links))

for i in course_links:
    if i is not None and i is not "" and i is not "\n":
        if i == course_links[-1]:
            course_links_file.write(i.strip())
        else:
            course_links_file.write(i.strip()+'\n')

course_links_file.close()
print(*course_links, sep='\n')
