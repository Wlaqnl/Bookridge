import os
import pandas as pd
import numpy as np
from datetime import datetime as dt
import json
from pprint import pprint
from tqdm import tqdm
from preprocess.connect_db import MysqlController

tqdm.pandas()

with open('./data/isbn_add/kdc.json', 'r', encoding='utf-8') as f:
    kdc = json.load(f)

POPULAR = "./data/popular/"
POPULAR_DATA = os.listdir(POPULAR)

db = MysqlController()

def json_to_dataframe(data_path):
    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())

        d = {}
        columns = data["data"].keys()

        for c in columns:
            d[c] = data["data"][c].values()

        return pd.DataFrame.from_dict(d)
    except FileNotFoundError as e:
        print(f"{data_path} 파일 없음")
        raise e

def nan_to_none(dataframe):
    """
    np.nan 타입을 None 으로 변경해줌
    """
    return dataframe.where(pd.notnull(dataframe), None)

def object_to_datetime(dataframe, column):
    """
    datetime dtype으로 변경
    """
    # dtype: datetime64[ns]
    return pd.to_datetime(dataframe[column], format="%Y-%m-%d", errors='raise')

def set_gender(gender):
    if gender == "남성":
        return 0
    elif gender == "여성":
        return 1
    else:
        return 2

def set_datetime_format(date):
    d = str(date).split("T")
    return d[0].split(" ")[0]

def set_loan_count_type(count):
    cnt = count.replace(",", "")
    return int(cnt)

def get_book_pk_from_db(dataframe, unique_dataframe, desc):
    dataframe["book"] = None
    isbn_list = unique_dataframe["isbn"].values
    
    for idx in tqdm(range(0, len(isbn_list)), desc=desc):
        isbn = isbn_list[idx]
        sql = f"SELECT id FROM books_book WHERE isbn='{isbn_list[idx]}'"
        rows = db.search(sql)

        if rows:
            for idx in dataframe[dataframe["isbn"] == isbn]["book"].index:
                dataframe.loc[idx, "book"] = rows[0]["id"]
    return dataframe

def adjust_columns(dataframe):
    cols = [
        "gender", "age", "ranking", "start_date", "end_date",
        "loan_count", "region", "isbn"
    ]
    return dataframe.loc[:, cols]

def organize_popular_book_columns(dataframe, unique_dataframe, desc=""):

    new_df = adjust_columns(dataframe)
    new_df["gender"] = new_df["gender"].apply(set_gender)
    new_df["loan_count"] = new_df["loan_count"].apply(set_loan_count_type)
    new_df["start_date"] = object_to_datetime(dataframe, "start_date")
    new_df["end_date"] = object_to_datetime(dataframe, "end_date")
    new_df["start_date"] = new_df["start_date"].apply(set_datetime_format)
    new_df["end_date"] = new_df["end_date"].apply(set_datetime_format)

    new_df = get_book_pk_from_db(new_df, unique_dataframe, desc)

    new_df = new_df.rename(columns={"loan_count": "rent_count", "region": "location"})
    new_df = new_df.drop(columns=["isbn"])

    return nan_to_none(new_df)

def book_dataframe_to_json_list(dataframe, desc=""):
    # 테이블에 마지막 id 정보 가져오기
    # rows = db.search("SELECT id FROM books_popularbook ORDER BY id DESC LIMIT 1")
    # if rows:
    #     pk = rows[0]["id"]
    # else:
    #     pk = 0

    indexes = list(dataframe.index)
    columns = list(dataframe.columns)

    books = []

    for i in tqdm(range(0, len(indexes)), desc):
        f = {}
        # pk += 1
        f["pk"] = None
        f["model"] = "books.popularbook"
        f["fields"] = {}

        fi = f["fields"]
        d = dataframe.loc[indexes[i]]

        for c in columns:
            fi[c] = d[c]

        books.append(f)

    return books

class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32) or isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.datetime64): 
            return str(obj)

        return json.JSONEncoder.default(self, obj)

def create_json_file(jsondata, url):
    with open(url, "w", encoding="utf-8") as f:
        json.dump(jsondata, f, cls=npEncoder)

for popular_data in POPULAR_DATA:
    # popular_data = POPULAR_DATA[0]

    sample = json_to_dataframe(POPULAR + popular_data)
    sample = sample.rename(columns={"isbn13": "isbn", "addition_symbol": "isbn_add"})
    fname = popular_data.split(".")[0]

    sample = sample[sample["class_no"].isna() == False]
    sample = sample[sample["isbn_add"].isna() == False]
    
    sample_df = nan_to_none(sample)

    unique_df = sample_df.drop_duplicates(subset=['isbn'], keep="first")

    desc = fname.split("인기도서")[0] + "pk"
    df = organize_popular_book_columns(sample_df, unique_df, desc)
    df.columns

    jsondata = book_dataframe_to_json_list(df, fname)
    create_json_file(jsondata, f'./data/books/db/popular/{fname}_popular_db.json')

    backend_dir = "C:/Users/moo/Desktop/program/specialPJT/s03p23d103/backend/backend/"
    backend_dir_json_fname = f'{backend_dir}{fname}_popular_db.json'
    create_json_file(jsondata, backend_dir_json_fname)

    print("insert data ...")
    os.system(f"python {backend_dir}manage.py loaddata -v 3 {backend_dir_json_fname}")
    print("Done!\n")

