import os
import re
import random
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
from tqdm import tqdm
from konlpy.tag import Mecab

from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

from accounts.models import User
from books.models import Book
from reviews.models import Review

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

tqdm.pandas()
dir_path = os.path.dirname(os.path.realpath(__file__))

stopwords = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',"hadn't",
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
    'won', "won't", 'wouldn', "wouldn't", '소설', '년', "장편소설", "단편소설", "단편", "장편"
]

def set_isbn_add1(isbn_add):
    
    if isbn_add:
        if len(isbn_add) == 4:
            return "0"
        elif len(isbn_add) == 5:
            return isbn_add[0]
        else:
            return None
    else:
        return None

def set_isbn_add2(isbn_add):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_add[0]
        elif len(isbn_add) == 5:
            return isbn_add[1]
        else:
            return None
    else:
        return None

def set_isbn_add3(isbn_add):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_add[1:3]
        elif len(isbn_add) == 5:
            return isbn_add[2:4]
        else:
            return None
    else:
        return None

def get_isbn_columns():
    cols = []
    for i in range(0, 10):
        cols.append(f"isbn_add1_{str(i)}")
    for i in range(0, 10):
        cols.append(f"isbn_add2_{str(i)}")
    for i in range(0, 100):
        cols.append(f"isbn_add3_{str(i).zfill(2)}")
        
    return cols

def get_nan_dataframe(x, y):
    nan_data = np.empty((len(x), len(y)))
    nan_data[:] = np.NaN
    return pd.DataFrame(
                data=nan_data,
                index=x,
                columns=y
            )

def get_processed_dataframe(dataframe):
    isbn_key = "isbn_add_original"
    new_df = dataframe[[isbn_key]]

    new_df["isbn_add1"] = new_df[isbn_key].apply(set_isbn_add1)
    new_df["isbn_add2"] = new_df[isbn_key].apply(set_isbn_add2)
    new_df["isbn_add3"] = new_df[isbn_key].apply(set_isbn_add3)

    return new_df[["isbn_add1", "isbn_add2", "isbn_add3"]]

# def get_description_dataframe(dataframe):
#     return 

def fill_nan_dataframe(nan_dataframe, dataframe):
    isbn_info = dataframe.values

    for idx in tqdm(range(0, len(isbn_info))):
        info = isbn_info[idx]

        a1 = "isbn_add1_"+info[0]
        a2 = "isbn_add2_"+info[1]
        a3 = "isbn_add3_"+info[2]

        iloc = nan_dataframe.iloc[idx]
        
        b1 = iloc[a1] 
        b2 = iloc[a2]
        b3 = iloc[a3] 

        iloc[a1] = 1 if np.isnan(b1) else b1 + 1
        iloc[a2] = 1 if np.isnan(b2) else b2 + 1
        iloc[a3] = 1 if np.isnan(b3) else b3 + 1

    return nan_dataframe

def get_user_like_book_data(user):
    book_list = user.like_books.all()
    df = pd.DataFrame(book_list.values())
    return df

def get_user_unlike_book_data(user):
    book_list = user.unlike_books.all()
    df = pd.DataFrame(book_list.values())
    return df

def get_user_like_book_sum_series(user):
    df = get_processed_dataframe(
        get_user_like_book_data(user)
    )

    x = df.index
    y = get_isbn_columns()
    nan_df = get_nan_dataframe(x, y)

    sum_series = fill_nan_dataframe(nan_df, df).sum()
    return sum_series

def increase_dimension(sum_series):
    # 독자대상기호 + 도서내용
    key_add2 = sum_series.index[10:20]
    val_add2 = sum_series.values[10:20]
    key_add3 = sum_series.index[20:]
    val_add3 = sum_series.values[20:]
    
    new_series = pd.Series([])
    for k2, v2 in zip(key_add2, val_add2):
        for k3, v3 in zip(key_add3, val_add3):
            new_series[k2 + "_" + k3] = v2 + v3

    return new_series

def get_isbn_count_info(series):
    # _max = series.max()
    # series = series.apply(lambda x: x/_max)
    info = {key: round(val) for key, val in series.items()}
    return info

def get_isbn_counted_str(new_series):
    arr = []
    for key, val in new_series.items():
        a = (key + " ") * int(val)
        arr.append(a.rstrip())

    return arr

def nomarlize(arr):
    # max min scaling 
    max_val = max(arr)
    min_val = min(arr)
    mn = max_val - min_val
    return [(a - min_val) / (mn) for a in arr]

def get_isbn_norm_weight_info(series):
    pass

def get_tfidf_info(info, stop_words=None):
    tfidf = TfidfVectorizer(stop_words=stop_words)
    return tfidf.fit_transform(info), tfidf.get_feature_names()

