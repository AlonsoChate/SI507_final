from rotten_tomatoes import get_review_list as get_rotten_tomatoes
from metacritic import get_review_list as get_metacritic
from utility import loadCache, storeCache
from math import ceil
from plotly import graph_objs as go
from plotly import express as px
from plotly import offline as pyo
import pandas as pd

scoreTree = []

timeTree = {}

def get_review_raw_data(movie_name):
    filename = f'cache/{movie_name}_reviews.json'
    reviews = loadCache(filename)
    if len(reviews)==0:
        movie_name = "shawshank_redemption"
        RT = get_rotten_tomatoes(movie_name, 30)
        movie_name = "the-shawshank-redemption"
        MC = get_metacritic(movie_name, 30)
        reviews = [RT[0]+RT[0], RT[1]+MC[1]]
        storeCache(filename, reviews)
    return reviews

def get_score_tree(data):
    # score tree keeps the reviews(in index)
    # should all have score
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
    # time tree only need scores
    # some may not have time stamp
    # year - month - number of reviews
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


def score_distribution(movie_name):
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
    data = get_review_raw_data(movie_name)
    get_trees(data, movie_name)
    global timeTree

    value = []
    
    df = pd.DataFrame(value)
    fig = px.line(df)
    fig.update_layout(
        title_text="Average score with time",
        title_x=0.5,
        xaxis_title_text="Time stamp",
        yaxis_title_text="Average of normalized score"
    )
    pyo.plot(fig, filename=f'templates/{movie_name}_time_distribution.html', auto_open=False)


time_distribution("THE SHAWSHANK REDEMPTION")