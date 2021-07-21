import os
import pandas as pd
import numpy as np
from datetime import datetime as dt
from tqdm import tqdm
import json
from pprint import pprint

from preprocess.connect_db import MysqlController

db = MysqlController()

df = pd.read_pickle('./data/books/books.pkl')

df = df[df["isbn_add"].isna() == False]

df = df.drop_duplicates(subset=['isbn'], keep="first")

def set_isbn_add(isbn_add):
    if isbn_add:
        if len(isbn_add) == 4:
            return "0" + isbn_add
        elif len(isbn_add) == 5:
            return isbn_add
        else:
            return None
    else:
        return None

df = df[df["isbn_add"].str.len() > 3]

df["isbn_add"] = df["isbn_add"].apply(set_isbn_add)
df = df[df["isbn_add"].isna() == False]
df["isbn_add"]
select_sql = f"SELECT isbn FROM books_book"
rows = db.search(select_sql)

for idx in tqdm(range(len(rows))):
    r = rows[idx]
    isbn = r['isbn']
    isbn_add = df[df["isbn"] == isbn]["isbn_add"].values[0]
    update_sql = f"UPDATE books_book SET isbn_add_original = {isbn_add} WHERE isbn = {isbn}"
    db.search(update_sql)

db.commit()
db.disconnect()