def get_counter_info(info, stop_words=None):
    counter = CountVectorizer(stop_words=stop_words)
    return counter.fit_transform(info), counter.get_feature_names()

def get_tsne_info(arr, n_components=2, n_iter=5000, verbose=0):
    tsne = TSNE(n_components=n_components, n_iter=n_iter, verbose=verbose)
    Z = tsne.fit_transform(arr.T)
    return Z[:, 0], Z[:,1]

def get_neareast_book_info(matrix, n_neighbors=50):
    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(matrix)

def get_user_like_similarity(user):
    series = get_user_like_book_sum_series(user)
    series = increase_dimension(series)

    strs = get_isbn_counted_str(series)
    arr, features = get_counter_info(strs)
    x, y = get_tsne_info(arr)

    return features, x, y

# def combine_texts(text):

def filter_by_pos(text, accepts=["NNG", "NNP", "NNB", "VA", "VV", "VX", "VCP", "SL", "SH"]):
    mecab = Mecab()
    temp = []
    for pos in mecab.pos(text):
        if pos[1] in accepts:
            temp.append(pos[0])
    del mecab
    return " ".join(temp)

class RecommendBooks:
    
    desc_data: pd.Series = pd.read_pickle(dir_path + '/data/preprocessed_books_descriptions.pkl')
    desc_data.index.name = "id"
    title_data: pd.Series = pd.read_pickle(dir_path + '/data/preprocessed_books_title.pkl')
    title_data.index.name = "id"

    def __init__(self, user):
        self.user = user
        self.exclude_unliked_books()
        self.like_books = self.get_like_books()
        self.reviews = self.get_review_books()

    def exclude_unliked_books(self):
        unlike_books = get_user_unlike_book_data(self.user)
        if len(unlike_books):
            self.desc_data = self.desc_data[self.desc_data.index.isin(unlike_books["id"].values.tolist())==False]
            self.title_data = self.title_data[self.title_data.index.isin(unlike_books["id"].values.tolist())==False]

    def check_user_index(self, arr):
        try:
            idx = arr.index("user")
            arr.pop(idx)
        except:
            pass
        finally:
            return arr

    def get_like_books(self):
        return get_user_like_book_data(self.user)

    def get_review_books(self):
        return pd.DataFrame(Review.objects.filter(user=self.user.pk).values())

    def get_neareset_neighb(self, matrix, data, index_name, n_neighbors=51):
        row = data.index.get_loc(index_name)
        nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(matrix)
        distances, indices = nbrs.kneighbors(matrix.getrow(row))
        return self.check_user_index(data.reset_index().iloc[indices.flatten()]["id"].values.tolist())

    def get_recommend_books_by_desc(self):
        user = self.user
        like_books = self.like_books

        if len(like_books) == 0:
            return []

        like_books = like_books[like_books["description"].isna()==False]
        like_df = like_books[["id", "description"]]

        # user_like_books_desc = " ".join(list(like_df["description"].values))
        # user_like_books_desc = filter_by_pos(user_like_books_desc)

        test_data = self.desc_data.copy()
        test_data = test_data[test_data.index.isin(like_df["id"].values.tolist())==False]
        user_like_books_desc = test_data[test_data.index.isin(like_df["id"].values.tolist())].values

        test_data["user"] = " ".join(user_like_books_desc)
        print(test_data["user"])
        matrix, features = get_counter_info(test_data, stopwords)

        return self.get_neareset_neighb(matrix, test_data, "user")

    def get_recommend_books_by_title(self):
        user = self.user
        like_books = self.like_books

        if len(like_books) == 0:
            return []

        like_books = like_books[like_books["title"].isna()==False]
        like_df = like_books[["id", "title"]]

        # user_like_books_title = " ".join(list(like_df["title"].values))
        # user_like_books_title = filter_by_pos(user_like_books_title)

        test_data = self.title_data.copy()
        test_data = test_data[test_data.index.isin(like_df["id"].values.tolist())==False]
        user_like_books_title = test_data[test_data.index.isin(like_df["id"].values.tolist())].values

        test_data["user"] = " ".join(user_like_books_title)

        matrix, features = get_counter_info(test_data, stopwords)

        return self.get_neareset_neighb(matrix, test_data, "user")

    def get_recommend_books_by_score(self):
        reviews = self.reviews

        if len(reviews) == 0:
            return []
        
        books = pd.DataFrame(Book.objects.filter(pk__in=reviews["book_id"].values).values())
        merge_score_book = pd.merge(
            reviews, books, left_on="book_id", right_on="id"
        )
        df: pd.DataFrame = merge_score_book[["book_id", "content_score", "design_score", "isbn_add_original", "kdc_original", "description"]]

        high_score_df = df[df["content_score"] > 2]

        descs_groups = high_score_df.groupby(["kdc_original"], as_index = True).agg({'description': ' '.join})
        descs_groups["description"] = descs_groups["description"].apply(filter_by_pos)
        groups = df.groupby("kdc_original").agg(count=('kdc_original', 'size'), mean=('content_score', 'mean'))
        # groups = groups.reset_index().sort_values("count", ascending=False)

        len_reviews = len(high_score_df)
        kdc_index = descs_groups.index
        fracs = [50 * (groups.loc[idx]["count"] / len_reviews) for idx in descs_groups.index]
        fracs = np.ceil(fracs)

        test_data = self.desc_data.copy()
        test_data = test_data[test_data.index.isin(reviews["book_id"].values.tolist())==False]

        for idx in range(len(kdc_index)):
            index = descs_groups.index[idx]
            value = descs_groups.values[idx][0]
            test_data[index] = value

        matrix, features = get_counter_info(test_data, stopwords)
        nbrs = NearestNeighbors(n_neighbors=51).fit(matrix)
        recommend_book_ids = []
        td = test_data.reset_index()

        for index, kdc in enumerate(descs_groups.index):
            row = test_data.index.get_loc(kdc)
            distances, indices = nbrs.kneighbors(matrix.getrow(row))
            recommend_book_ids.extend(
                random.sample(list(td.iloc[indices.flatten()[1:]]["id"].values), int(fracs[index]))
            )

        return recommend_book_ids

    def get_recommend_books_by_others(self):
        user = self.user.pk

        if len(self.like_books) == 0:
            return []

        us = User.objects.raw(
            '''
            SELECT 
                (@cnt := @cnt + 1) as id, aa.user_id as user_id, bb.id as book_id
            FROM 
                books_book bb, accounts_user_like_books aa
                CROSS JOIN (SELECT @cnt := 0) AS dummy
            where bb.id = aa.book_id;
            '''
        )
        
        ul = []
        cols = us.columns
        for row in us:
           f = {}
           f["user_id"] = row.user_id
           f["book_id"] = str(row.book_id)
           ul.append(f)

        users = pd.DataFrame(ul, columns=["id", "user_id", "book_id"])
        le = LabelEncoder()
        le.fit(list(set(users["book_id"].values.tolist())))
        groups = users.groupby(['user_id'], as_index = True).agg({'book_id': ' '.join})

        data = pd.Series(data=groups["book_id"].values, index=groups.index)
        data.index.name = "id"
        data.astype("O")

        matrix, features = get_counter_info(data)
        row = data.index.get_loc(user)
        nbrs = NearestNeighbors(n_neighbors=101).fit(matrix)
        distances, indices = nbrs.kneighbors(matrix.getrow(row))

        recommend_books = set()
        users_books = data.loc[user].split(" ")
        closest_users = data.reset_index().iloc[indices.flatten()[1:]]["id"].values

        idx = 0
        while len(recommend_books) < 50:
            cub = data.loc[closest_users[idx]].split(" ")
            rb = list(filter(lambda i: i not in users_books, cub))
            recommend_books.update(rb)
            idx += 1

        return [int(r) for r in recommend_books]
    
    def get_recommend_books_by_genre(self):
        genres = pd.DataFrame(self.user.user_genres.all().values())

        if len(genres) == 0:
            return []

        gs = list(genres["genre"].values.astype('int32'))
        books = pd.DataFrame(Book.objects.filter(isbn_add3_id__in=gs).values())

        if len(self.like_books):
            like_df = self.like_books[["id"]]
            books = books[books.index.isin(like_df["id"].values.tolist())==False]["id"].values.tolist()
        else:
            books = books["id"].values.tolist()
            
        return random.sample(books, 50)

    def get_recommend_book_ids(self):
        return self.get_recommend_books_by_desc(), self.get_recommend_books_by_title(), self.get_recommend_books_by_score(), self.get_recommend_books_by_others(), \
                self.get_recommend_books_by_genre()

