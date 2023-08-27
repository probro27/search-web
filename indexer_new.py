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
    """Used to clean the body of the html page, and get rid of the unnnecessary tags and punctuations.

    Args:
        body (str): body string produced by beautiful soup

    Returns:
        str: set of words in the body of the html page, parsed as tokens and seperated by space.
    """    
    body = str(body)
    CLEANR = re.compile(r"<[^>]*>")
    cleantext = CLEANR.sub("", body)
    ## uncomment this while running for first time ....
    nltk.download("omw-1.4")
    nltk.download("wordnet")
    nltk.download("stopwords")
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
    term_count = normalized_document.count(term.lower())
    
    #TODO remove this. Probably not needed.
    # building the word count collection
    db["word-count"].update_one(
        {"word": term}, {"$inc": {"count": term_count}}, upsert=True
    )

    # number of documents containing, update in db
    db['docs-per-word'].update_one(
        {"word": term}, {"$inc": {"count": 1}}, upsert=True
    )

    return term_count / float(len(normalized_document))


def compute_normalizedtf(document:str, url:str):

    sentence = document.lower().split()
    norm_tf = dict.fromkeys(set(sentence), 0)
    
    for word in sentence:
        norm_tf[word] += term_frequency(word, document)
    
    doc_object = {
        "url": url,
        "normalized-tf": norm_tf
    }

    db['normalized-tf'].insert_one(doc_object)


def htmlparse(soup, url):

    #what is this?
    db["metadata"].update_one(
        {"documents": "urls"}, {"$inc": {"count": 1}}, upsert=True
    )
    
    body = soup.find("body")
    compute_normalizedtf(bodyClean(body), url)
