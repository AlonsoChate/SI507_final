from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.by import By
import time
import re
from utility import loadCache, storeCache

BASE_URL = 'https://www.rottentomatoes.com/m/'
PATH_1 = '/reviews' #path for critics
PATH_2 = '/reviews?type=user' # path for normal audience

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # don't open windows when running the program
service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)
# driver = webdriver.Chrome(service=service)

# get some overal information
def get_basic(movie_name):
    driver.get(BASE_URL + movie_name)
    description = driver.find_element(By.XPATH, '//*[@id="movie-info"]/div/div/drawer-more/p').text
    release_date = driver.find_element(By.XPATH, '//*[@id="info"]/li[7]/p/span/time').text
    return [description, release_date]

# For critics
def get_critic_review(movie_name):
    driver.get(BASE_URL + movie_name + PATH_1)
    critic = []
    while(True):
        reviews = driver.find_elements(By.CLASS_NAME, 'review-row')
        for i in reviews:
            try:
                reviewer_name = i.find_element(By.CLASS_NAME, 'display-name').text
                review_text = i.find_element(By.CLASS_NAME, 'review-text').text
                score_and_time = i.find_element(By.CLASS_NAME, 'original-score-and-url').text.split(' | ')
                score = re.findall(r"\d+\.?\d*",score_and_time[1])
                grade = float(score[0])/float(score[1])
                time_stamp = score_and_time[2] # Format: Mar 18, 2022
                # append to list
                review = [reviewer_name, time_stamp, grade, review_text]
                critic.append(review)
            except:
                continue
        # next page
        next_btn = driver.find_element(By.XPATH, '//*[@id="reviews"]/div[1]/rt-button[2]')
        if(not next_btn.is_displayed()):
            break
        next_btn.click()
        time.sleep(1)
    return critic


# For normal audience
def get_audience_review(movie_name, num=500):
    driver.get(BASE_URL + movie_name + PATH_2)
    audience = []
    while(True):
        reviews = driver.find_elements(By.CLASS_NAME, 'audience-review-row')
        for i in reviews:
            try:
                reviewer_name = i.find_element(By.CLASS_NAME, 'audience-reviews__name').text
                review_text = i.find_element(By.CSS_SELECTOR, '.audience-reviews__review.js-review-text').text
                time_stamp = i.find_element(By.CLASS_NAME, 'audience-reviews__duration').text # Format: Mar 18, 2022
                
                # score is displayed as stars, so need to convert to number format
                score = i.find_element(By.CLASS_NAME, 'audience-reviews__score')
                full_star = score.find_elements(By.CLASS_NAME, 'star-display__filled ')
                half_star = score.find_elements(By.CLASS_NAME, 'star-display__half ')
                grade = len(full_star) + 0.5*len(half_star)
                review = [reviewer_name, time_stamp, grade, review_text]
                audience.append(review)
            except:
                continue
        
        # next page
        next_btn = driver.find_element(By.XPATH, '//*[@id="reviews"]/div[1]/rt-button[2]')
        if(not next_btn.is_displayed() or len(audience)>num):
            break
        next_btn.click()
        time.sleep(1)
    return audience


def get_review_list(movie_name, num=500):
    # movie: movie name
    # num: number of reviews for common audience
    # check if cache is available
    filename = f'rotten_tomatoes_{movie_name}.json'
    result = loadCache(filename)
    if len(result) == 0:
        basic_info = get_basic(movie_name)
        critic = get_critic_review(movie_name)
        audience = get_audience_review(movie_name, num)
        result = [basic_info, critic, audience]
        storeCache(filename, result)
    return result

# get_review_list("shawshank_redemption")