def get_recommend_books_by_desc(user):
    # books = pd.DataFrame(Book.objects.all().values())
    # books = books[["id", "description"]]

    like_books = get_user_like_book_data(user)
    like_books = like_books[like_books["description"].isna()==False]
    like_df = like_books[["id", "description"]]
    # 사용자가 좋아요 누른 책은 제외
    # books = books[books["id"].isin(like_df["id"].values.tolist()) == False]
    unlike_books = get_user_unlike_book_data(user)
    # if len(unlike_books):
    #     # 사용자가 싫어요 누른 책은 제외
    #     books = books[books["id"].isin(unlike_books["id"].values.tolist()) == False]

    # books = books[books["description"].isna()==False]
    # books["description"] = books["description"].progress_apply(lambda x: re.sub('&.*;', "", x))
    # books["description"] = books["description"].progress_apply(filter_by_pos)
    # books_ids = books["id"].values
    user_like_books_desc = " ".join(list(like_df["description"].values))
    # like_df["description"] = like_df["description"].apply(lambda x: re.sub('&.*;', "", x))
    user_like_books_desc = filter_by_pos(user_like_books_desc)

    # test_data = pd.Series(data=books["description"].values, index=books_ids)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_data: pd.Series = pd.read_pickle(dir_path + '/data/preprocessed_books_descriptions.pkl')
    test_data = test_data[test_data.index.isin(like_df["id"].values.tolist())==False] # 좋아요한 책은 제외
    test_data.index.name = "book_id"
    # 싫어요한 책 제외
    if len(unlike_books):
        test_data = test_data[test_data.index.isin(unlike_books["id"].values.tolist())==False]
    test_data["user"] = user_like_books_desc
    matrix, features = get_tfidf_info(test_data, stopwords)

    nbrs = NearestNeighbors(n_neighbors=51).fit(matrix)
    row = test_data.index.get_loc("user")
    distances, indices = nbrs.kneighbors(matrix.getrow(row))
    td = test_data.reset_index()
    # names_similar = pd.Series(indices.flatten()).map(test_data.reset_index()['id'])
    # result = pd.DataFrame({'distance':distances.flatten(), 'name':names_similar})
    return td.iloc[indices.flatten()[1:]]["book_id"].values

