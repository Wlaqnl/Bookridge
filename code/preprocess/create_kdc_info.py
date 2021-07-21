import json

with open('./data/isbn_add/kdc.json', encoding="utf-8") as f:
    data = json.loads(f.read())

kdc_list = []
pk = 0

for idx in range(0, 1000):
    pk += 1
    info = {
        "pk": pk,
        "model": "books.kdc",
        "fields": {}
    }

    f = info["fields"]
    
    key = str(idx).zfill(3)
    f["num"] = key
    f["desc"] = data.get(key, None)

    kdc_list.append(info)

# kdc info 만들기
with open("./data/isbn_add/kdc_info.json", 'w', encoding="utf-8") as f:
    json.dump(kdc_list, f)


# books_kdc 테이블의 pk 정보 만들기
kdc_pk_info = {}
for idx in range(0, 1000):
    key = str(idx).zfill(3)
    kdc_pk_info[key] = idx + 1

with open("./data/isbn_add/kdc_pk_info.json", 'w', encoding="utf-8") as f:
    json.dump(kdc_pk_info, f)