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


def search_movie_name(movie_name):
    ''' search movie name and get url for metacritic
        return None if movie not found
    '''
    para = movie_name.replace(" ", "%20")
    url = f"https://www.metacritic.com/search/movie/{para}/results"
    driver.get(url)
    movie = driver.find_element(By.CSS_SELECTOR, ".result.first_result")
    global BASE_URL
    BASE_URL = movie.find_element(By.TAG_NAME, "a").get_attribute('href')


def get_critic_review():
    ''' get all critic reviews in one list, need to run after search_movie_name
        format:
        [[name, time, score, text], ...]
    '''
    # it seems that metacritic place critic reviews all in one page
    driver.get(BASE_URL + PATH_1)
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


def get_audience_review(num=100):
    ''' get normal audience reviews in one list, need to run after search_movie_name
        format:
        [[name, time, score, text], ...]
    '''
    driver.get(BASE_URL + PATH_2)
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

        try:
            next_btn = driver.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div[3]/div/div[1]/div[7]/div/div[1]/span[2]/a')
            if(not next_btn.is_displayed() or len(audience)>num):
                break
            next_url = next_btn.get_attribute('href')
            # jump to next page
            driver.get(next_url)
        except:
            break
    return audience


def get_review_list(movie_name, num=100):
    ''' get list of reviews from cache if available, else scrape data from website
        format: [[critic reviews], [andience reviews]]
    '''
    filename = f'cache/metacritic_{movie_name}.json'
    result = loadCache(filename)
    if len(result) == 0:
        search_movie_name(movie_name)
        critic = get_critic_review()
        audience = get_audience_review(num)
        result = [critic, audience]
        storeCache(filename, result)
    return result
