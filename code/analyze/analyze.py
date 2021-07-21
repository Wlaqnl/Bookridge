import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# ISBN 부가기호 상관성 분석하기
ALL_2020 = "./data/popular/"
ALL_2020_DATA = os.listdir(ALL_2020)

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

def rename_columns(dataframe, prefix=""):
    origin_cols = dataframe.columns.tolist()
    origin_cols.pop(0)
    re_cols = {col: prefix + col for col in origin_cols}
    return dataframe.rename(columns=re_cols)

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

def nomarlize(arr):
    max_val = max(arr)
    min_val = min(arr)
    mn = max_val - min_val
    return [(a - min_val) / (mn) for a in arr]

def get_ranking_weight(dataframe, max_rank=0):
    """
    ranking 에 따라 가중치를 주기 위해서 만듬\n
    가중치 점수는 `minmax_scale` 로 0 ~ 1 사이로 바꿈
    """
    ranking = sorted(dataframe["ranking"].unique().tolist(), key=lambda x: int(x))
    if max_rank == 0:
        max_rank = int(max(ranking))
        
    weights = [max_rank / int(rank) for rank in ranking]
    normalize_weights = nomarlize(weights)

    weight_info = {}

    for key, val in zip(ranking, normalize_weights):
        weight_info[key] = val

    return weight_info

def set_ranking_weight(dataframe):
    weight_info = get_ranking_weight(dataframe)
    return [weight_info[rank] for rank in dataframe["ranking"].values]

# fname = ALL_2020_DATA[0]
# sample = json_to_dataframe(ALL_2020 + fname)
# df = get_processed_dataframe(sample)

# # kido_boy = df[df["age_gender"] == "8~13세_남성"]
# dummies1 = get_dummies(df["isbn_add1"], "add1")
# dummies2 = get_dummies(df["isbn_add2"], "add2")
# dummies3 = get_dummies(df["isbn_add3"], "add3")


# new_df = pd.concat((df[["age_gender", "ranking"]], dummies1, dummies2, dummies3), axis=1)
# new_df["weight"] = set_ranking_weight(new_df)
# new_df = new_df.drop(columns=["ranking"])

# # adds = [
# #     "add1_0", "add1_1", "add1_4", "add1_6", "add1_7",
# #     "add2_0", "add2_2", "add2_3", "add2_4", "add2_6", 
# #     "add2_7"
# # ]

# for idx in tqdm(range(0, len(new_df.index))):
#     values = new_df.iloc[idx].values.tolist()
#     weight = float(values[-1])
#     w = [weight * val for val in new_df.iloc[idx].values.tolist()[1:-1]]
#     new_df.iloc[idx] = [new_df.iloc[idx].values.tolist()[0]] + w + [weight]

# kido = new_df[new_df["age_gender"] == "8~13세_남성"]

new_df = pd.read_pickle('./data/matrix/processed/sample.pkl')
kido = new_df[new_df["age_gender"] == "8~13세_남성"].drop(columns=["age_gender", "weight"])

weight = [(key, val) for key, val in zip(kido.columns, kido.sum().values)]
weight.sort(key=lambda x: x[1], reverse=True)



dcs_tree = DecisionTreeClassifier(max_depth=5)
enc = LabelEncoder()
enc.fit(new_df["age_gender"].values)
y_enc = enc.transform(new_df["age_gender"].values)
# enc.classes_

new_df = new_df.drop(columns=["weight"])
x = new_df.drop(columns=["age_gender"]).values
dcs_tree.fit(x, y_enc)

# new_df.to_pickle('./data/matrix/processed/sample.pkl')
# new_df.drop(columns=["weight"]).corr(method="pearson")