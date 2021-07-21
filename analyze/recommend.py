import os
import pandas as pd
import random
from datetime import datetime as dt

from .preprocess import get_user_like_similarity
from .preprocess import get_recommend_books_by_desc
from .preprocess import get_recommend_books_by_title
from .preprocess import get_recommend_books_by_score
from .preprocess import RecommendBooks

from books.models import Book

dir_path = os.path.dirname(os.path.realpath(__file__))
weight_info: pd.DataFrame = pd.read_pickle(dir_path + '/data/weight_info.pkl')

def get_user_age(birth, western_age=True):
    """
    사용자의 나이를 얻는다. western_age가 True 면 `만 나이`를 리턴한다.

    Parameters:
        birth (datetime): 사용자의 나이
        western_age (Boolean): Default=True

    Return:
        (int): 사용자의 나이
    """
    bt = dt.strptime(birth, '%Y-%m-%d')
    return dt.today().year - bt.year if western_age else dt.today().year - bt.year + 1

def get_user_age_range(age):
    """
    weight_info 용 나이 index 를 return 한다.
    """
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
    except:
        print("[get_user_age_range] 제대로 된 나이를 입력해주세요")


def get_user_gender(gender):
    """
    사용자의 성별을 return 한다.
    0: 남자, 1: 여자
    """

    if gender:
        return "여성"
    else:
        return "남성"

def get_user_initial_weight(user):
    """
    가입 초기에 사용자 정보를 바탕으로 인기도서 가중치를 return

    Parameters
        user (accounts.models.User): 사용자 정보

    Return
        (pandas.core.series.Series): 가중치 정보
    """
    age = get_user_age(user["birth"])
    age_range = get_user_age_range(age)
    gender = get_user_gender(user["gender"])
    idx = age_range + "_" + gender

    return weight_info.loc[idx]

def get_sorted_user_weight_list(weight):
    """
    가중치 높은 순으로 정렬하기
    """
    return sorted([(idx, val) for idx, val in zip(weight.index, weight.values)], key=lambda x: x[1], reverse=True)

def get_ranked_isbn_add_info(weight):
    """
    isbn 부가기호 별로 분리한 dictionary 를 return 한다.
    """
    weight_list = get_sorted_user_weight_list(weight)
    info = {}

    adds = ["isbn_add1", "isbn_add2", "isbn_add3"]
    for add in adds:
        spliter = add + "_"
        info[add] = [(a[0].split(spliter)[1], a[1]) for a in weight_list if a[0].startswith(spliter)]

    return info

def get_book_list_by_initial_info(user, n=30, list_weight=[]):
    """
    가입 초기에 사용자 정보를 바탕으로 책 30권 추천하기
    가중치는 인기도서 정보로 작성한 가중치를 적용

    Parameters
        user (accounts.models.User): 사용자 정보
        n (int): 추천 책 개수
        list_weight (list): (임시) 사용자가 따로 부여한 가중치를 쓸 때 사용

    Returns:
        (list): 책 pk list
    """
    weight = get_user_initial_weight(user)
    isbn_add_info = get_ranked_isbn_add_info(weight)
    best_isbn_add = ""
    corr_perc = 0.0  # 도서 취향과 얼마나 일치하는지 나타낼 percentage

    for key in isbn_add_info.keys():
        best_isbn_add += isbn_add_info[key][0][0]
        corr_perc += isbn_add_info[key][0][1]

    best_isbn_add += "0"
    books = Book.objects.all().filter(isbn_add_original=best_isbn_add)
    return random.sample(list(books), n), corr_perc

def get_user_like_similarity_info(user):
    return get_user_like_similarity(user)

def get_book_list_by_description(user):
    """
    사용자가 좋아요를 누른 책의 줄거리를 기반으로 책 추천
    """
    book_id_list = get_recommend_books_by_desc(user)
    return sorted(Book.objects.filter(id__in=book_id_list), key=lambda x: list(book_id_list).index(x.id))

def get_book_list_by_title(user):
    """
    사용자가 좋아요를 누른 책의 제목을 기반으로 책 추천
    """
    book_id_list = get_recommend_books_by_title(user)
    return sorted(Book.objects.filter(id__in=book_id_list), key=lambda x: list(book_id_list).index(x.id))

def get_book_list_by_review(user):
    """
    사용자가 작성한 리뷰의 점수를 바탕으로 책 추천
    """
    book_id_list = get_recommend_books_by_score(user)
    return sorted(Book.objects.filter(id__in=book_id_list), key=lambda x: list(book_id_list).index(x.id))

def get_recommend_books(user):

    recommends = {}
    try:
        email = user.email
        user_booklist_dir = dir_path + f'\\data\\users_recommends\\{email}_books.pkl'
        users_books = pd.read_pickle(user_booklist_dir)

        desc = Book.objects.filter(id__in=users_books["desc"]) if len(users_books["desc"]) > 0 else []
        title = Book.objects.filter(id__in=users_books["title"]) if len(users_books["title"]) > 0 else []
        review = Book.objects.filter(id__in=users_books["review"]) if len(users_books["review"]) > 0 else []
        others = Book.objects.filter(id__in=users_books["others"]) if len(users_books["others"]) > 0 else []
        genres = Book.objects.filter(id__in=users_books["genres"]) if len(users_books["genres"]) > 0 else []

        recommends = {
            "desc": desc,
            "title": title,
            "review": review,
            "others": others,
            "genres": genres
        }
    except:
        r = RecommendBooks(user)
        book_id_list = r.get_recommend_book_ids()
        desc = Book.objects.filter(id__in=book_id_list[0]) if len(book_id_list[0]) > 0 else []
        title = Book.objects.filter(id__in=book_id_list[1]) if len(book_id_list[1]) > 0 else []
        review = Book.objects.filter(id__in=book_id_list[2]) if len(book_id_list[2]) > 0 else []
        others = Book.objects.filter(id__in=book_id_list[3]) if len(book_id_list[3]) > 0 else []
        genres = Book.objects.filter(id__in=book_id_list[4]) if len(book_id_list[4]) > 0 else []

        recommends = {
            "desc": desc,
            "title": title,
            "review": review,
            "others": others,
            "genres": genres
        }
    
    return recommends
