import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from .preprocess import RecommendBooks
from accounts.models import User
from books.models import Book

dir_path = os.path.dirname(os.path.realpath(__file__))

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

class UserTendency:
    
    def __init__(self, user):
        self.user = user
        self.kdc_info = pd.read_pickle(dir_path + '/data/kdc_info.pkl')
        self.user_pkl_dir = self.set_user_pkl_dir()

    def set_user_pkl_dir(self):
        return dir_path + f'/data/users_tendency/{self.user.email}_tendency.pkl'

    def create_user_tendency_table(self):
        isbn_info1 = [str(i) for i in range(0, 10)]
        isbn_info2 = [str(i).zfill(2) for i in range(0, 100)]

        empty_isbn1_table = get_nan_dataframe([0], isbn_info1)
        empty_isbn2_table = get_nan_dataframe([0], isbn_info1)
        empty_isbn3_table = get_nan_dataframe([0], isbn_info2)
        empty_kdc_table = get_nan_dataframe([0], self.kdc_info.values)
        
        table = {
            "isbn1": empty_isbn1_table,
            "isbn2": empty_isbn2_table,
            "isbn3": empty_isbn3_table,
            "kdc": empty_kdc_table,
        }

        pd.to_pickle(table, self.user_pkl_dir)

    def process_book_info(self, dataframe):
        book_info = dataframe[["isbn_add_original", "kdc_original"]]
        book_info["isbn1"] = book_info["isbn_add_original"].apply(set_isbn_add1)
        book_info["isbn2"] = book_info["isbn_add_original"].apply(set_isbn_add2)
        book_info["isbn3"] = book_info["isbn_add_original"].apply(set_isbn_add3)
        book_info = book_info.drop(columns=["isbn_add_original"])

        return book_info

    def add_tendency(self, tendency, values):
        keys = ["kdc", "isbn1", "isbn2", "isbn3"]
        for key, val in zip(keys, values):
            try:
                if np.isnan(tendency[key].at[0, val]):
                    tendency[key].loc[0, [val]] = 1
                else:
                    tendency[key].loc[0, [val]] += 1
            except:
                pass

    def sub_tendency(self, tendency, values):
        keys = ["kdc", "isbn1", "isbn2", "isbn3"]

        for key, val in zip(keys, values):
            try:
                if np.isnan(tendency[key].at[0, val]):
                    tendency[key].loc[0, [val]] = -1
                else:
                    tendency[key].loc[0, [val]] -= 1
            except:
                pass

    def add_user_tendency_table(self, pk):
        book = pd.DataFrame(Book.objects.filter(pk=pk).values())
        book_info = self.process_book_info(book)
        
        tendency = pd.read_pickle(self.user_pkl_dir)
        self.add_tendency(tendency, book_info.values[0])

        pd.to_pickle(tendency, self.user_pkl_dir)

    def sub_user_tendency_table(self, pk):
        book = pd.DataFrame(Book.objects.filter(pk=pk).values())
        book_info = self.process_book_info(book)
        
        tendency = pd.read_pickle(self.user_pkl_dir)
        self.sub_tendency(tendency, book_info.values[0])

        pd.to_pickle(tendency, self.user_pkl_dir)

    def scaling(self, tendency):
        cols = tendency.columns
        vals = tendency.values.tolist()[0]
        vals = [0 if np.isnan(v) else v for v in vals]

        max_val = np.max(vals)
        min_val = np.min(vals)
        mn = max_val - min_val

        values = [(a - min_val) / (mn) for a in vals]

        return {key: val for key, val in zip(cols, values)}

    def get_user_tendency_score(self):
        tendency = pd.read_pickle(self.user_pkl_dir)
        isbn1 = self.scaling(tendency["isbn1"])
        isbn2 = self.scaling(tendency["isbn2"])
        isbn3 = self.scaling(tendency["isbn3"])
        kdc = self.scaling(tendency["kdc"])

        return kdc, isbn1, isbn2, isbn3

    def get_books_user_tendency_score(self, pk):
        book = pd.DataFrame(Book.objects.filter(pk=pk).values())
        book_info = self.process_book_info(book)

        kdc, isbn1, isbn2, isbn3 = self.get_user_tendency_score()

        score2 = isbn1[book_info.loc[0, "isbn1"]]
        score3 = isbn2[book_info.loc[0, "isbn2"]]
        score4 = isbn3[book_info.loc[0, "isbn3"]]

        try:
            score1 = kdc[book_info.loc[0, "kdc_original"]]
            return (score1 * 0.45 + score2 * 0.05 + score3 * 0.15 + score3 * 0.35)
        except:
            return (score2 * 0.05 + score3 * 0.20 + score3 * 0.75)

    def temp_create_users_info(self):
        users = pd.DataFrame(User.objects.all().values())["id"]

        for idx in tqdm(range(0, len(users.values))):
            isbn_info1 = [str(i) for i in range(0, 10)]
            isbn_info2 = [str(i).zfill(2) for i in range(0, 100)]

            empty_isbn1_table = get_nan_dataframe([0], isbn_info1)
            empty_isbn2_table = get_nan_dataframe([0], isbn_info1)
            empty_isbn3_table = get_nan_dataframe([0], isbn_info2)
            empty_kdc_table = get_nan_dataframe([0], self.kdc_info.values)
            
    #         table = {
    #             "isbn1": empty_isbn1_table,
    #             "isbn2": empty_isbn2_table,
    #             "isbn3": empty_isbn3_table,
    #             "kdc": empty_kdc_table,
    #         }

    #         pk = users.values[idx]
    #         user = User.objects.get(pk=pk)
    #         email = user.email
    #         user_pkl_dir = dir_path + f'/data/users_tendency/{email}_tendency.pkl'

    #         tendency = table

    #         like_books = pd.DataFrame(user.like_books.all().values())
    #         for i in range(0, len(like_books)):
    #                 book = like_books.iloc[[i]]
    #                 book_info = self.process_book_info(book)
    #                 self.add_tendency(tendency, book_info.values[0])

    #         unlike_books = pd.DataFrame(user.unlike_books.all().values())
    #         for i in range(0, len(unlike_books)):
    #                 book = unlike_books.iloc[[i]]
    #                 book_info = self.process_book_info(book)
    #                 self.sub_tendency(tendency, book_info.values[0])

    #         pd.to_pickle(tendency, user_pkl_dir)

