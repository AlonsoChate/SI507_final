from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.by import By
from utility import loadCache, storeCache

BASE_URL = 'https://www.metacritic.com/movie/'
PATH_1 = '/critic-reviews'
PATH_2 = '/user-reviews'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # don't open windows when running the program
service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)
# driver = webdriver.Chrome(service=service)

# get some overal information
def get_basic(movie_name):
    driver.get(BASE_URL + movie_name + PATH_1)
    description = driver.find_element(By.XPATH, '//*[@id="movie-info"]/div/div/drawer-more/p').text
    release_date = driver.find_element(By.XPATH, '//*[@id="info"]/li[7]/p/span/time').text
    return [description, release_date]

# For critics
def get_critic_review(movie_name):
    # it seems that metacritic place critic reviews all in one page
    driver.get(BASE_URL + movie_name + PATH_1)
    critics = []
    reviews = driver.find_elements(By.CSS_SELECTOR, '.review.pad_top1.pad_btm1')
    for i in reviews:
        try:
            reviewer_name = i.find_element(By.CLASS_NAME, 'author').text
            review_text = i.find_element(By.CLASS_NAME, 'summary').text

            #no timestamp for critics, so make it empty now
            score = i.find_element(By.CSS_SELECTOR, '.metascore_w.large.movie').text
            grade = float(score)/100 # critic score is out of 100
            review = [reviewer_name, "", grade, review_text]
            critics.append(review)
        except:
            continue
    return critics

# For normal audience
def get_audience_review(movie_name, num=100):
    driver.get(BASE_URL + movie_name + PATH_2)
    audience = []
    while(True):
        reviews = driver.find_elements(By.CSS_SELECTOR, '.review.pad_top1')
        for i in reviews:
            reviewer_name = i.find_element(By.CLASS_NAME, 'author').text
            review_text = i.find_element(By.CLASS_NAME, 'review_body').text
            timestamp = i.find_element(By.CLASS_NAME, 'date').text # Mar 24, 2015
            score = i.find_element(By.CSS_SELECTOR, '.metascore_w.user.large.movie').text
            grade = float(score)/10 # normal score is out of 10
            review = [reviewer_name, timestamp, grade, review_text]
            audience.append(review)

        next_btn = driver.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[3]/div/div[1]/div[7]/div/div[1]/span[2]/a')
        if(not next_btn.is_displayed() or len(audience)>num):
            break
        next_url = next_btn.get_attribute('href')
        # jump to next page
        driver.get(next_url)
    return audience


def get_review_list(movie_name, num=100):
    # movie: movie name
    # num: number of reviews for common audience
    # check if cache is available
    filename = f'cache/metacritic_{movie_name}.json'
    result = loadCache(filename)
    if len(result) == 0:
        critic = get_critic_review(movie_name)
        audience = get_audience_review(movie_name, num)
        result = [critic, audience]
        storeCache(filename, result)
    return result

movie_name = "the-shawshank-redemption"