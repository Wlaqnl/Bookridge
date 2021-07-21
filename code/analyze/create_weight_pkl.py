'''
isbn 가중치 생성
'''

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from .utils import *

ALL_2020 = "./data/popular/"
ALL_2020_DATA = os.listdir(ALL_2020)

def set_gender_age_column(dataframe):
    return dataframe["age"] + "_" + dataframe["gender"]

def get_processed_dataframe(dataframe):
    new_df = dataframe[["age", "gender", "ranking", "addition_symbol"]]

    new_df["age_gender"] = new_df.apply(set_gender_age_column, axis=1)
    new_df["isbn_add1"] = new_df["addition_symbol"].apply(set_isbn_add1)
    new_df["isbn_add2"] = new_df["addition_symbol"].apply(set_isbn_add2)
    new_df["isbn_add3"] = new_df["addition_symbol"].apply(set_isbn_add3)

    return new_df[["age_gender", "ranking", "isbn_add1", "isbn_add2", "isbn_add3"]]

def get_dummies(series, prefix):
    return pd.get_dummies(series, prefix=prefix, dtype=float)

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

def fill_nan_dataframe(nan_dataframe, dataframe):
    isbn_info = dataframe.drop(columns=["ranking"]).values

    for idx in tqdm(range(0, len(isbn_info))):
        info = isbn_info[idx]

        # index = info[0]
        a1 = "isbn_add1_"+info[1]
        a2 = "isbn_add2_"+info[2]
        a3 = "isbn_add3_"+info[3]
        w = info[4]

        iloc = nan_dataframe.iloc[idx]
        
        b1 = iloc[a1] 
        b2 = iloc[a2]
        b3 = iloc[a2] 

        iloc[a1] = w if np.isnan(b1) else b1 + w
        iloc[a2] = w if np.isnan(b2) else b2 + w
        iloc[a3] = w if np.isnan(b3) else b3 + w

    return nan_dataframe


def set_ranking_weight():
    pass

def nomarlize(arr):
    max_val = max(arr)
    min_val = min(arr)
    mn = max_val - min_val
    return [(a - min_val) / (mn) for a in arr]

def get_ranking_weight():
    """
    ranking 에 따라 가중치를 주기 위해서 만듬\n
    (max=1000)가중치 점수는 `minmax_scale` 로 0 ~ 1 사이로 바꿈
    """
    ranking = [str(i) for i in range(1000, 0, -1)]
    max_rank = 1000
        
    weights = [max_rank / int(rank) for rank in ranking]
    normalize_weights = nomarlize(weights)

    weight_info = {}

    for key, val in zip(ranking, normalize_weights):
        weight_info[key] = val

    return weight_info

def get_weight_series(ranking):
    weight_info = get_ranking_weight()
    return pd.Series([weight_info[rank] for rank in ranking])

sorter1 = [
    '8~13세_남성', '8~13세_여성', '14~19세_남성', '14~19세_여성', '20대_남성',
    '20대_여성', '30대_남성', '30대_여성', '40대_남성', '40대_여성',
    '50대_남성', '50대_여성', '60세 이상_남성', '60세 이상_여성'
]


# for data in ALL_2020_DATA:
#     fname = data.split(".")[0]

#     sample = json_to_dataframe(ALL_2020 + data)
#     sample = sample[(sample["isbn13"].isna() == False) & (sample["addition_symbol"].isna() == False) & (sample["class_no"].isna() == False)]
#     df = get_processed_dataframe(sample)

#     # age_gender 로 sort 하기 위해 type을 categry로 변경
#     df["age_gender"] = df["age_gender"].astype("category")
#     # category 의 우선순위를 sorter1 의 변수 순서로 설정
#     df["age_gender"].cat.set_categories(sorter1, inplace=True)
#     # 정렬을 위해 임시 컬럼생성. rank 타입이 obejct 라서 int 타입으로 바꿔줌.
#     df["temp_rank"] = df["ranking"].astype("int64")
#     # age_gender 와 ranking 순으로 정렬함
#     df = df.sort_values(["age_gender", "temp_rank"])
#     # 임시 컬럼 삭제
#     df = df.drop(columns=["temp_rank"])

#     df["weight"] = get_weight_series(df["ranking"]).values

#     x = df["age_gender"]
#     y = get_isbn_columns()
#     nan_df = get_nan_dataframe(x, y)

#     filled = fill_nan_dataframe(nan_df, df)

#     weighted_df = filled.groupby("age_gender").sum()

#     pd.to_pickle(weighted_df, f"./data/matrix/weight/{fname}.pkl")

loc = "./data/matrix/weight/"
fnames = os.listdir(loc)

data = pd.read_pickle(loc + fnames[0])
for f in fnames[1:]:
    d = pd.read_pickle(loc + f)
    data += d

for idx in data.index:
    norm = np.nansum(data.loc[idx].values)
    data.loc[idx] = data.loc[idx].apply(lambda x: x/norm)

# pd.to_pickle(data, './weight_info.pkl')

# dd = pd.read_pickle("./data/weight_info.pkl")
# weight = dd.loc["60세 이상_여성"]

# arr = sorted([(idx, val) for idx, val in zip(weight.index, weight.values)], key=lambda x: x[1], reverse=True)
# arr1 = [(a[0].split("isbn_add1/")[1], a[1]) for a in arr if a[0].startswith("isbn_add1")]
# arr2 = [(a[0].split("isbn_add2/")[1], a[1]) for a in arr if a[0].startswith("isbn_add2")]
# arr3 = [(a[0].split("isbn_add3/")[1], a[1]) for a in arr if a[0].startswith("isbn_add3")]

# info = {
#     1: arr1,
#     2: arr2,
#     3: arr3
# }