def get_recommend_books_by_title(user):
    like_books = get_user_like_book_data(user)
    like_books = like_books[like_books["title"].isna()==False]
    like_df = like_books[["id", "title"]]

    unlike_books = get_user_unlike_book_data(user)

    user_like_books_title = " ".join(list(like_df["title"].values))
    user_like_books_title = filter_by_pos(user_like_books_title)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_data: pd.Series = pd.read_pickle(dir_path + '/data/preprocessed_books_title.pkl')
    test_data = test_data[test_data.index.isin(like_df["id"].values.tolist())==False] # 좋아요한 책은 제외
    test_data.index.name = "book_id"
    # 싫어요한 책 제외
    if len(unlike_books):
        test_data = test_data[test_data.index.isin(unlike_books["id"].values.tolist())==False]

    test_data["user"] = user_like_books_title
    matrix, features = get_counter_info(test_data, stopwords)

    nbrs = NearestNeighbors(n_neighbors=51).fit(matrix)
    row = test_data.index.get_loc("user")
    distances, indices = nbrs.kneighbors(matrix.getrow(row))

    td = test_data.reset_index()
    return td.iloc[indices.flatten()[1:]]["book_id"].values

def get_recommend_books_by_score(user):
    reviews = pd.DataFrame(Review.objects.filter(user=user.pk).values())

    if len(reviews) == 0:
        return []

    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_data: pd.Series = pd.read_pickle(dir_path + '/data/preprocessed_books_descriptions.pkl')
    test_data.index.name = "book_id"
    unlike_books = get_user_unlike_book_data(user)
    if len(unlike_books):
        test_data = test_data[test_data.index.isin(unlike_books["id"].values.tolist())==False]

    books = pd.DataFrame(Book.objects.filter(pk__in=reviews["book_id"].values).values())
    merge_score_book = pd.merge(
        reviews, books, left_on="book_id", right_on="id"
    )
    df: pd.DataFrame = merge_score_book[["book_id", "content_score", "design_score", "isbn_add_original", "kdc_original", "description"]]

    high_score_df = df[df["content_score"] > 2]

    descs_groups = high_score_df.groupby(["kdc_original"], as_index = True).agg({'description': ' '.join})
    descs_groups["description"] = descs_groups["description"].apply(filter_by_pos)
    groups = df.groupby("kdc_original").agg(count=('kdc_original', 'size'), mean=('content_score', 'mean'))
    # groups = groups.reset_index().sort_values("count", ascending=False)

    len_reviews = len(high_score_df)
    kdc_index = descs_groups.index
    fracs = [50 * (groups.loc[idx]["count"] / len_reviews) for idx in descs_groups.index]
    fracs = np.ceil(fracs)

    for idx in range(len(kdc_index)):
        index = descs_groups.index[idx]
        value = descs_groups.values[idx][0]
        test_data[index] = value

    matrix, features = get_counter_info(test_data, stopwords)
    nbrs = NearestNeighbors(n_neighbors=51).fit(matrix)
    recommend_book_ids = []
    td = test_data.reset_index()

    for index, kdc in enumerate(descs_groups.index):
        row = test_data.index.get_loc(kdc)
        distances, indices = nbrs.kneighbors(matrix.getrow(row))
        k = random.sample(list(td.iloc[indices.flatten()[1:]]["book_id"].values), int(fracs[index]))
        recommend_book_ids.extend(
            random.sample(list(td.iloc[indices.flatten()[1:]]["book_id"].values), int(fracs[index]))
        )
    return recommend_book_ids