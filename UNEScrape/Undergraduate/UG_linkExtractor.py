"""Description:
    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 26-10-20
    * description:This script extracts all the courses links and save it in txt file.
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
def clean_tags(soup_):
    for tag in soup_.find_all(["script"]):
        tag.decompose()

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
list_of_links = []
each_url = 'https://my.une.edu.au/courses/#Undergraduate'
main_url = 'https://my.une.edu.au/'
browser.get(each_url)
pure_url = each_url.strip()
each_url = browser.page_source

soup = bs4.BeautifulSoup(each_url, 'html.parser')


result_elements = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[2]/div/div/table[2]')\
        .find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
for element in result_elements:
    link = element.find_element_by_tag_name('a').get_property('href')
    list_of_links.append(link)

result_element = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[2]/div/div/table[3]')\
        .find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
for element in result_element:
    linky = element.find_element_by_tag_name('a').get_property('href')
    list_of_links.append(linky)

print(len(list_of_links))

course_links_file_path = os.getcwd().replace('\\', '/') + '/UNE_UG_links.txt'
course_links_file = open(course_links_file_path, 'w')
for link in list_of_links:
    if link is not None and link != "" and link != "\n":
        if link == list_of_links[-1]:
            course_links_file.write(link.strip())
        else:
            course_links_file.write(link.strip() + '\n')

course_links_file.close()


browser.quit()
