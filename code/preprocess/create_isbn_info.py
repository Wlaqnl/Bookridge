import json

isbn1_target = ["교양", "실용", "여성", "예비번호", "청소년", "학습참고서1(중.고교용)", "학습참고서2(초등학생용)", "아동", "예비번호", "전문"]
isbn1_desc = [
    "일반 독자층을 대상으로 한 것으로, 주로 전문적인 내용을 비전공 일반 독자들이 쉽게 알아볼 수 있도록 풀어쓴 교양 도서",
    "일반인을 대상으로 한, 어떤 목적을 가진 수험서적",
    "여성을 대상으로 한 도서",
    "예비번호",
    "중∙고등 학습 참고서에 해당되지 않는 것으로 중∙고등학생을 대상으로 한 도서",
    "중∙고등학생을 대상으로 한 학습 참고서",
    "초등학생을 대상으로 한 학습 참고서",
    "초등학습참고서에 해당되지 않는 것으로 영유아, 초등학생을 대상으로 한 도서",
    "예비번호",
    "주로 학술∙전문적인 내용의 도서"
]

isbn2_shape = ["문고본", "사전", "신서판", "단행본", "시리즈", "전자출판물", "도감", "만화책", "혼합자료", "예비번호"]
isbn2_desc = [
    "세로 15cm 이하 자료",
    "사전류(책 크기에 상관없음)",
    "세로 18cm 미만 자료",
    "세로 18cm 이상 자료",
    "전집, 총서, 다권본, 시리즈",
    "E-Book, CD, DVD 등",
    "도감류",
    "그림책, 만화",
    "혼합자료, 점자자료, 마이크로자료",
    "예비번호"
]

isbn3 = {
    0: ["총류,컴퓨터과학", "도서학", "문헌 정보학", "백과사전", "강연집,연설문집", "일반 연속 간행물", "일반학회,단체,기관,박물관", "신문,저널리즘", "일반전집", "향토자료"],
    1: ["철학일반", "형이상학", "인식론,인간학", "철학체계", "경학,사서,오경", "동양철학,사상", "서양철학", "논리학", "심리학,풍수지리,관상", "윤리학,자기계발"],
    2: ["종교일반", "비교종교학", "불교", "기독교,천주교,유대교", "도교", "천도교,단군교,대종교", "", "힌두교,브라만교", "이슬람교,조로아스터교", "기타종교"],
    3: ["사회과학일반", "통계학", "경제학,경영학,부동산,보험,취업", "사회학,사회복지", "정치학,외교학,선거,입법,통일", "행정학,경비,경찰", "법학", "교육학", "풍속,예절,민속학", "군사학"],
    4: ["자연과학일반", "수학", "물리학", "화학", "천문학", "지구과학", "광물학", "생명과학", "식물학", "동물학"],
    5: ["기술과학일반", "의학,약학,한의학,다이어트", "농학,수의학,임업", "공학,공업,토목,환경", "건축공학,구조,설비", "기계공학,군사공학,원자핵공학,자동차,로봇", "전기공학,전자공학", "화학공학,연료공업,식품공학,음료기술", "제조업,인쇄술", "생활과학,의복,미용"],
    6: ["예술일반", "", "조각 및 조형예술", "공예, 장식미술", "서예", "회화,도화,판화", "사진예술", "음악,국악,오페라", "공연예술,영화,연극,무용", "오락,스포츠"],
    7: ["언어일반", "한국어", "중국어", "일본어,기타 아시아어", "영어", "독일어", "프랑스어", "스페인어,포르투칼어", "이탈리아어", "기타언어"],
    8: ["문학일반", "한국문학", "중국문학", "일본문학, 기타 아시아문학", "영미문학", "독일문학", "프랑스문학", "스페인문학,포르투칼문학", "이탈리아문학", "기타문학"],
    9: ["역사일반", "아시아역사,아시아지리", "유럽역사,유럽지리", "아프리카역사,아프리카지리", "북아메리카역사,북아메리카지리", "남아메리카역사,남아메리카지리", "오세아니아역사,오세아니아지리", "", "지리,관광", "전기,족보"]
}

isbn_add1_info = []

# isbnadd1 테이블 기본 자료 입력
for idx, (target, desc) in enumerate(zip(isbn1_target, isbn1_desc)):
    # print(idx, target, desc)
    info = {
        "pk": 0,
        "model": "books.isbnadd1",
        "fields": {}
    }
    info["pk"] = idx + 1

    f = info["fields"]
    f["num"] = str(idx)
    f["target"] = target
    f["desc"] = desc

    isbn_add1_info.append(info)

# isbnadd1 용 데이터 생성
with open("./data/isbn_add/isbn_add1.json", 'w', encoding="utf-8") as f:
    json.dump(isbn_add1_info, f)
#######################################################################################


# isbnadd2 테이블 기본자료 입력
isbn_add2_info = []
for idx, (shape, desc) in enumerate(zip(isbn2_shape, isbn2_desc)):
    # print(idx, target, desc)
    info = {
        "pk": 0,
        "model": "books.isbnadd2",
        "fields": {}
    }
    info["pk"] = idx + 1

    f = info["fields"]
    f["num"] = str(idx)
    f["shape"] = shape
    f["desc"] = desc

    isbn_add2_info.append(info)

# isbnadd2 용 데이터 생성
with open("./data/isbn_add/isbn_add2.json", 'w', encoding="utf-8") as f:
    json.dump(isbn_add2_info, f)



#######################################################################################
# isbnadd3 테이블 기본자료 입력
isbn_add3_info = []
pk = 0
for key in isbn3.keys():
    for idx, desc in enumerate(isbn3[key]):
        pk += 1
        info = {
            "pk": pk,
            "model": "books.isbnadd3",
            "fields": {}
        }

        f = info["fields"]
        f["num"] = str(key) + str(idx)
        f["desc"] = desc

        isbn_add3_info.append(info)

# isbnadd3 용 데이터 생성
with open("./data/isbn_add/isbn_add3.json", 'w', encoding="utf-8") as f:
    json.dump(isbn_add3_info, f)


# isbn_pk_info.json 생성
isbn_pk_info = {
    "isbn_add1": {},
    "isbn_add2": {},
    "isbn_add3": {}
}

for i in range(0, 10):
    isbn_pk_info["isbn_add1"][i] = i + 1
    isbn_pk_info["isbn_add2"][i] = i + 1

ibsn_add3_pk = 0
for i in range(0, 10):
    for j in range(0, 10):
        ibsn_add3_pk += 1
        num = str(i) + str(j)
        isbn_pk_info["isbn_add3"][num] = ibsn_add3_pk

# isbn_pk_info.json 생성
with open("./data/isbn_add/isbn_pk_info.json", 'w', encoding="utf-8") as f:
    json.dump(isbn_pk_info, f)

