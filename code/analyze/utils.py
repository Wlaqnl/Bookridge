import os
from datetime import datetime as dt
import json
from pprint import pprint
import pandas as pd
import numpy as np
from tqdm import tqdm

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

def get_gender_age_index(dataframe):
    age_list = dataframe["age"].unique().tolist()
    gender_list = dataframe["gender"].unique().tolist()

    age_gender_list = []

    for a in age_list:
        for g in gender_list:
            age_gender_list.append(a + "_" + g)

    return age_gender_list

def set_gender_age_column(dataframe):
    return dataframe["age"] + "_" + dataframe["gender"]

def get_kdc_info():
    with open("./data/isbn_add/kdc.json", "r", encoding="utf-8") as f:
        kdc_info = json.load(f)
    return kdc_info

def nomarlize(arr):
    max_val = max(arr)
    min_val = min(arr)
    mn = max_val - min_val
    return [(a - min_val) / (mn) for a in arr]

def get_ranking_weight(dataframe):
    """
    ranking 에 따라 가중치를 주기 위해서 만듬\n
    가중치 점수는 `minmax_scale` 로 0 ~ 1 사이로 바꿈
    """
    ranking = sorted(dataframe["ranking"].unique().tolist(), key=lambda x: int(x))
    max_rank = int(max(ranking))
    weights = [max_rank / int(rank) for rank in ranking]
    normalize_weights = nomarlize(weights)

    weight_info = {}

    for key, val in zip(ranking, normalize_weights):
        weight_info[key] = val

    return weight_info

def set_isbn_add1(isbn_add, isna=0):
    
    if isbn_add:
        if len(isbn_add) == 4:
            return "0"
        elif len(isbn_add) == 5:
            return isbn_add[0]
        else:
            return isna
    else:
        return isna

def set_isbn_add2(isbn_add, isna=0):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_add[0]
        elif len(isbn_add) == 5:
            return isbn_add[1]
        else:
            return isna
    else:
        return isna

def set_isbn_add3(isbn_add, isna=0):

    if isbn_add:
        if len(isbn_add) == 4:
            return isbn_add[1:3]
        elif len(isbn_add) == 5:
            return isbn_add[2:4]
        else:
            return isna
    else:
        return isna

def set_kdc_type(kdc):
    if kdc:
        return str(int(float(kdc))).zfill(3)
    return kdc