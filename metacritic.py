from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.by import By
import re

BASE_URL = 'https://www.metacritic.com'
PATH_0 = '/movie/the-shawshank-redemption'
PATH_1 = '/movie/the-shawshank-redemption/critic-reviews'
PATH_2 = '/movie/the-shawshank-redemption/user-reviews'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # don't open windows when running the program
service = ChromeService(executable_path=ChromeDriverManager().install())

# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service)

# get some overal information
if 0:
    driver.get(BASE_URL + PATH_0)
    description = driver.find_element(By.XPATH, '//*[@id="movie-info"]/div/div/drawer-more/p').text
    release_date = driver.find_element(By.XPATH, '//*[@id="info"]/li[7]/p/span/time').text

# For critics
if 0:
    driver.get(BASE_URL + PATH_1)
    reviews = driver.find_elements(By.CSS_SELECTOR, '.review.pad_top1.pad_btm1')
    for i in reviews:
        reviewer_name = i.find_element(By.CLASS_NAME, 'author').text
        review_text = i.find_element(By.CLASS_NAME, 'no_hover').text

        #TODO: no timestamp for critics so need to deal with it
        score = i.find_element(By.CSS_SELECTOR, '.metascore_w.large.movie.positive.indiv.perfect').text
        grade = float(score)/100 # critic score is out of 100

# For normal audience
if 0:
    driver.get(BASE_URL + PATH_2)
    reviews = driver.find_elements(By.CSS_SELECTOR, '.review.pad_top1')
    for i in reviews:
        reviewer_name = i.find_element(By.CLASS_NAME, 'author').text
        review_text = i.find_element(By.CLASS_NAME, 'review_body').text
        timestamp = i.find_element(By.CLASS_NAME, 'date').text # Mar 24, 2015
        score = i.find_element(By.CSS_SELECTOR, '.metascore_w.user.large.movie.mixed.indiv').text
        grade = float(score)/10 # normal score is out of 10
        pass

# they store url to next page so it's simple to just jump to new page
driver.get("https://www.metacritic.com/movie/the-shawshank-redemption/user-reviews")
next_btn = driver.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[3]/div/div[1]/div[7]/div/div[1]/span[2]/a')
next_url = next_btn.get_attribute('href')
# jump to next page
driver.get(next_url)

pass