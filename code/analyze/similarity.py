import os
import re
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
# from collections import Counter

from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

from analyze.connect_db import MysqlController
from eunjeon import Mecab

a = pd.read_pickle("C:\\Users\\dogma\\Desktop\\Program\\specialPJT\\backend\\backend\\backend\\analyze\\data\\users_tendency\\real2@bookridge.com_tendency.pkl")

db = MysqlController()
sql = "SELECT DISTINCT kdc_original FROM books_book"
rows = db.execute(sql)
kdcs = []
for row in rows:
    kdcs.append(row["kdc_original"])

kdc = pd.Series(kdcs)
kdc = kdc[kdc != ""]
kdc.to_pickle("kdc_info.pkl")

sw = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',"hadn't",
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
    'won', "won't", 'wouldn', "wouldn't", '소설', '년'
]

def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

set_config()

loc = "./data/matrix/weight/"
fnames = os.listdir(loc)

DATA_2017 = [f for f in fnames if f.startswith("2017")]
DATA_2018 = [f for f in fnames if f.startswith("2018")]
DATA_2019 = [f for f in fnames if f.startswith("2019")]
DATA_2020 = [f for f in fnames if f.startswith("2020")]

data_2017 = pd.read_pickle(loc + DATA_2017[0])

for f in DATA_2017[1:]:
    d = pd.read_pickle(loc + f)
    data_2017 += d

idx = 0
keys = data_2017.loc[idx].index[20:]
vals = data_2017.loc[idx].values[20:]

sum_series = data_2017.iloc[idx]
key_add2 = sum_series.index[10:20]
val_add2 = sum_series.values[10:20]
key_add3 = sum_series.index[20:]
val_add3 = sum_series.values[20:]

new_series = pd.Series([])
for k2, v2 in zip(key_add2, val_add2):
    for k3, v3 in zip(key_add3, val_add3):
        new_series[k2 + "_" + k3] = v2 + v3

# _max = new_series.max()
# new_series = new_series.apply(lambda x: x/_max)
# info = {key: val for key, val in new_series.items()}

def set_info(new_series):
    arr = []
    for key, val in new_series.items():
        a = (key + " ") * int(val)
        arr.append(a.rstrip())

    return arr

info = set_info(new_series)
# info = {key: round(val) for key, val in zip(keys, vals)}

fig, axs = plt.subplots(ncols=2)

# tf-idf 유사도 측정
tfidf = TfidfVectorizer()
tr1 = tfidf.fit_transform(info)

data_array1 = tr1.toarray()
features1 = tfidf.get_feature_names()
tsne1 = TSNE(n_components=2, n_iter=10000, verbose=1)

Z1 = tsne1.fit_transform(data_array1.T)
# plt.scatter(Z[:,0], Z[:,1])
axs[0].scatter(Z1[:,0], Z1[:,1])
axs[0].set_title(idx)
for i in range(len(features1)):
    axs[0].annotate(s=features1[i].encode("utf8").decode("utf8"), xy=(Z1[i,0], Z1[i,1]))

# counter 유사도 측정
cov = CountVectorizer()
tr2 = cov.fit_transform(info)
data_array2 = tr2.toarray()
features2 = cov.get_feature_names()

tsne2 = TSNE(n_components=2, n_iter=10000, verbose=1)

Z2 = tsne2.fit_transform(data_array2.T)

axs[1].scatter(Z2[:,0], Z2[:,1])
axs[1].set_title(idx)
for i in range(len(features2)):
    axs[1].annotate(s=features2[i].encode("utf8").decode("utf8"), xy=(Z2[i,0], Z2[i,1]))

plt.show()

# http://andrewgaidus.com/Finding_Related_Wikipedia_Articles/


# d = pd.Series(data_array2, index=features2).sort_values(ascending=False)

cov = CountVectorizer()
tr2 = cov.fit_transform([info])
data_array2 = tr2.toarray()
features2 = cov.get_feature_names()
nbrs = NearestNeighbors(n_neighbors=10).fit(tr2)
# new_series.index.get_loc("isbn_add2_3_isbn_add3_82")
# d = pd.Series(data_array2.flatten(), 
#               index = features2).sort_values(ascending=False)

features2.index("isbn_add2_9_isbn_add3_81")
distances, indices = nbrs.kneighbors(tr2.getrow(365))

