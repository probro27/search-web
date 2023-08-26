from dotenv import load_dotenv
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient

import re
import nltk
import os

tf_doc = []

load_dotenv()

## for client connecting
if os.environ.get("ENVIRONMENT") == "dev":
    client = MongoClient("mongodb://localhost:27017/")
else:
    client = MongoClient(os.environ.get("ATLAS_URI"))


## Db connect and index creation for unique words
db = client["web-map"]
db.tags.create_index("word", unique=True)

def bodyClean(body):
    body = str(body)
    CLEANR = re.compile(r"<[^>]*>")
    cleantext = CLEANR.sub("", body)
    ## uncomment this while running for first time ....
    nltk.download('omw-1.4')
    nltk.download('wordnet')
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    doc = re.sub("[^a-zA-Z]", " ", cleantext)
    doc = doc.lower()
    doc = doc.split()
    doc = [lemmatizer.lemmatize(word) for word in doc if not word in set(stopwords)]
    doc = " ".join(doc)
    return doc

def term_frequency(term, body):
    normalized_document = body.lower().split()
    return normalized_document.count(term.lower()) / float(len(normalized_document))

def compute_normalizedtf(document):
    sentence = document.lower().split()
    norm_tf = dict.fromkeys(set(sentence), 0)
    for word in sentence:
        norm_tf[word] += term_frequency(word, document)
    tf_doc.append(norm_tf)
    
def htmlparse(soup, url):
    body = soup.find("body")
    compute_normalizedtf(bodyClean(body))
