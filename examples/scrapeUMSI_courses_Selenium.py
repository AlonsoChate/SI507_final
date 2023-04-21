from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  
# info about how to install webdriver_manager https://pypi.org/project/webdriver-manager/


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get('https://www.si.umich.edu/programs/courses/')

from selenium.webdriver.common.by import By
## https://selenium-python.readthedocs.io/locating-elements.html

course_elements = driver.find_element(By.CLASS_NAME, 'item-teaser-group')

a_tags = course_elements.find_elements(By.TAG_NAME, 'a')

# Print the href attribute of each a tag
for a_tag in a_tags:
    print(a_tag.get_attribute('href'))

h2_tags = course_elements.find_elements(By.TAG_NAME, 'h2')
# Print the text of each a tag
for h2_tag in h2_tags:
    print(h2_tag.text)

desc_tags = course_elements.find_elements(By.CLASS_NAME, 'wysiwyg-content') #notice class_name only accepts 1 class name. you can do body.wysiwyg-content but you cant do body wysiwyg-content
# Print the text of each a tag
for desc_tag in desc_tags:
    print(desc_tag.text) 

desc = course_elements.find_elements(By.CSS_SELECTOR, ".body.wysiwyg-content") #note the leading period
# Print the text of each a tag
for desc_tag in desc:
    print(desc_tag.text) 

#### now that we've documented that this works, lets make a list of dictionaries
Course_Info = []

for a in a_tags:
    Course_Info.append(
        {
        'URL':a.get_attribute('href')
        })
driver.quit()

driver = webdriver.Chrome(service=service)

for z in Course_Info:
    driver.get(z['URL']) #this will navigate to each site. Fill the loop with code to get the data you want through tags just like we did on https://www.si.umich.edu/programs/courses/