names_similar = pd.Series(indices.flatten()).map(pd.Series(data=features2))
result = pd.DataFrame({'distance':distances.flatten(), 'name':names_similar})



tfidf = TfidfVectorizer()
tr1 = tfidf.fit_transform(info)

data_array1 = tr1.toarray()
features1 = tfidf.get_feature_names()

wiki_data = pd.read_csv('./analyze/wiki_people.csv', index_col='name')['text']
name = 'Barack Obama'
text = wiki_data[name]
count_vectorizer = TfidfVectorizer()
count_matrix = count_vectorizer.fit_transform([text])
features = count_vectorizer.get_feature_names()
row = wiki_data.index.get_loc(name)
count_matrix.getrow(2).todense()



# DB
mecab = Mecab()

db = MysqlController()
sql = "SELECT * FROM books_book"
rows = db.execute(sql)
books = pd.DataFrame(rows)
# df1 = books[["id", "description"]]
df1 = books[["id", "title"]]
sql2 = "SELECT * FROM accounts_user_like_books WHERE user_id = 40"
# sql2 = "SELECT * FROM accounts_user_like_books"
rows1 = db.execute(sql2)
likes = pd.DataFrame(rows1)

def make_groups_by_user(dataframe):
    # book_id object type으로 변경
    dataframe['book_id'] = dataframe['book_id'].astype(str) 
    # 아이디 별 좋아요 한 책으로 묶기
    return dataframe.groupby(['user_id'], as_index = True).agg({'book_id': ' '.join})

gr = make_groups_by_user(likes)

# 사용자가 좋아요한 책은 제외
df1 = df1[df1["id"].isin(likes["book_id"].values.tolist()) == False]

user_like_desc = ""
for row in rows1:
    sql3 = f"SELECT * FROM books_book WHERE id = {row['book_id']}"
    r = db.execute(sql3)
    try:
        user_like_desc += r[0]["title"]
    except:
        pass

# # 좋아요한 책 1권으로 비교하기
# user_like_desc_list = []
# for row in rows1:
#     sql3 = f"SELECT * FROM books_book WHERE id = {row['book_id']}"
#     r = db.execute(sql3)
#     try:
#         if r[0]["title"]:
#             user_like_desc_list.append(r[0]["title"])
#     except:
#         pass

# html 특수기호 제거
# user_like_desc1 = re.sub('&.*;', "", user_like_desc)
user_like_desc1 = re.sub('&.*;', "", user_like_desc)
comb_title = []
accept_pos = ["NNG", "NNP", "NNB", "VA", "VV", "VX", "VCP", "SL", "SH"]
# https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY/edit#gid=589544265
mecab.pos(user_like_desc1)
for pos in mecab.pos(user_like_desc1):
    if pos[1] in accept_pos:
        comb_title.append(pos[0])

mecab.pos(user_like_desc1)[0]
user_like_desc1 = " ".join(comb_title)


def filter_by_pos(text, accepts=["NNG", "NNP", "NNB", "VA", "VV", "VX", "VCP", "SL", "SH"]):
    temp = []
    for pos in mecab.pos(text):
        if pos[1] in accepts:
            temp.append(pos[0])
    return " ".join(temp)

df1.set_index("id", drop=True, inplace=True)
df1 = df1[df1["title"].isna()==False]
df1["title"] = df1["title"].apply(lambda x: re.sub('&.*;', "", x))
df1["title"] = df1["title"].apply(filter_by_pos)

sw.extend([
    "소설", "년"
])

ser = pd.Series(data=df1["title"].values, index=df1.index)
ser["user"] = user_like_desc1

tfidf = TfidfVectorizer()
matrix = tfidf.fit_transform(ser)
features = tfidf.get_feature_names()
r = ser.index.get_loc("user")
d = pd.Series(matrix.getrow(r).toarray().flatten(), index = features).sort_values(ascending=False)

# tf-idf 로 중요하게 생각하는 단어 10 확인하기
ax = d[:10].plot(kind='bar', figsize=(10,6), width=.8, fontsize=14, rot=45,
            title='User Important 10 Keyword')

ax.title.set_size(18)
plt.show()


ger = pd.Series(data=gr["book_id"].values, index=gr.index)
counter = CountVectorizer(stop_words=sw)
# ct_matrix = counter.fit_transform(ser)
ct_matrix = counter.fit_transform(ser)
features = counter.get_feature_names()

