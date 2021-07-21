import json
import requests
import pandas as pd
from datetime import datetime as dt

from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.utils import permission
from books.models import Book
from books.models import PopularBook
from books.serializers import BookSerializer
from books.serializers import PopularBookSerializer
from libraries.models import Library
from libraries.serializers import LibrarySerializer

from .recommend import get_book_list_by_initial_info
from .recommend import get_user_like_similarity_info
from .recommend import get_book_list_by_description
from .recommend import get_book_list_by_title
from .recommend import get_book_list_by_review
from .recommend import get_recommend_books
from .preprocess import RecommendBooks
from .tendency import UserTendency

def get_user_info(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data["email"]
    password = data["password"]
    return authenticate(email=email, password=password)

@csrf_exempt
def temp(request):
    # data = json.loads(request.body.decode('utf-8'))
    # 남자 아이 아이디
    # user = authenticate(email="real@bookridge.com", password="asdf1212!")
    # 20세 남성 용 아이디
    # user = authenticate(email="real2@bookridge.com", password="asdf1212!")
    # 30세 여성 용 아이디
    user = authenticate(email="real3@bookridge.com", password="asdf1212!")
    data = UserSerializer(user)

    ls = get_book_list_by_initial_info(data.data)
    ser = BookSerializer(ls[0], many=True)
    info = {
        "books": ser.data,
        "perc": ls[1]
    }
    
    return JsonResponse(info)

@csrf_exempt
def make_info(request):
    
    # pop_books_2017 = PopularBook.objects.filter(start_data__startswith="2017")
    # pop_books_2018 = PopularBook.objects.filter(start_data__startswith="2018")
    # pop_books_2019 = PopularBook.objects.filter(start_data__startswith="2019")
    # pop_books_2020 = PopularBook.objects.filter(start_data__startswith="2020")

    data = {}
    try:
        pop_books =  PopularBook.objects.all()
        # print(pop_book)
        pop_book_serial = PopularBookSerializer(pop_books, many=True)
        # print(pop_book_serial.data)
        data["popular"] = {}

        data["popular"]['gender'] = {}
        data["popular"]["gender"]["2017"] = {'남성':0, '여성':0}
        data["popular"]["gender"]["2018"] = {'남성':0, '여성':0}
        data["popular"]["gender"]["2019"] = {'남성':0, '여성':0}
        data["popular"]["gender"]["2020"] = {'남성':0, '여성':0}

        data["popular"]['age'] = {}
        data["popular"]["age"]["2017"] = [0,0,0,0,0,0,0]
        data["popular"]["age"]["2018"] = [0,0,0,0,0,0,0]
        data["popular"]["age"]["2019"] = [0,0,0,0,0,0,0]
        data["popular"]["age"]["2020"] = [0,0,0,0,0,0,0]

        data["popular"]["date"] = {}
        data["popular"]["date"]["2017"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2018"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2019"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2020"] = [0,0,0,0,0,0,0,0,0,0,0,0]

        # print(pop_book_serial.data)
        for pick in pop_book_serial.data:
            # print(pick)
            year = pick['start_date'][:4]
            month = int(pick['start_date'][5:7])-1

            if pick["gender"] == 0:
                data["popular"]['gender'][year]['남성'] += pick['rent_count']
            else:
                data["popular"]['gender'][year]['여성'] += pick['rent_count']

            if pick['age'] == "8~13세":
                data["popular"]["age"][year][0] += pick['rent_count']
            elif pick['age'] == "14~19세":
                data["popular"]["age"][year][1] += pick['rent_count']
            elif pick['age'] == "20대":
                data["popular"]["age"][year][2] += pick['rent_count']
            elif pick['age'] == "30대":
                data["popular"]["age"][year][3] += pick['rent_count']
            elif pick['age'] == "40대":
                data["popular"]["age"][year][4] += pick['rent_count']
            elif pick['age'] == "50대":
                data["popular"]["age"][year][5] += pick['rent_count']
            elif pick['age'] == "60세 이상":
                data["popular"]["age"][year][6] += pick['rent_count']

            data["popular"]["date"][year][month] += pick['rent_count']
            
    except: 
        data['error'] = "도서 대여 정보가 없습니다."
    
    with open("./analyze/data/analyze_pop_books.json", "w", encoding='utf-8') as json_file:
            temp_D = pd.DataFrame(data)

            result = {
                "date": f"2017-01~2020-08",
                "data": temp_D, 
            }
            json.dump(result, json_file, indent="\t", default=lambda temp_D: json.loads(temp_D.to_json()))

    temp_result = {"result": "성공?"}
    return JsonResponse(temp_result)

@csrf_exempt
def get_info(request):
    with open("./analyze/data/analyze_pop_books.json", "r", encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        # print(json_data)
        data = json_data["data"]
        return JsonResponse(data)

class RocomLikeView(View):
    @permission
    def get(self, request):
        user = request.user
        # data = UserSerializer(user)
        df = get_user_like_similarity_info(user)
        info = {}
        return JsonResponse(info)

class RocomDescView(View):
    @permission
    def get(self, request):
        user = request.user
        books = get_book_list_by_description(user)
        books = BookSerializer(books, many=True)
        info = {"data": books.data}
        return JsonResponse(info)

class RocomTitleView(View):
    @permission
    def get(self, request):
        user = request.user
        books = get_book_list_by_title(user)
        books = BookSerializer(books, many=True)
        info = {"data": books.data}
        return JsonResponse(info)

class RocomReviewView(View):
    @permission
    def get(self, request):
        user = request.user
        books = get_book_list_by_review(user)
        books = BookSerializer(books, many=True)
        info = {"data": books.data}
        return JsonResponse(info)
        
class RecommendBooksView(View):
    @permission
    def get(self, request):
        if request.method == 'OPTIONS':
            return JsonResponse({})
            
        user = request.user
        recommendations = get_recommend_books(user)
        r1 = BookSerializer(recommendations["desc"], many=True)
        r2 = BookSerializer(recommendations["title"], many=True)
        r3 = BookSerializer(recommendations["review"], many=True)
        r4 = BookSerializer(recommendations["others"], many=True)
        r5 = BookSerializer(recommendations["genres"], many=True)

        desc = [] if len(r1.data) == 0 else r1.data
        title = [] if len(r2.data) == 0 else r2.data
        review = [] if len(r3.data) == 0 else r3.data
        others = [] if len(r4.data) == 0 else r4.data
        genres = [] if len(r5.data) == 0 else r5.data

        info = {
            "desc": desc,
            "title": title,
            "review": review,
            "others": others,
            "genres": genres
        }
        return JsonResponse(info)

class RecomFeatureView(View):
    def get_user_age(self, birth, western_age=True):
        bt = dt.strptime(birth, '%Y-%m-%d')
        return dt.today().year - bt.year if western_age else dt.today().year - bt.year + 1

    def get_user_age_range(self, age):
        try:
            if age < 14:
                return "8~13세"
            elif 14<=age<20:
                return "14~19세" 
            elif 20<=age<30:
                return "20대"
            elif 30<=age<40:
                return "30대"
            elif 40<=age<50:
                return "40대"
            elif 50<=age<60:
                return "50대"
            elif 60<=age:
                return "60세 이상"
            else:
                return "미상"
        except:
            pass
    
    def get_popular_books(self, dataframe):
        pass

    @permission
    def get(self, request):
        
        if request.method == 'OPTIONS':
            return JsonResponse({})

        user = request.user
        birth = str(user.birth)
        gender = user.gender

        age = self.get_user_age(birth)
        age_range = self.get_user_age_range(age)
        
        if age_range == "미상":
            books = PopularBook.objects.filter(gender=gender).order_by('-rent_count')[:300]
            df = pd.DataFrame(books.values())
        else:
            books = PopularBook.objects.filter(Q(gender=gender) & Q(age=age_range)).order_by('-rent_count')[:300]
            df = pd.DataFrame(books.values())
        
        df = df.groupby(["book_id"])["rent_count"].sum().reset_index().sort_values(by=["rent_count"], ascending=False)
        
        book_ids = df["book_id"].values
        recom = BookSerializer(Book.objects.filter(pk__in=book_ids), many=True).data

        data = {
            "feature": recom,
            "info": {
                "gender": gender,
                "age": age,
                "name": user.name
            }
        }
        return JsonResponse(data)
class TendencyBooksView(View):
    @permission
    def get(self, request):
        
        user = request.user
        ut = RecommendBooks(user)
        ut.get_recommend_books_by_genre()
        
        info = {}
        return JsonResponse(info)
