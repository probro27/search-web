# from bson.objectid import ObjectId
from datetime import datetime as time

from pymongo import MongoClient

# import numpy as np
start = time.now()

client = MongoClient(
    "mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)

db = client["web-map"]
y = db["domains"]
x = db["tags"]


import csv

words = ["scraping", "error"]

z = y.find({"count": {"$gt": 0}})
count = 0
for i in z:
    count += 1
    print(i)
end = time.now()
print(count)
print(end - start)
