from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.by import By
import re

BASE_URL = 'https://www.rottentomatoes.com'
PATH_0 = '/m/shawshank_redemption'
PATH_1 = '/m/shawshank_redemption/reviews'
PATH_2 = '/m/shawshank_redemption/reviews?type=user'

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
    reviews = driver.find_elements(By.CLASS_NAME, 'review-row')
    for i in reviews:
        reviewer_name = i.find_element(By.CLASS_NAME, 'display-name').text
        review_text = i.find_element(By.CLASS_NAME, 'review-text').text
        score_and_time = i.find_element(By.CLASS_NAME, 'original-score-and-url').text.split(' | ')
        if len(score_and_time) != 3:
            # if the review has no grade, discard it for now
            break
        score = re.findall(r"\d+\.?\d*",score_and_time[1])
        grade = float(score[0])/float(score[1])
        time_stamp = score_and_time[2] # Format: Mar 18, 2022


# For normal audience
if 0:
    driver.get(BASE_URL + PATH_2)
    reviews = driver.find_elements(By.CLASS_NAME, 'audience-review-row')
    for i in reviews:
        reviewer_name = i.find_element(By.CLASS_NAME, 'audience-reviews__name').text
        review_text = i.find_element(By.CSS_SELECTOR, '.audience-reviews__review.js-review-text').text
        time_stamp = i.find_element(By.CLASS_NAME, 'audience-reviews__duration').text # Format: Mar 18, 2022
        
        # score is displayed as stars, so need to convert to number format
        score = i.find_element(By.CLASS_NAME, 'audience-reviews__score')
        full_star = score.find_elements(By.CLASS_NAME, 'star-display__filled ')
        half_star = score.find_elements(By.CLASS_NAME, 'star-display__half ')
        grade = len(full_star) + 0.5*len(half_star)


# test for next page
import time
driver.get("https://www.rottentomatoes.com/m/shawshank_redemption/reviews")
next_btn = driver.find_element(By.XPATH, '//*[@id="reviews"]/div[1]/rt-button[2]')
time.sleep(1)
next_btn.click()
# TODO: get access to the new page

pass