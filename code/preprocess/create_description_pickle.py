import os
import re
import json
import pandas as pd
import numpy as np
from tqdm import tqdm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier

from analyze.connect_db import MysqlController
from eunjeon import Mecab

tqdm.pandas()

sw = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',"hadn't",
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
    'won', "won't", 'wouldn', "wouldn't", '소설', '년'
]

def get_tfidf_info(info, max_features=10, stop_words=None):
    tfidf = TfidfVectorizer(max_features=max_features, stop_words=stop_words)
    return tfidf.fit_transform(info), tfidf.get_feature_names()

def get_counter_info(info, max_features=10, stop_words=None):
    counter = CountVectorizer(max_features=max_features, stop_words=stop_words)
    return counter.fit_transform(info), counter.get_feature_names()

def get_neareast_book_info(matrix, n_neighbors=50):
    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(matrix)

def filter_by_pos(text, accepts=["NNG", "NNP", "NNB", "VA", "VV", "VX", "VCP", "SL", "SH"]):
    mecab = Mecab()
    temp = []
    try:
        for pos in mecab.pos(text):
            if pos[1] in accepts:
                temp.append(pos[0])
    except:
        pass
    del mecab
    return " ".join(temp)

db = MysqlController()
sql = "SELECT * FROM books_book"

rows = db.execute(sql)
books = pd.DataFrame(rows)
books_desc = books[["id", "description"]]
books_desc = books_desc[books_desc["description"].isna()==False]
books_desc["description"] = books_desc["description"].progress_apply(lambda x: re.sub('&.*;', "", x))
books_desc["description"] = books_desc["description"].progress_apply(filter_by_pos)

books_ids = books_desc["id"].values
book_desc_data = pd.Series(data=books_desc["description"].values, index=books_ids)

book_desc_data.to_pickle("preprocessed_books_descriptions.pkl")

books_title = books[["id", "title"]]
books_title = books_title[books_title["title"].isna()==False]
# books_title["title"] = books_title["title"].progress_apply(lambda x: re.sub('&.*;', "", x))
books_title["title"] = books_title["title"].progress_apply(filter_by_pos)

books_ids2 = books_title["id"].values
book_title_data = pd.Series(data=books_title["title"].values, index=books_ids2)
book_title_data.to_pickle("preprocessed_books_title.pkl")