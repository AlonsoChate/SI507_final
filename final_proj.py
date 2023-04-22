from rotten_tomatoes import get_review_list as get_rotten_tomatoes
from metacritic import get_review_list as get_metacritic
from utility import loadCache, storeCache
from math import ceil
from plotly import express as px
from plotly import offline as pyo
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re

scoreTree = []

timeTree = {}

###########################################
#                                         #
#              Scraping                   #
#                                         #
###########################################


def get_review_raw_data(movie_name, num=200):
    ''' Combine reviews from rotten tomatoes and metacritic
        if cache available, get from cache directly
    '''
    filename = f'cache/{movie_name}_reviews.json'
    reviews = loadCache(filename)
    if len(reviews)==0:
        RT = get_rotten_tomatoes(movie_name, num)
        MC = get_metacritic(movie_name, num)
        reviews = [RT[0]+RT[0], RT[1]+MC[1]]
        storeCache(filename, reviews)
    return reviews


def get_score_tree(data):
    ''' construct score tree from data
        score tree keeps the index into raw data
        one branch is critics-score-list of index
    '''
    global scoreTree
    scoreTree = [
        [[] for _ in range(10)],  # critics
        [[] for _ in range(10)]   # audience
    ]
    for weight in range(2):
        for index in range(len(data[weight])):
            # critics [name, time, score, text]
            score = ceil(data[weight][index][2]*10)
            if score == 10:
                score = 9
            scoreTree[weight][score].append(index)
            index += 1


def get_time_tree(data):
    ''' construct time tree from data
        time tree keeps the scores
        one branch is year-month-list of scores
    '''
    global timeTree
    month_map = {
        "Jan" : 0, "Feb" : 1,
        "Mar" : 2, "Apr" : 3,
        "May" : 4, "Jun" : 5,
        "Jul" : 6, "Aug" : 7,
        "Sep" : 8, "Oct" : 9,
        "Nov" : 10, "Dec" : 11
    }
    #insert data into tree
    for weight in range(2):
        for entry in data[weight]:
            time = entry[1]
            if time != "":
                # granularity is month
                month, _, year = time.replace(",", "").split(" ")
                if year not in timeTree:
                    timeTree[year] = [[] for _ in range(12)]
                timeTree[year][month_map[month]].append(entry[2])


def get_trees(data, movie_name):
    ''' construct score tree and time tree
        cacheable
    '''
    filename = f'cache/{movie_name}.json'
    result = loadCache(filename)
    if len(result) == 0:
        global scoreTree, timeTree
        get_score_tree(data)
        get_time_tree(data)
        result = [scoreTree, timeTree]
        storeCache(filename, result)
    else:
        scoreTree, timeTree = result


###########################################
#                                         #
#   Data processing and visualization     #
#                                         #
###########################################


def get_reviews(movie_name, isHighScore=True):
    ''' get reviews of high score or low score
    '''
    data = get_review_raw_data(movie_name)
    get_trees(data, movie_name)
    global scoreTree
    critic = []
    audience = []
    start_score = 7 if isHighScore else 0
    for score in range(start_score, start_score+3):
        for index in scoreTree[0][score]:
            if data[0][index][3] != "":
                critic.append(data[0][index])
        for index in scoreTree[1][score]:
            if data[1][index][3] != "":
                audience.append(data[1][index])
    if isHighScore:
        critic.reverse()
        audience.reverse()
    return [critic, audience]


def score_distribution(movie_name):
    ''' get overall score distribution
    '''
    data = get_review_raw_data(movie_name)
    get_trees(data, movie_name)
    global scoreTree
    value = {
        "critics": [len(i) for i in scoreTree[0]],
        "audience": [len(i) for i in scoreTree[1]],
    }
    df = pd.DataFrame(value)
    fig = px.bar(df)
    fig.update_layout(
        title_text="Overal score distirbution",
        title_x=0.5,
        xaxis_title_text="Normalized score",
        yaxis_title_text="Number"
    )
    pyo.plot(fig, filename=f'templates/{movie_name}_score_distribution.html', auto_open=False)


def time_distribution(movie_name):
    ''' get score distribution with time
    '''
    data = get_review_raw_data(movie_name)
    get_trees(data, movie_name)
    global timeTree
    keys = list(timeTree.keys())
    keys.sort()
    value = []
    label = []
    for year in keys:
        for month in range(len(timeTree[year])):
            try:
                temp = timeTree[year][month]
                value.append(float(sum(temp))/len(temp))
                label.append(year+'/'+str(month+1))
            except:
                continue

    fig = px.line(x=label, y=value)
    fig.update_layout(
        title_text="Average score with time",
        title_x=0.5,
        xaxis_title_text="Time stamp",
        yaxis_title_text="Average of normalized score"
    )
    pyo.plot(fig, filename=f'templates/{movie_name}_time_distribution.html', auto_open=False)


def get_common_words(movie_name, isHighScore=True, isCritics=True, num=30):
    ''' get commonly used works for reviews of high score or low score
    '''
    data = get_review_raw_data(movie_name)
    get_trees(data, movie_name)
    global scoreTree
    long_string = ""
    set = 0 if isCritics else 1
    start_score = 7 if isHighScore else 0
    # add extra space to make sure words are seperated
    for score in range(start_score, start_score+3):
        for review_index in scoreTree[set][score]:
            review = data[set][review_index][3]
            long_string += (" " + review)

    # split string into words
    long_words = re.split("\W+", long_string.lower())

    # remove filler words and digits
    filler_words = []
    try:
        filler_words = stopwords.words('english')
    except:
        nltk.download('stopwords')
    words = [word for word in long_words if word not in filler_words and not word.isdigit()]

    # sort by frequency, and select the first several
    common_words = [word[0] for word in Counter(words).most_common(num)]
    return ", ".join(common_words)


# def draw_common_words(movie_name, isHighScore=True, isCritics=True, num=30):
#     ''' visualization for common words
#     '''
#     common_words = get_common_words(movie_name, isHighScore, isCritics, num)
