import json

with open("./data/libcode/libcode.json", "r", encoding="utf-8") as f:
    data = json.load(f)

codes = data["code"]
cities = data["city"]
gus = data["gu"]

lib_list = []

pk = 0
for code, city, gu in zip(codes, cities, gus):
    pk += 1
    info = {
        "pk": pk,
        "model": "libraries.librarylocation",
        "fields": {}
    }

    f = info["fields"]

    

