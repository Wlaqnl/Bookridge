import os
import pandas as pd
import numpy as np
from datetime import datetime as dt
from tqdm import tqdm
import json
from pprint import pprint

# from connect_db import MysqlController

tqdm.pandas()

POPULAR = "./data/popular/"
POPULAR_DATA = os.listdir(POPULAR)
LOCATION = "./data/지역별/"

# rows = db.search("SELECT id FROM books_isbnadd1 ORDER BY id DESC LIMIT 1")
# isbn_add 테이블에 대한 pk 정보
with open("./data/isbn_add/isbn_pk_info.json", "r", encoding="utf-8") as f:
    isbn_pk_info = json.load(f)

with open("./data/isbn_add/kdc_pk_info.json", "r", encoding="utf-8") as f:
    kdc_pk_info = json.load(f)

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

# isbn 부가기호가 제대로 들어오지 않은 것들이 존재한다.
def set_isbn_add1_pk(isbn_add):
    
    if isbn_add:
        if len(isbn_add) == 4:
            return 1
        elif len(isbn_add) == 5:
            return isbn_pk_info["isbn_add1"][isbn_add[0]]
        else:
            return None
    else:
        return None

def set_isbn_add2_pk(isbn_add):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_pk_info["isbn_add2"][isbn_add[0]]
        elif len(isbn_add) == 5:
            return isbn_pk_info["isbn_add2"][isbn_add[1]]
        else:
            return None
    else:
        return None

def set_isbn_add3_pk(isbn_add):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_pk_info["isbn_add3"][isbn_add[1:3]]
        elif len(isbn_add) == 5:
            return isbn_pk_info["isbn_add3"][isbn_add[2:4]]
        else:
            return None
    else:
        return None

def set_kdc_type(kdc):
    if kdc:
        # kdc pk 값을 리턴하기
        key = str(int(float(kdc))).zfill(3)
        return kdc_pk_info[key]
    return kdc

def organize_book_columns(dataframe):
    """
    인기 도서 데이터 와 전체 도서 목록 데이터를 merge 시키면 다음과 같은 컬럼이 나옴.\n
    `['seq', 'isbn', 'vol_x', 'title', 'author', 'publisher_x',\n
    'pub_date', 'isbn_add', 'price', 'img_url', 'description']` \n
    \+ `['no', 'ranking','bookname', 'authors', 'publisher_y', 'publication_year',\n
    'isbn13','addition_symbol', 'vol_y', 'class_no', 'loan_count', 'bookImageURL',\n
    'gender', 'age', 'region', 'addCode1', 'start_date', 'end_date',\n
    'addCode2', 'addCode3', 'addCode34', 'kdc']`\n\n

    DB 정보에 맡게 컬럼을 변경해 줄 것.\n
    """
    # db_columns = [
    #     'title', 'author', 'publisher', 'vol', 'pub_date', 
    #     'isbn', 'price', 'img_url', 'description', 'isbn_add1',
    #     'isbn_add2', 'isbn_add3'
    # ]
    
    cols = [
        "title", "author", "publisher_x", "vol_x", "pub_date", "isbn",
        "price", "img_url", "description", "class_no", "isbn_add"
    ]
    new_df = dataframe.loc[:, cols]

    new_df["isbn_add1"] = new_df["isbn_add"].apply(set_isbn_add1_pk)
    new_df["isbn_add2"] = new_df["isbn_add"].apply(set_isbn_add2_pk)
    new_df["isbn_add3"] = new_df["isbn_add"].apply(set_isbn_add3_pk)
    new_df["class_no"] = new_df["class_no"].apply(set_kdc_type)

    new_df = new_df.drop(columns=["isbn_add"])
    
    new_df = new_df.rename(columns={"publisher_x": "publisher", "vol_x": "vol", "isbn_add": "isbn", "class_no": "kdc"})

    return nan_to_none(new_df)

def kill_sleeping_process():
    db = MysqlController()
    rows = db.search("select id from information_schema.processlist where Command='Sleep';")
    for row in rows:
        db.search(f"KILL {row['id']};")

def check_book_data_exist(db, isbn):
    rows = db.search(f"SELECT id FROM books_book WHERE isbn = {isbn}")
    if len(rows) > 0:
        return False
    return True

def book_dataframe_to_json_list(dataframe, desc=""):
    # books_book 테이블에 마지막 id 정보 가져오기
    # rows = db.search("SELECT id FROM books_book ORDER BY id DESC LIMIT 1;")
    
    # if len(rows) > 0:
    #     pk = rows[0]["id"]
    # else:
    #     pk = 0
    # pk 를 None 으로 주는 것이 더 좋다.
    indexes = list(dataframe.index)
    columns = list(dataframe.columns)

    books = []
    db = MysqlController()
    for i in tqdm(range(0, len(indexes)), desc=desc):
        d = dataframe.loc[indexes[i]]
        # books_book 테이블에 도서정보가 있으면 패스

        if check_book_data_exist(db, d["isbn"]):
            f = {}
            # pk를 None 으로 하면, DB 에 저장될 때 알아서 primary key 가 부여된다.
            f["pk"] = None
            f["model"] = "books.book"
            f["fields"] = {}

            fi = f["fields"]

            for c in columns:
                fi[c] = d[c]
            
            books.append(f)
            
    db.disconnect()
    return books

class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32):
            return int(obj)

        if isinstance(obj, np.int64):
            return int(obj)
        
        return json.JSONEncoder.default(self, obj)

def create_json_file(jsondata, url):
    with open(url, "w", encoding="utf-8") as f:
        json.dump(jsondata, f, cls=npEncoder)

# 도서 전체 데이터 가져오기
df = pd.read_pickle('./data/books/books.pkl')

for popular_data in POPULAR_DATA:
    # popular_data = POPULAR_DATA[0]
    sample = json_to_dataframe(POPULAR + popular_data)
    fname = popular_data.split(".")[0]

    # ISBN 정보로 두 dataframe 묶기
    sample_df = pd.merge(
        df, sample, left_on="isbn", right_on="isbn13"
    )

    # Nan to None
    sample_df = nan_to_none(sample_df)

    # 곂치는 데이터 삭제시키기
    sample_df = sample_df.drop_duplicates(subset=['isbn'], keep="first")
    # kdc 정보 없는 것 삭제
    sample_df = sample_df[sample_df["class_no"].isna() == False]
    # isbn_add 정보 없는 것 삭제
    sample_df = sample_df[sample_df["isbn_add"].isna() == False]

    jsondata = book_dataframe_to_json_list(organize_book_columns(sample_df), fname)

    create_json_file(jsondata, f'./data/books/db/{fname}_db.json')

    backend_dir = "C:/Users/dogma/Desktop/Program/specialPJT/s03p23d103/backend/backend/"
    backend_dir_json_fname = f'{backend_dir}{fname}_db.json'
    create_json_file(jsondata, backend_dir_json_fname)
    print("insert data ...")
    os.system(f"python {backend_dir}manage.py loaddata -v 3 {backend_dir_json_fname}")
    print("Done!\n")

