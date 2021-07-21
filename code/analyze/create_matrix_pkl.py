'''
isbn 매트릭스 생성
'''

import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm

from .utils import *

# from analyze.connect_db import MysqlController

ALL_2020 = "./data/popular/"
ALL_2020_DATA = os.listdir(ALL_2020)

with open("./data/isbn_add/isbn_pk_info.json", "r", encoding="utf-8") as f:
    isbn_pk_info = json.load(f)

# http://www.booktrade.or.kr/kdc/kdc.jsp
with open("./data/isbn_add/kdc.json", "r", encoding="utf-8") as f:
    kdc_info = json.load(f)

def get_nan_dataframe(x, y):
    nan_data = np.empty((len(x), len(y)))
    nan_data[:] = np.NaN
    return pd.DataFrame(
                data=nan_data,
                index=x,
                columns=y
            )

def get_filled_dataframe_sgd(nan_df, dataframe, weight_info):
    for d in dataframe.values:
        # d[0] = age_gender
        # d[1] = isbn_add
        # d[2] = ranking

        if d[1]:
            if np.isnan(nan_df.at[d[0], d[1]]):
                nan_df.at[d[0], d[1]] = float(weight_info[d[2]])
            else:
                nan_df.at[d[0], d[1]] += float(weight_info[d[2]])

    return nan_df.astype(pd.SparseDtype("float", np.nan))

def create_popular_book_sdf(dataframe, to="isbn"):
    index = get_gender_age_index(dataframe)
    weight_info = get_ranking_weight(dataframe)

    nan_df1 = get_nan_dataframe(index, isbn_pk_info["isbn_add1"].keys())
    nan_df2 = get_nan_dataframe(index, isbn_pk_info["isbn_add2"].keys())

    if to == "isbn":
        nan_df3 = get_nan_dataframe(index, isbn_pk_info["isbn_add3"].keys())
    else:
        nan_df3 = get_nan_dataframe(index, kdc_info.keys())

    # addition_symbol = isbn 부가기호
    new_df = dataframe.loc[:, ["age", "gender", "ranking", "addition_symbol"]]
    new_df2 = dataframe.loc[:, ["age", "gender", "ranking", "class_no"]]

    new_df["age_gender"] = new_df.apply(set_gender_age_column, axis=1)
    new_df2["age_gender"] = new_df2.apply(set_gender_age_column, axis=1)
    
    # 장르를 확인하기 위해 isbn 부가기호의 3, 4번째 숫자만 사용
    new_df["isbn_add1"] = new_df["addition_symbol"].apply(set_isbn_add1)
    new_df["isbn_add2"] = new_df["addition_symbol"].apply(set_isbn_add2)

    if to == "isbn":
        new_df["isbn_add3"] = new_df["addition_symbol"].apply(set_isbn_add3)
    else:
        new_df2 = nan_to_none(new_df2)
        new_df2["class_no"] = new_df2["class_no"].apply(set_kdc_type)
    
    df1 = new_df[["age_gender", "isbn_add1", "ranking"]]
    df2 = new_df[["age_gender", "isbn_add2", "ranking"]]
    if to == "isbn":
        df3 = new_df[["age_gender", "isbn_add3", "ranking"]]
    else:
        df3 = new_df2[["age_gender", "class_no", "ranking"]]

    sgd1 = get_filled_dataframe_sgd(nan_df1, df1, weight_info)
    sgd2 = get_filled_dataframe_sgd(nan_df2, df2, weight_info)
    sgd3 = get_filled_dataframe_sgd(nan_df3, df3, weight_info)

    return {"isbn1_sgd": sgd1, "isbn2_sgd": sgd2, "isbn3_sgd": sgd3}

def dump_dataframes(dataframes, url):
    pd.to_pickle(dataframes, url)


# create kdc pkl
for idx in tqdm(range(len(ALL_2020_DATA))):
    fname = ALL_2020_DATA[idx]
    sample = json_to_dataframe(ALL_2020 + fname)
    sdf = create_popular_book_sdf(sample, to="kdc")
    dump_dataframes(sdf, "./data/matrix/kdc/" + fname.split(".json")[0] + "_kdc.pkl")

# create isbn pkl
for idx in tqdm(range(len(ALL_2020_DATA))):
    fname = ALL_2020_DATA[idx]
    sample = json_to_dataframe(ALL_2020 + fname)
    sdf = create_popular_book_sdf(sample)
    dump_dataframes(sdf, "./data/matrix/isbn/" + fname.split(".json")[0] + "_isbn.pkl")

