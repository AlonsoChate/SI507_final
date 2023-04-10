import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://www.si.umich.edu'
COURSES_PATH = '/programs/courses'

## Make the soup for the Courses page
courses_page_url = BASE_URL + COURSES_PATH
response = requests.get(courses_page_url)
soup = BeautifulSoup(response.text, 'html.parser')

## For each course listed
course_listing_parent = soup.find('div', class_='item-teaser-group')
course_listing_divs = course_listing_parent.find_all('div', recursive=False)
for course_listing_div in course_listing_divs:

    ## extract the course details URL
    course_link_tag = course_listing_div.find('a')
    course_details_path = course_link_tag['href']
    course_details_url = BASE_URL + course_details_path

    ## Make the soup for course details
    response = requests.get(course_details_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ## extract course number and name
    number_name = soup.find(class_='grid--3col-2').find('h1')
    print(number_name.text.strip())

    ## extract course description
    desc = soup.find(class_='grid--3col-2').find('p')
    #print(desc.text.strip())

    ## extract credit hours
    credits = soup.find(class_='credit-hours').find('span')
    print('Credits:', credits.text.strip())

    ## extract prereqs
    prereqs_div = soup.find(class_='prerequisites-enforced')
    if (prereqs_div is not None):
        prereqs = prereqs_div.find_all('li')
        for p in prereqs:
            print('Prereq:', p.text.strip())

    print('-' * 40)

    time.sleep(1)