print(ct_matrix.toarray())
# 코사인 유사도 -> 벡터의 크기가 중요하지 않을 때.
# 벡터의 크기가 중요하면, euclidean 거리로 계산
cosine_similarity(ct_matrix.toarray())
counter.get_stop_words()

r = ser.index.get_loc("user")
d1 = pd.Series(ct_matrix.getrow(r).toarray().flatten(), index = features).sort_values(ascending=False)

ax = d1[:20].plot(kind='bar', figsize=(10,6), width=.8, fontsize=14, rot=45,
            title='User Important 10 Keyword')

ax.title.set_size(18)
plt.show()

# tfidf
nbrs = NearestNeighbors(n_neighbors=30).fit(matrix)
row = ser.index.get_loc("user")
distances, indices = nbrs.kneighbors(matrix.getrow(row))
names_similar = pd.Series(indices.flatten()).map(ser.reset_index()['id'])
result = pd.DataFrame({'distance':distances.flatten(), 'name':names_similar})
result

# count
nbrs = NearestNeighbors(n_neighbors=20).fit(ct_matrix)
row = ser.index.get_loc("user")
distances, indices = nbrs.kneighbors(ct_matrix.getrow(row))
names_similar = pd.Series(indices.flatten()).map(ser.reset_index()['id'])
result = pd.DataFrame({'distance':distances.flatten(), 'name':names_similar})
result


knn = KNeighborsClassifier(n_neighbors=100).fit(ct_matrix.toarray(), ger.index)
d, i = knn.kneighbors(ct_matrix.toarray()[2].reshape(1, -1))
names_similar = pd.Series(i.flatten()).map(ger.reset_index()['user_id'])
result = pd.DataFrame({'distance':d.flatten(), 'name':names_similar})
result
# 줄거리로 클러스트링 묶어보기
likes_books = books[books["id"].isin(likes["book_id"].values.tolist())]
lb = likes_books[["id", "isbn_add_original", "description"]]

# 검증
test_data: pd.Series = pd.read_pickle('preprocessed_books_title.pkl')
# test_data[test_data.str.contains("설국")]
test_data.index.name = "book_id"
test_data["user"] = user_like_desc1
row = test_data.index.get_loc("user")

test_data.iloc[1]
counter = CountVectorizer(stop_words=sw)
matrix = counter.fit_transform(test_data)
features = counter.get_feature_names()

val = counter.vocabulary_.values()
key = counter.vocabulary_.keys()
new_voc = {}
for k, v in zip(key, val):
    new_voc[v] = k

tfid = TfidfVectorizer(stop_words=sw)
matrix = tfid.fit_transform(test_data)
features = counter.get_feature_names()
# counter.vocabulary_

# (minkowski , euclidean, cosine, manhattan)
nbrs = NearestNeighbors(n_neighbors=51).fit(matrix)
print(matrix.getrow(row))
distances, indices = nbrs.kneighbors(matrix.getrow(row))
print(matrix[2])
new_voc[14245]
print(matrix.getrow(21698))
idx = test_data.index.get_loc(21698)
test_data.iloc[19265]

test_data[21698]
td = test_data.reset_index()
td.iloc[indices.flatten()[1:]]["book_id"].values[0]

test_data: pd.Series = pd.read_pickle('preprocessed_books_title.pkl')
# test_data[test_data.str.contains("설국")]
test_data.index.name = "book_id"
loc = test_data.index[-1] + 1
test_data[test_data.index[-1] + 1] = user_like_desc1
row = test_data.index.get_loc("user")

counter = CountVectorizer(stop_words=sw)
matrix = counter.fit_transform(test_data)
features = counter.get_feature_names()

knn = KNeighborsClassifier(n_neighbors=20).fit(matrix.toarray(), test_data.index)
d, i = knn.kneighbors(matrix.toarray()[row].reshape(1, -1))
# d = pd.Series(matrix.getrow(row).toarray().flatten(), index = features).sort_values(ascending=False)

# ax = d[:10].plot(kind='bar', title='Barack Obama Wikipedia Article Word TF-IDF Values',
#             figsize=(10,6), width=.8, fontsize=14, rot=45 )
# ax.title.set_size(20)
# plt.show()