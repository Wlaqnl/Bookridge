import pandas as pd
import numpy as np
from datetime import datetime as dt
import json
import pyspark
import requests


API_KYE = "13721f2ab86e1affdbacc602b942bcd1f1170b8906c10a6f67acc886b6145615"
BASE_URL = f"http://seoji.nl.go.kr/landingPage/SearchApi.do?cert_key={API_KYE}&result_style=json&page_no=1&page_size=10&isbn="

req = requests.get(BASE_URL + "9788926389362")
req.json()

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

ALL_2019 = "./data/2019전국/"
LOCATION = "./data/지역별/"

df = json_to_dataframe(ALL_2019 + '2019년_01월_1주_전국.json')

# object 타입을 datetime 으로 변경해주기
def object_to_datetime(dataframe, column):
    # dtype: datetime64[ns]
    return pd.to_datetime(dataframe[column], format="%Y-%m-%d", errors='raise')

df["start_date"] = object_to_datetime(df, "start_date")
df["end_date"] = object_to_datetime(df, "end_date")
isbn = set(df["isbn13"].values.tolist())
isbn = pd.Series(list(isbn))

df.columns
df.loc[2]

df["gender"].value_counts()

def dataframe_to_db_data(dataframe):
    pass