class UserUpdateTendency(RecommendBooks):

    def __init__(self):
        self.users = pd.DataFrame(User.objects.all().values())

    def process_book_info(self, dataframe):
        book_info = dataframe[["isbn_add_original", "kdc_original"]]
        book_info["isbn1"] = book_info["isbn_add_original"].apply(set_isbn_add1)
        book_info["isbn2"] = book_info["isbn_add_original"].apply(set_isbn_add2)
        book_info["isbn3"] = book_info["isbn_add_original"].apply(set_isbn_add3)
        book_info = book_info.drop(columns=["isbn_add_original"])

        return book_info

    def add_tendency(self, tendency, values):
        keys = ["kdc", "isbn1", "isbn2", "isbn3"]
        for key, val in zip(keys, values):
            try:
                if np.isnan(tendency[key].at[0, val]):
                    tendency[key].loc[0, [val]] = 1
                else:
                    tendency[key].loc[0, [val]] += 1
            except:
                pass

    def sub_tendency(self, tendency, values):
        keys = ["kdc", "isbn1", "isbn2", "isbn3"]

        for key, val in zip(keys, values):
            try:
                if np.isnan(tendency[key].at[0, val]):
                    tendency[key].loc[0, [val]] = -1
                else:
                    tendency[key].loc[0, [val]] -= 1
            except:
                pass
            
    def create_users_tendency(self):
        users = self.users["id"]
        kdc_info = pd.read_pickle(dir_path + '\\data\\kdc_info.pkl')

        for idx in tqdm(range(0, len(users.values))):
            isbn_info1 = [str(i) for i in range(0, 10)]
            isbn_info2 = [str(i).zfill(2) for i in range(0, 100)]

            empty_isbn1_table = get_nan_dataframe([0], isbn_info1)
            empty_isbn2_table = get_nan_dataframe([0], isbn_info1)
            empty_isbn3_table = get_nan_dataframe([0], isbn_info2)
            empty_kdc_table = get_nan_dataframe([0], kdc_info.values)
            
            table = {
                "isbn1": empty_isbn1_table,
                "isbn2": empty_isbn2_table,
                "isbn3": empty_isbn3_table,
                "kdc": empty_kdc_table,
            }

            pk = users.values[idx]
            user = User.objects.get(pk=pk)
            email = user.email
            user_pkl_dir = dir_path + f'\\data\\users_tendency\\{email}_tendency.pkl'

            tendency = table

            like_books = pd.DataFrame(user.like_books.all().values())
            for i in range(0, len(like_books)):
                    book = like_books.iloc[[i]]
                    book_info = self.process_book_info(book)
                    self.add_tendency(tendency, book_info.values[0])

            unlike_books = pd.DataFrame(user.unlike_books.all().values())
            for i in range(0, len(unlike_books)):
                    book = unlike_books.iloc[[i]]
                    book_info = self.process_book_info(book)
                    self.sub_tendency(tendency, book_info.values[0])

            pd.to_pickle(tendency, user_pkl_dir)

    def create_recommend_list_by_users(self):
        users = self.users["id"]

        for idx in tqdm(range(0, len(users.values))):
            table = {}

            pk = users.values[idx]
            self.user = User.objects.get(pk=pk)
            email = self.user.email
            self.exclude_unliked_books()
            self.like_books = self.get_like_books()
            self.reviews = self.get_review_books()

            user_booklist_dir = dir_path + f'\\data\\users_recommends\\{email}_books.pkl'

            book_ids = self.get_recommend_book_ids()

            table["desc"] = book_ids[0]
            table["title"] = book_ids[1]
            table["review"] = book_ids[2]
            table["others"] = book_ids[3]
            table["genres"] = book_ids[4]

            pd.to_pickle(table, user_booklist_dir)

    
