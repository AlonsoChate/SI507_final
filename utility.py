# some help functions
import json

def loadCache(filename):
    try:
        file = open(filename,"r")
        cache = json.loads(file.read())
        file.close()
    except:
        cache = {}
    return cache

def storeCache(filename, cache):
    file = open(filename, 'w')
    contents_to_write = json.dumps(cache)
    file.write(contents_to_write)
    file.close()

# could be useful for debug
def print_review():
    pass