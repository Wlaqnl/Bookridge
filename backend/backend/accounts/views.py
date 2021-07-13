from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse


from decouple import config

from .models import User
from .models import UserPrivacy
from .models import Calendar
from books.models import Book
from .forms import LoginForm, CustomUserChangeForm, CustomUserCreationForm
from .serializers import UserSerializer
from .serializers import UserPrivacySerializer
from .serializers import CalendarSerializer
from books.serializers import BookSerializer
from .utils import permission

import requests
import json
import jwt

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


@csrf_exempt
def signup(request):
    print('회원가입 진입')
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if request.method == 'POST':
        form = CustomUserCreationForm(data=data)
        print(form)
        if form.is_valid():
            user = form.save()
            UserPrivacy(user=user).save()
            print(user)
            data = {}
            data['result'] = 'success'
            return JsonResponse(data)
    else:
        form = CustomUserCreationForm()
    data = {}
    data['error'] = form.errors.as_json()
    return JsonResponse(data)


@csrf_exempt
def check_email(request):
    email = request.GET.get('email')
    data = {}
    if User.objects.filter(email=email).exists():
        data["result"] = False
        return JsonResponse(data)
    else:
        data["result"] = True
        return JsonResponse(data)

@csrf_exempt
def login(request):
    # print("login 진입")
    # print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    # print(data)

    if request.method == 'GET':
        return HttpResponse("GET또다제")

    if request.method == 'POST':
        form = LoginForm(data=data)

        if form.is_valid():
            email = data["email"]
            password = data["password"]
            user = authenticate(email=email, password=password)
            # print(user)
            if user is not None:
                if user.is_active:
                    token = jwt.encode({"email": email}, config(
                        'SECRET_KEY'), algorithm="HS256")
                    token = token.decode("utf-8")
                    # print(token)
                    data = {}
                    data["token"] = token
                    data["user_pk"] = user.pk
                    return JsonResponse(data)
            else:
                data = {}
                data['error'] = "존재하지 않는 회원입니다."
        else:
            data = {}
            data['error'] = "아이디, 비밀번호를 확인해주세요."
    return JsonResponse(data)


def logout(request):
    pass

# KAKAO


def oauth(request):
    code = request.GET.get('code', None)
    # print('이것이 code = ' + str(code))
    client_id = config('KAKAO_LOGIN_client_ID')
    redirect_uri = config('REDIRECT_URI')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    # print('이것은 access_token = ' + str(access_token))

    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded; charset-utf-8',
    }
    kakao_response = requests.get(url, headers=headers).json()
    # print('이것이 결과 = ' + str(kakao_response))

    try:
        email = kakao_response['kakao_account']['email']
    except:
        email = 'kakao_account' + str(kakao_response['id'])

    try:
        if kakao_response['kakao_account']['profile']['profile_image_url']:
            profile_image_url = kakao_response['kakao_account']['profile']['profile_image_url']
        if kakao_response['kakao_account']['profile']['thumbnail_image_url']:
            thumbnail_image_url = kakao_response['kakao_account']['profile']['thumbnail_image_url']
    except:
        profile_image_url = ""
        thumbnail_image_url = ""

    gender = 2
    name = kakao_response['properties']['nickname']
    social = 1
    social_id = str(kakao_response['id'])

    User = get_user_model()

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        # print(user)
        token = jwt.encode({"email": user.email}, config(
            'SECRET_KEY'), algorithm="HS256")
        token = token.decode("utf-8")
        data = {}
        data["token"] = token
        data["social_id"] = user.social_id
        data["user_pk"] = user.pk
        data["user_gender"] = user.gender
        data["email"] = user.email
        data["name"] = user.name
        data["social"] = user.social
        # print(data)
        return JsonResponse(data)

    User(
        email=email,
        gender=gender,
        name=name,
        social=social,
        social_id=social_id,
    ).save()

    user = User.objects.get(email=email)
    UserPrivacy(user=user).save()

    token = jwt.encode({"email": user.email}, config(
        'SECRET_KEY'), algorithm="HS256")
    token = token.decode("utf-8")
    data = {}
    data["token"] = token
    data["social_id"] = social_id
    data["user_pk"] = user.pk
    data["user_gender"] = user.gender
    data["email"] = user.email
    data["name"] = user.name
    data["social"] = user.social
    return JsonResponse(data)


