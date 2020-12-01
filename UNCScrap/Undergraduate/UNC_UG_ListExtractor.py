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
import os


def clean_tags(soup_):
    for tag in soup_.find_all("tr", class_='hidethis'):
        tag.decompose()


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
course_links = []
each_url = 'https://www.newcastle.edu.au/degrees#filter=level_undergraduate,level_undergraduate_honours,' \
           'location_callaghan,location_newcastle_city,location_central_coast,location_sydney,location_online,' \
           'type_single '
main_url = 'https://www.newcastle.edu.au/'
browser.get(each_url)
pure_url = each_url.strip()
each_url = browser.page_source

soup = bs4.BeautifulSoup(each_url, 'lxml')
clean_tags(soup)


def all_courses():
    each_courses_links = soup.find_all('a', class_='degree-link')
    for tag in each_courses_links:
        var = main_url + tag['href']
        if var not in course_links:
            course_links.append(var)
        else:
            del var

    print(len(course_links))


def save_courses(link_list, filename_):
    course_links_file_path = os.getcwd().replace('\\', '/') + filename_
    course_links_file = open(course_links_file_path, 'w')

    for i in link_list:
        if i is not None and i is not "" and i is not "\n":
            if i == link_list[-1]:
                course_links_file.write(i.strip())
            else:
                course_links_file.write(i.strip() + '\n')

    course_links_file.close()
    print(*course_links, sep='\n')


all_courses()
save_courses(course_links, '/UNC_UG_links.txt')

browser.quit()

