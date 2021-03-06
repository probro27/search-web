
# import psycopg2
from enum import unique
from pymongo import MongoClient
from random import randint
import requests
from bs4 import BeautifulSoup
from queue import Queue
import math
import re, string

# for debugging
from pprint import pprint
client = MongoClient('mongodb://localhost:27017/')
# client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = client["web-map"]
# db.domains.create_index("url",unique=True)
db.tags.create_index("word", unique=True)










def tagparse(data,priority):
    lst_tags = {}
    try:
        for i in data:
            for j in i.text.strip().split(' '):
                # j.translate(None, j.punctuation)
                j = re.sub('[%s]' % re.escape(string.punctuation), '', j)
                if len(j) >= 4 and len(j) <=45 :
                    if lst_tags.get(j.lower()):
                        # print("hi")
                        x = (lst_tags[j.lower()]/priority) + 1
                        lst_tags[j.lower()] = x*priority
                    else:
                        lst_tags[j.lower()] = priority
                        
                else:
                    pass
        # print(lst_tags)
        return lst_tags

    except:
        return None

def htmlparser(soup, url):
    # print("running")
    priorities = [
        tagparse(soup.findAll('h1'), 10), tagparse(soup.findAll('h2'), 9), tagparse(soup.findAll('p'), 8), tagparse(soup.findAll('h3'), 9), tagparse(soup.findAll('li'), 7), tagparse(soup.findAll('b'), 8)
    ]
    
    for i in priorities:
        for key, value in i.items():
            # print(key)
            db.tags.update_one(
                filter= { "word": key },
                update= { "$addToSet": { str(math.ceil(value/10)) : url}},
                upsert=True,
                )
    # print(priorities)

# r = requests.get("https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/",timeout=(2,5))
# soup = BeautifulSoup(r.content, 'lxml')

# htmlparser(soup, "https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/")





# s = "string. With. Punctuation?" # Sample string 
# out = re.sub('[%s]' % re.escape(string.punctuation), '', s)
