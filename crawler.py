import os
import pprint
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser as Robot
from multiprocessing import pool
from multiprocessing.pool import ThreadPool as Pool
from queue import Queue
from threading import Thread
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient

import changer
import indexer

load_dotenv()


# make a cache pool(temporary storage) which stores the html tags of the website. We keep this so that the indexer can access it and do text analysis.
# instead of uniques we make a cash pools.

q = Queue(maxsize=0)
changes = Queue(maxsize=0)
cache_pool = Queue(maxsize=10000)
unique = dict()

if os.environ.get("ENVIRONMENT") == "dev":
    client = MongoClient("mongodb://localhost:27017/")
else:
    client = MongoClient(os.environ.get("ATLAS_URI"))

db = client["web-map"]
collection = db["seed-url"]

root_url = collection.find({"status": "pending"})

for i in root_url:
    q.put(i)


start_time = time.time()
seconds = 120
words = dict()


def isValidURL(url):
    regex = (
        "((http|https)://)(www.)?"
        + "[a-zA-Z0-9@:%._\\+~#?&//=]"
        + "{2,256}\\.[a-z]"
        + "{2,6}\\b([-a-zA-Z0-9@:%"
        + "._\\+~#?&//=]*)"
    )
    p = re.compile(regex)
    if re.search(p, url):
        return True
    else:
        return False


def updateChanger(url):
    # url is already validated
    global unique
    link = urlparse(url)
    domain = link.netloc
    host = link.path

    if unique.get(domain):
        # if the domain is already present in the dictionary
        if unique[domain].get(host):
            unique[domain][host] += 1
        else:
            unique[domain][host] = 1

        unique[domain]["__0__"] += 1  # number of urls of a given domain + 1
        x = unique[domain]["__0__"]  # number of unique urls in the domain

        # logic to update the database, after every consecutive change
        # until 10, then over 10 every 20 change, and over 200 every
        # 200 change.
        # TODO : perform batch update for this logic.
        if x > 10:
            if x % 200 == 0:
                changes.put([domain, unique[domain]["__0__"], "upd"])
            elif x < 200 and x % 20 == 0:
                changes.put([domain, unique[domain]["__0__"], "upd"])
        else:
            changes.put([domain, unique[domain]["__0__"], "upd"])
        return False

    else:
        unique[domain] = {"__0__": 1}
        unique[domain][host] = 1  # new element
        changes.put([domain, unique[domain]["__0__"], "new"])
        return True


def all_url(root_url):
    global q
    global unique

    try:
        link = urlparse(root_url)
        domain = link.netloc
        scheme = link.scheme
        combined_str = scheme + "://" + domain + "/robots.txt"
        rp = Robot.RobotFileParser()
        rp.set_url(combined_str)
        try:
            rp.read()
            boolean = rp.can_fetch("*", root_url)
        except:
            boolean = True

        if boolean:
            r = requests.get(root_url, timeout=(3, 5))
            soup = BeautifulSoup(r.content, "lxml", from_encoding="iso-8859-1")
            cache_pool.put([soup, root_url])
            fill = soup.findAll("a")
            lst = []
            for i in fill:
                lst.append(i.get("href"))

            for i in lst:
                if i:
                    regex1 = "(^\/[a-zA-Z*%$!)(\/&*]*)"
                    p1 = re.compile(regex1)
                    if re.search(p1, i):
                        if root_url[-1] == "/":
                            i = root_url + i[1:]
                        else:
                            i = root_url + i
                    if isValidURL(i):
                        updateChanger(i)
                        q.put(i)
                    else:
                        pass
                else:
                    pass
        else:
            pass
    except:
        pass


def print_results():
    print("queue size :" + str(q.qsize()))
    print("memory :" + str(sys.getsizeof(unique)))
    print("cachepool :" + str(cache_pool.qsize()))
    print("changes :" + str(changes.qsize()))


def main_init():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            break

        if q.empty():
            pass
        else:

            all_url(q.get())
            print("domains crawled : %10s %1s" % (str(len(unique)), "|"), end="\r")
            print("domains crawled : %10s %1s" % (str(len(unique)), "/"), end="\r")
            print("domains crawled : %10s %1s" % (str(len(unique)), "-"), end="\r")


def indexing():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time < seconds + 300:
            if cache_pool.empty() == False:
                print(
                    "indexing Left : %10s %1s" % (str(cache_pool.qsize()), "*"),
                    end="\r\t\t\t\t\t",
                )
                element = cache_pool.get()
                indexer.htmlparser(element[0], element[1])
        else:
            print_results()
            break
            # print("Cache pool empty")


def changing():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time <= seconds + 300:
            if changes.empty() == False:
                print(
                    "Changes Left : %10s %1s" % (str(changes.qsize()), "*"),
                    end="\r\t\t\t\t\t",
                )
                element = changes.get()
                changer.changes(element)
        elif elapsed_time > seconds + 300:
            print_results()
            break
        else:
            pass
            # print("Cache pool empty")


num_threads = 1
threads = []
for i in range(num_threads):
    for j in range(1):
        t1 = Thread(target=changing)
        t3 = Thread(target=indexing)
        threads.append(t1)
        t1.start()
        t3.start()
    t2 = Thread(target=main_init)
    threads.append(t2)
    t2.setDaemon(True)
    t2.start()

# for x in threads:
#     x.join()
#     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(unique)
# t1.close()
# t2.close()
