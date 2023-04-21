# import functions from rotten_tomatoes.py and metacritic.py to scrape data
import json
from rotten_tomatoes import get_review_list as get_rotten_tomatoes

CACHE_FILE = 'cache.json'

reviewTree = {
    "high_w": { # review weight
        "high_g": [], # review grade
        "medium_g": [],
        "low_g": []
    },
    "low weight": {
        "high_g": [],
        "medium_g": [],
        "low_g": []
    }
}

def loadCache():
    try:
        file = open(CACHE_FILE,"r")
        cache = json.loads(file.read())
        file.close()
    except:
        cache = {}
    return cache

def storeCache(cache):
    file = open(CACHE_FILE, 'w')
    contents_to_write = json.dumps(cache)
    file.write(contents_to_write)
    file.close()

cache = loadCache()
if len(cache) != 0:
    reviewTree = cache

# load data from scraping files
# data -> list of reviews?
def loadData(data):
    pass