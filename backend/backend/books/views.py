from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse

import json
from .models import Book
from .models import PopularBook
from django.contrib.auth import get_user_model
from .serializers import BookSerializer
from .serializers import PopularBookSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from accounts.utils import permission
import requests

def get_book_list(request):
    books = Book.objects.all()[:20000]
    res = BookSerializer(books, many=True)

    return JsonResponse(res.data, safe=False)

def get_pop_book_list(request):
    pop_books = PopularBook.objects.all()
    pop_book_serial = PopularBookSerializer(pop_books, many=True)

    return JsonResponse(pop_book_serial.data, safe=False)

def book_detail(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    book_serial = BookSerializer(book)
    data = {}

    for key, val in book_serial.data.items():
        data[key] = val

    try:
        pop_book = PopularBook.objects.filter(book=book)
        # print(pop_book)
        pop_book_serial = PopularBookSerializer(pop_book, many=True)
        # print(pop_book_serial.data)
        data["popular"] = {}
        data["popular"]['gender'] = {'남성':0, '여성':0}
        data["popular"]['age'] = [0,0,0,0,0,0,0]
        data["popular"]["date"] = {}
        data["popular"]["date"]["2017"] = {}
        data["popular"]["date"]["2018"] = {}
        data["popular"]["date"]["2019"] = {}
        data["popular"]["date"]["2020"] = {}
        data["popular"]["date"]["2017"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2018"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2019"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2020"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        # print(pop_book_serial.data)
        for pick in pop_book_serial.data:
            # print(pick)
            if pick["gender"] == 0:
                data["popular"]['gender']['남성'] += pick['rent_count']
            else:
                data["popular"]['gender']['여성'] += pick['rent_count']
            if pick['age'] == "8~13세":
                data["popular"]["age"][0] += pick['rent_count']
            elif pick['age'] == "14~19세":
                data["popular"]["age"][1] += pick['rent_count']
            elif pick['age'] == "20대":
                data["popular"]["age"][2] += pick['rent_count']
            elif pick['age'] == "30대":
                data["popular"]["age"][3] += pick['rent_count']
            elif pick['age'] == "40대":
                data["popular"]["age"][4] += pick['rent_count']
            elif pick['age'] == "50대":
                data["popular"]["age"][5] += pick['rent_count']
            elif pick['age'] == "60세 이상":
                data["popular"]["age"][6] += pick['rent_count']

            year = pick['start_date'][:4]
            month = int(pick['start_date'][5:7])-1

            data["popular"]["date"][year][month] += pick['rent_count']
            
    except: 
        data['error'] = "도서 대여 정보가 없습니다."

    return JsonResponse(data)

def book_search(request, page_num):
    search_word = request.GET.get("search_word")
    search_type = request.GET.get("search_type")
    data2 = {}

    def page_conf(lst, leng, page_num):
        if leng % 10: # 나머지가 있다. 
            if leng // 10 == page_num: # 단, 10개 꽉 채워지진 않는다.
                return lst[page_num*10:]
            elif leng // 10 > page_num: # 
                return lst[page_num*10:(page_num+1)*10]
            elif leng // 10 < page_num: # 남은게 10개 초과다.
                return []
        else: # 나머지 없다.
            if leng // 10 <= page_num: # 더 이상 보내줄 데이터가 없다.
                return []
            else: # 
                return lst[page_num*10:(page_num+1)*10]

    if search_word:
    # search_type
    # 제목(0), 작가(1), 출판사(2)
        if int(search_type) == 0:
            try:
                books = Book.objects.filter(title__icontains=search_word)
                books_serial = BookSerializer(books, many = True)

                temp_len = len(books_serial.data)
                data2['result'] = page_conf(books_serial.data, temp_len, page_num)
            except:
                data2['error'] = "도서 대여 정보가 없습니다."
        elif int(search_type) == 1:
            try:
                books = Book.objects.filter(author__icontains=search_word)
                books_serial = BookSerializer(books, many = True)

                temp_len = len(books_serial.data)
                data2['result'] = page_conf(books_serial.data, temp_len, page_num)
            except:
                data2['error'] = "도서 대여 정보가 없습니다."
        elif int(search_type) == 2:
            try:
                books = Book.objects.filter(publisher__icontains=search_word)
                books_serial = BookSerializer(books, many = True)
                
                temp_len = len(books_serial.data)
                data2['result'] = page_conf(books_serial.data, temp_len, page_num)
            except:
                data2['error'] = "도서 대여 정보가 없습니다."
        return JsonResponse(data2)
    else:
        data2['result'] = "fail"
    return JsonResponse(data2)

def book_auto_search(request):
    try:
        search_word = request.GET.get("search_word")
    except:
        search_word = ""
    data2 = {}

    if search_word:
        try:
            books = Book.objects.filter(title__istartswith=search_word)
            books_serial = BookSerializer(books, many = True)

            data2['result'] = books_serial.data[:5]
        except:
            data2['result'] = []
            data2['error'] = "도서 정보가 없습니다."

        return JsonResponse(data2)

@csrf_exempt
def like_book(request):
    print("진입")
    book_pk = int(request.GET.get("book_pk"))
    user_pk = int(request.GET.get("user_pk"))
    user = get_object_or_404(get_user_model(), pk=user_pk)
    book = get_object_or_404(Book, pk=book_pk)

    if book.like_users.filter(pk=user.pk).exists():
        book.like_users.remove(user)
        liked = False
    else:
        book.like_users.add(user)
        liked = True
    
    book = get_object_or_404(Book, pk=book_pk)
    print(book.like_users)

    data2 = {
        "liked" : liked,
        "count" : book.like_users.count(),
    }

    return JsonResponse(data2)