def kakao_login(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = config('KAKAO_LOGIN_client_ID')
    redirect_uri = config('REDIRECT_URI')
    # print(redirect_uri)
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'

    return redirect(login_request_uri)


class UnlinkView(View):
    @permission
    def delete(self, request):
        user = request.user
        if user.social == 1:  # 카카오 연결 끊기(탈퇴)
            unlink_request_url = 'https://kapi.kakao.com/v1/user/unlink'
            # print(ADMIN_KEY)
            headers = {
                'Authorization': 'KakaoAK ' + config('ADMIN_KEY'),
            }
            params = {
                'Authorization': 'KakaoAK ' + config('ADMIN_KEY'),
                'target_id': user.social_id,
                'target_id_type': "user_id",
            }
            result = requests.post(
                unlink_request_url, headers=headers, params=params).json()
            # print(result)
            user.delete()
            data = {
                'result': "카카오 연결 끊기",
            }
        else:  # 일반, 구글 (탈퇴)
            user.delete()
            data = {
                'result': "회원 탈퇴"
            }
        return JsonResponse(data)

    @permission
    def post(self, request):  # 카카오 로그아웃
        user = request.user
        logout_request_url = 'https://kapi.kakao.com/v1/user/logout'
        headers = {
            'Authorization': config('ADMIN_KEY'),
        }
        params = {
            'Authorization': config('ADMIN_KEY'),
            'target_id': user.social_id,
            'target_id_type': "user_id"
        }
        result = requests.post(
            logout_request_url, headers=headers, params=params).json()
        # print(result)
        data = {
            'result': '카카오 로그아웃'
        }

        return JsonResponse(data)


def google_login(request):
    # print('google_login 진입')
    login_request_uri = "https://accounts.google.com/o/oauth2/v2/auth?"
    client_id = config('GOOGLE_LOGIN_client_ID')
    # print(client_id)
    redirect_uri = config('REDIRECT_URI_GOOGLE')
    # print(redirect_uri)
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'
    login_request_uri += '&scope=profile%20email%20openid'
    # print(login_request_uri)

    return redirect(login_request_uri)


def oauth2(request):
    # print('oauth2 진입')
    code = request.GET.get('code', None)
    # print('이것이 code = ' + str(code))
    client_id = config('GOOGLE_LOGIN_client_ID')
    redirect_uri = config('REDIRECT_URI_GOOGLE')
    client_secret = config('GOOGLE_SECRET')

    access_token_request_uri = "https://accounts.google.com/o/oauth2/token"
    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    access_token_request_uri_data = requests.post(
        access_token_request_uri, params=params)
    # print(access_token_request_uri_data)
    json_data = access_token_request_uri_data.json()
    # print(json_data['id_token'])
    # print(json_data['scope'])
    access_token = json_data['access_token']
    url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    google_response = requests.get(url, headers=headers).json()
    # print(google_response)

    email = google_response['email']
    profile_image_url = google_response['picture']
    thumbnail_image_url = ""
    gender = 2  # 미상
    name = google_response['name']
    social = 2  # 구글
    social_id = str(google_response['sub'])
    User = get_user_model()

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        # print(user)
        token = jwt.encode({"email": user.email}, config(
            'SECRET_KEY'), algorithm="HS256")
        token = token.decode("utf-8")
        data = {}
        data["token"] = token
        data["social_id"] = user.social_id
        data["user_pk"] = user.pk
        data["user_gender"] = user.gender
        data["email"] = user.email
        data["name"] = user.name
        data["social"] = user.social
        return JsonResponse(data)

    User(
        email=email,
        gender=gender,
        name=name,
        social=social,
        social_id=social_id,
    ).save()

    user = User.objects.get(email=email)
    UserPrivacy(user=user).save()

    token = jwt.encode({"email": user.email}, config(
        'SECRET_KEY'), algorithm="HS256")
    token = token.decode("utf-8")
    data = {}
    data["token"] = token
    data["social_id"] = user.social_id
    data["user_pk"] = user.pk
    data["user_gender"] = user.gender
    data["email"] = user.email
    data["name"] = user.name
    data["social"] = user.social
    # print(data)
    return JsonResponse(data)


def get_all_profile(request):
    users = User.objects.all()
    users_serial = UserSerializer(users, many=True)

    return JsonResponse(users_serial.data, safe=False)


class ProfileView(View):
    @permission
    def get(self, request, user_pk):
        # print('profile 진입')
        user = get_object_or_404(User, pk=user_pk)
        user_serial = UserSerializer(user)
        # print(user_serial.data)
        user_privacy = get_object_or_404(UserPrivacy, user=user)
        user_privacy_serial = UserPrivacySerializer(user_privacy)
        # print(user_privacy_serial.data)

        data = {}
        data['privacy'] = {}

        for key, val in user_serial.data.items():
            data[key] = val
        for key, val in user_privacy_serial.data.items():
            data['privacy'][key] = val
        return JsonResponse(data)

    @permission
    def post(self, request, user_pk):
        # print('프로필 수정 진입')
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        form = CustomUserChangeForm(data=data, instance=request.user)
        if form.is_valid():
            user = form.save()
            # print(user)
            data = {}
            user_serial = UserSerializer(user)
            for key, val in user_serial.data.items():
                data[key] = val
            data['result'] = 'success'
            return JsonResponse(data)
        else:
            form = CustomUserCreationForm(instance=request.user)
        data = {}
        data['error'] = "입력값을 확인해주세요."
        return JsonResponse(data)


class PasswordView(View):
    @permission
    def get(self, request, user_pk):
        # print(request.user)
        data = request.GET.get('password')
        # print(data)
        current_password = data
        user = request.user
        data = {}
        if check_password(current_password, user.password):
            data['result'] = True
            return JsonResponse(data)
        else:
            data['result'] = False
            data['error'] = "비밀번호가 일치하지 않습니다."
            return JsonResponse(data)

    @permission
    def post(self, request, user_pk):
        data = json.loads(request.body.decode('utf-8'))
        # print(data['password1'])
        current_password = data['password']
        user = request.user
        if check_password(current_password, user.password):
            password1 = data["password1"]
            password2 = data["password2"]
            if password1 == password2:
                user.set_password(password1)
                user.save()
                user_serial = UserSerializer(user)
                data = {}
                for key, val in user_serial.data.items():
                    data[key] = val
                return JsonResponse(data)
            else:
                data = {}
                data['error'] = "두 비밀번호가 일치하지 않습니다."
                return JsonResponse(data)
        else:
            data = {}
            data['error'] = "비밀번호가 일치하지 않습니다."
            return JsonResponse(data)


class PrivacyView(View):
    @permission
    def post(self, request, user_pk):
        data = json.loads(request.body.decode('utf-8'))
        user_privacy = get_object_or_404(UserPrivacy, user=request.user)
        user_privacy_serial = UserPrivacySerializer(user_privacy, data=data)
        if user_privacy_serial.is_valid(raise_exception=True):
            user_privacy_serial.save()
            data2 = {}
            data2['result'] = user_privacy_serial.data
            return JsonResponse(data2)
        data['result'] = "수정 실패"

        return JsonResponse(data)


class CalendarView(View):
    # calendar create
    @permission
    def put(self, request):
        print('calendar create start')
        data = json.loads(request.body.decode('utf-8'))
        data2 = {}
        
        try:
            start_date = data['start_date']
        except:
            start_date = ""
            data2[result] = "start date 가 없습니다"
            return JsonResponse(data2)

        try:
            end_date = data['end_date']
        except:
            end_date = ""
            data['end_date'] = ""

        book_pk = data['book_pk']
        book = get_object_or_404(Book, pk=book_pk)
        user = request.user
        user_serial = UserSerializer(user)
        
        # try:
        #     calendar = get_object_or_404(Calendar, book=book, user=user)
        #     if calendar.start_date == data['start_date']:
        #         data2['result'] = "이미 등록된 도서입니다."
        #         return JsonResponse(data2)
        # except:
        #     print("except 진입")

        data['book'] = book_pk
        data['user'] = user.pk
        
        serializer = CalendarSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2['result'] = serializer.data
            return JsonResponse(data2)
        data2['result'] = "등록에 실패하였습니다."

        return JsonResponse(data2)

    # 해당 user 의 calendar
    @permission
    def get(self, request):
        data2 = {}

        try:
            date = request.GET.get("date")
        except:
            date = ""

        if date:
            try:
                # end_date 기준
                calendars_red = Calendar.objects.filter(end_date=date)

            except:
                # start_date 기준
                calendars_yellow = Calendar.objects.filter(start_date=date)
            
            data2['red'] = []
            date2['yellow'] = []

            for i in range(len(calendars_red)):
                try:
                    calendar = get_object_or_404(Calendar, pk=calendars_red[i].pk)
                    book = get_object_or_404(Book, pk=calendar.book.pk)
                    calendar_serial = CalendarSerializer(calendar)
                    book_serial = BookSerializer(book)
                    data2['red'].append({'calendar': calendar_serial.data, 'book': book_serial.data})
                except:
                    data2['red'].append({'error': "등록된 책 정보가 없습니다."})

            for i in range(len(calendars_yellow)):
                calendar = get_object_or_404(Calendar, pk=calendars_yellow[i].pk)
                if calendar.end_date:
                    continue
                else:
                    try:
                        book = get_object_or_404(Book, pk=calendar.book.pk)
                        calendar_serial = CalendarSerializer(calendar)
                        book_serial = BookSerializer(book)
                        data2['yellow'].append({'calendar': calendar_serial.data, 'book': book_serial.data})
                    except:
                        data2['yellow'].append({'error': "등록된 책 정보가 없습니다."})
            
        else:
            calendars = Calendar.objects.all()
            data2['result'] = []
            for i in range(len(calendars)):
                try:
                    calendar = get_object_or_404(Calendar, pk=calendars[i].pk)
                    book = get_object_or_404(Book, pk=calendar.book.pk)
                    calendar_serial = CalendarSerializer(calendar)
                    book_serial = BookSerializer(book)
                    data2['result'].append({'calendar': calendar_serial.data, 'book': book_serial.data})
                except:
                    data2['result'].append({'error': "등록된 책 정보가 없습니다."})

        return JsonResponse(data2)

    # calendar update
    @permission
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        calendar_pk = data['calendar_pk']
        calendar = get_object_or_404(Calendar, pk=calendar_pk)
        user = request.user
        data['book'] = book_pk
        data['user'] = user.pk
        serializer = CalendarSerializer(calendar, data=data)
        data2 = {}
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                data2['result'] = serializer.data
        except:
            data2['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        data2 = {}
        try:
            calendar_pk = request.GET.get("calendar_pk")
            calendar = get_object_or_404(Calendar, pk=calendar_pk)
            calendar.delete()
            data2["result"] = "success"
        except:
            data2["result"] = "fail"
        return JsonResponse(data2)