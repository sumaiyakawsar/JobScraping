"""Description:

    * author: Sumaiya Kawsar
    * company: Fresh Futures/Seeka Technologies
    * position: IT Intern
    * date: 27-11-20
    * description:This program extracts the corresponding course details and tabulate it.
"""
import copy
import csv
import os
import re
import time
from pathlib import Path

import DurationConverter
import TemplateData
import bs4 as bs4
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("headless")
option.add_argument('--no-sandbox')
option.add_argument("start-maximized")
option.add_argument("--disable-gpu")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/ACN_single_unit.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.parent.__str__() + '/ACN_single_unit_study.csv'

subject_data = {'Subject_or_Unit': '',
                'Subject_Objective': '',
                'Subject_Description': '',
                'Subject_Link': '',
                'Non-member_price': '',
                'Member_price': ''
                }

number = r"(\d+,\d{3})*\.*\d*"
currency_pattern = rf"\${number}"

subject_data_all = []


def tag_text(string_):
    return string_.get_text().__str__().strip()


def clean_tags(soup_):
    for tag in soup_.find_all("h3"):
        tag.decompose()  # removes unecessary hidden text if called


def description(course_description):
    for each_desc in course_description:
        subject_data['Subject_Objective'] = each_desc.text.replace("\n", "").strip()


def nm_unit_fee_r(amount):
    nm_unit_fee_raw = amount.text
    nm_unit_fee = re.search(currency_pattern, nm_unit_fee_raw)
    if nm_unit_fee:
        nm_unit_fees = nm_unit_fee.group()
        subject_data['Non-member_price'] = nm_unit_fees.replace("$", "").strip()


def m_unit_fee_r(amount):
    unit_fee_raw = amount.text
    unit_fee = re.search(currency_pattern, unit_fee_raw)
    if unit_fee:
        unit_fees = unit_fee.group()
        subject_data['Member_price'] = unit_fees.replace("$", "").strip()


for each_url in course_links_file:
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # Course-Website
    subject_data['Subject_Link'] = pure_url

    # Course-name
    course_name = soup.find("div", class_="uvc-sub-heading")
    if course_name:
        clean_tags(course_name)
        course_title = tag_text(course_name).strip()
        subject_data['Subject_or_Unit'] = course_title
    else:
        subject_data['Subject_or_Unit'] = ""

    # Description
    course_desc = soup.select(".vc_active .wpb_wrapper > p")

    if course_desc:
        description(course_desc)

    else:
        subject_data['Subject_Objective'] = "N/A"

    fee = soup.select("tr:contains('Fee') td:nth-of-type(2)")
    if fee:
        for so in fee:
            so_fee = so.text
            table = soup.find("table", class_="tablepress")
            if "Tier 1" in so_fee:
                non_member_amount = table.find(class_="row-2").find("td", class_="column-5")
                nm_unit_fee_r(non_member_amount)

                member_amount = table.find(class_="row-2").find("td", class_="column-4")
                m_unit_fee_r(member_amount)
            elif "Tier 2" in so_fee:
                non_member_amount = table.find(class_="row-3").find("td", class_="column-5")
                nm_unit_fee_r(non_member_amount)

                member_amount = table.find(class_="row-3").find("td", class_="column-4")
                m_unit_fee_r(member_amount)
            elif "Tier 3" in so_fee:
                non_member_amount = table.find(class_="row-4").find("td", class_="column-5")
                nm_unit_fee_r(non_member_amount)

                member_amount = table.find(class_="row-4").find("td", class_="column-4")
                m_unit_fee_r(member_amount)
            elif "Tier 4" in so_fee:
                non_member_amount = table.find(class_="row-5").find("td", class_="column-5")
                nm_unit_fee_r(non_member_amount)

                member_amount = table.find(class_="row-5").find("td", class_="column-4")
                m_unit_fee_r(member_amount)
            else:
                subject_data['Member_price'] = ""
                subject_data['Non-member_price'] = ""

    descript = soup.select("tr:contains('Availability') td:nth-of-type(2)")
    for to in descript:
        des = to.text
        subject_data['Subject_Description'] = des
    print(subject_data['Subject_Link'], subject_data['Subject_Description'])

    subject_data_all.append(copy.deepcopy(subject_data))

print(*subject_data_all, sep='\n')

desired_order_list = ['Subject_or_Unit',
                      'Subject_Objective',
                      'Subject_Description',
                      'Subject_Link',
                      'Non-member_price',
                      'Member_price']
# tabulate our data
with open(csv_file, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(subject_data_all)

browser.quit()
