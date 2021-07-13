from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from accounts.utils import permission
import requests
import json
from books.models import Book
from .models import Review, Phrase, ReviewComment
from .serializers import ReviewSerializer, PhraseSerializer, ReviewCommentSerializer
from books.serializers import BookSerializer
from accounts.models import User
from accounts.serializers import UserSerializer

# Create your views here.


class ReviewView(View):
    # create
    @permission
    def put(self, request):
        print('review create start')
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        print(data)
        book = get_object_or_404(Book, pk=book_pk)
        user = request.user
        user_serial = UserSerializer(user)
        print(book)
        data['book'] = book_pk
        data['user'] = user.pk
        # data['user'] = user_serial.data
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2 = {}
            data2['result'] = serializer.data
        #     print(serializer.data)
        #     reviews = Review.objects.filter(book=book)
        #     reviews_serial = ReviewSerializer(reviews, many=True)
            return JsonResponse(data2)

        return JsonResponse(data)

    # 해당 book 의 reviews
    @permission
    def get(self, request):
        book_pk = int(request.GET.get("book_pk"))
        book = get_object_or_404(Book, pk=book_pk)
        reviews = Review.objects.filter(book=book)
        data2 = {}
        data2['result'] = []

        for i in range(len(reviews)):
            try:
                review = get_object_or_404(Review, pk=reviews[i].pk)
                user = get_object_or_404(User, pk=review.user.pk)
                review_serial = ReviewSerializer(review)
                user_serial = UserSerializer(user)
                data2['result'].append({'review': review_serial.data, 'user': user_serial.data})
            except:
                data2['result'].append({'error': "등록된 리뷰 정보가 없습니다."})



        return JsonResponse(data2)

    # update
    @permission
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        review_pk = data['review_pk']
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
        data['book'] = book_pk
        data['user'] = user.pk
        serializer = ReviewSerializer(review, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2 = {}
            data2['result'] = serializer.data
            return JsonResponse(data2)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        review_pk = request.GET.get("review_pk")
        review = get_object_or_404(Review, pk=review_pk)
        review.delete()
        data2 = {}
        data2["result"] = "success"
        return JsonResponse(data2)


class PhraseView(View):
    # create
    @permission
    def put(self, request):
        print('phrase create start')
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        user = request.user
        data['book'] = book_pk
        data['user'] = user.pk
        serializer = PhraseSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2 = {}
            data2['result'] = serializer.data

            return JsonResponse(data2)

        return JsonResponse(data)

    # 해당 book 의 phrases
    @permission
    def get(self, request):
        book_pk = int(request.GET.get("book_pk"))
        book = get_object_or_404(Book, pk=book_pk)
        try:
            phrases = Phrase.objects.filter(book=book)
            phrases_serial = PhraseSerializer(phrases, many=True)
            data2 = {}
            data2['result'] = phrases_serial.data
        except:
            data2['result'] = "phrase 정보가 없습니다."

        return JsonResponse(data2)

    # update
    @permission
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        phrase_pk = data['phrase_pk']
        phrase = get_object_or_404(Phrase, pk=phrase_pk)
        user = request.user
        data['book'] = phrase.book.pk
        data['user'] = user.pk
        phrase_serializer = PhraseSerializer(phrase, data=data)
        if phrase_serializer.is_valid(raise_exception=True):
            phrase_serializer.save()
            data2 = {}
            data2['result'] = phrase_serializer.data
            return JsonResponse(data2)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        phrase_pk = request.GET.get("phrase_pk")
        try:
            phrase = get_object_or_404(Phrase, pk=phrase_pk)
            phrase.delete()
            data2 = {}
            data2["result"] = "success"
        except:
            data2['result'] = "phrase 정보가 없습니다."

        return JsonResponse(data2)


class CommunityView(View):
    # 해당 book 의 reviews
    @permission
    def get(self, request):
        #     book_pk = int(request.GET.get("book_pk"))
        #     book = get_object_or_404(Book)
        #     reviews = Review.objects.filter(book=book)
        #     reviews_serial = ReviewSerializer(reviews, many=True)
        #     # print(reviews_serial.data)
        #     data2 = {}
        #     data2['result'] = reviews_serial.data
        #     return JsonResponse(data2)
        # def book_search(request):
        try:
            search_word = request.GET.get("search_word")
            search_type = request.GET.get("search_type")
        except:
            search_word = ""
            search_type = ""
        data2 = {}

        if search_word:
            # search_type
            # 제목(0), 유저(1), 책(2)
            if int(search_type) == 0:
                try:
                    reviews = Review.objects.filter(
                        title__icontains=search_word)
                    reviews_serial = ReviewSerializer(reviews, many=True)
                    reviews_list = reviews_serial.data
            
                    for review in reviews_list:
                        book = get_object_or_404(Book, pk=review["book"])
                        book_serial = BookSerializer(book)

                        user = get_object_or_404(User, pk=review["user"])
                        user_serial = UserSerializer(user)

                        review["book_title"] = book_serial.data["title"]
                        review["book_img_url"] = book_serial.data["img_url"]
                        review["user_email"] = user_serial.data["email"]
                        review["user_name"] = user_serial.data["name"]

                    data2['result'] = reviews_list
                except:
                    data2['error'] = "검색 결과가 없습니다."
            elif int(search_type) == 1:
                try:
                    reviews = Review.objects.filter(
                        user__icontains=search_word)
                    reviews_serial = ReviewSerializer(reviews, many=True)
                    reviews_list = reviews_serial.data
            
                    for review in reviews_list:
                        book = get_object_or_404(Book, pk=review["book"])
                        book_serial = BookSerializer(book)

                        user = get_object_or_404(User, pk=review["user"])
                        user_serial = UserSerializer(user)

                        review["book_title"] = book_serial.data["title"]
                        review["book_img_url"] = book_serial.data["img_url"]
                        review["user_email"] = user_serial.data["email"]
                        review["user_name"] = user_serial.data["name"]

                    data2['result'] = reviews_list
                except:
                    data2['error'] = "검색 결과가 없습니다."
            elif int(search_type) == 2:
                try:
                    reviews = Review.objects.filter(
                        book__icontains=search_word)
                    reviews_serial = ReviewSerializer(reviews, many=True)
                    reviews_list = reviews_serial.data
            
                    for review in reviews_list:
                        book = get_object_or_404(Book, pk=review["book"])
                        book_serial = BookSerializer(book)

                        user = get_object_or_404(User, pk=review["user"])
                        user_serial = UserSerializer(user)

                        review["book_title"] = book_serial.data["title"]
                        review["book_img_url"] = book_serial.data["img_url"]
                        review["user_email"] = user_serial.data["email"]
                        review["user_name"] = user_serial.data["name"]

                    data2['result'] = reviews_list
                except:
                    data2['error'] = "검색 결과가 없습니다."
            return JsonResponse(data2)
        else:
            reviews = Review.objects.all()
            reviews_serial = ReviewSerializer(reviews, many=True)
            reviews_list = reviews_serial.data
            
            for review in reviews_list:
                book = get_object_or_404(Book, pk=review["book"])
                book_serial = BookSerializer(book)

                user = get_object_or_404(User, pk=review["user"])
                user_serial = UserSerializer(user)

                review["book_title"] = book_serial.data["title"]
                review["book_img_url"] = book_serial.data["img_url"]
                review["user_email"] = user_serial.data["email"]
                review["user_name"] = user_serial.data["name"]

            data2['result'] = reviews_list
        return JsonResponse(data2)


class CommentView(View):
    # create
    @permission
    def put(self, request):
        print('comment create start')
        # content = [내용]
        # review = [review_pk]
        data = json.loads(request.body.decode('utf-8'))
        review_pk = data["review_pk"]
        user = request.user
        data['user'] = user.pk

        serializer = ReviewCommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            comments = ReviewComment.objects.filter(review=review_pk)
            comments_serial = ReviewCommentSerializer(comments, many=True)
            comments_list = comments_serial.data
            for comment in comments_list:
                user = get_object_or_404(User, pk=comment["user"])
                user_serial = UserSerializer(user)
                comment["user_email"] = user_serial.data["email"]
                comment["user_name"] = user_serial.data["name"]

            data2 = {}
            data2['result'] = comments_list
            return JsonResponse(data2)

        return JsonResponse(data)

    # 해당 book 의 reviews
    @permission
    def get(self, request):
        # params: { review_pk : review_pk }
        review_pk = request.GET.get("review_pk")
        comments = ReviewComment.objects.filter(review=review_pk)
        comments_serial = ReviewCommentSerializer(comments, many=True)
        comments_list = comments_serial.data
        for comment in comments_list:
            user = get_object_or_404(User, pk=comment["user"])
            user_serial = UserSerializer(user)
            comment["user_email"] = user_serial.data["email"]
            comment["user_name"] = user_serial.data["name"]

        data2 = {}
        data2['result'] = comments_list
        return JsonResponse(data2)

    # update
    @permission
    def post(self, request):
        # comment_pk = [comment_pk]
        # content = [내용]
        # review = [review_pk]
        data = json.loads(request.body.decode('utf-8'))
        comment_pk = data["comment_pk"]
        review_pk = data["review_pk"]

        comment = get_object_or_404(ReviewComment, pk=comment_pk)
        user = request.user
        temp_data = {"content": data["content"], "review": review_pk, "user": user}

        serializer = ReviewCommentSerializer(comment, data=temp_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            comments = ReviewComment.objects.filter(review=review_pk)
            comments_serial = ReviewCommentSerializer(comments, many=True)
            comments_list = comments_serial.data
            for comment in comments_list:
                user = get_object_or_404(User, pk=comment["user"])
                user_serial = UserSerializer(user)
                comment["user_email"] = user_serial.data["email"]
                comment["user_name"] = user_serial.data["name"]

            data2 = {}
            data2['result'] = comments_list
            return JsonResponse(data2)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        # comment_pk = [comment_pk]
        comment_pk = request.GET.get("comment_pk")
        comment = get_object_or_404(ReviewComment, pk=comment_pk)
        review_pk = comment.review
        print(review_pk)
        comment.delete()
        comments = ReviewComment.objects.filter(review=review_pk)
        comments_serial = ReviewCommentSerializer(comments, many=True)
        comments_list = comments_serial.data
        for comment in comments_list:
            user = get_object_or_404(User, pk=comment["user"])
            user_serial = UserSerializer(user)
            comment["user_email"] = user_serial.data["email"]
            comment["user_name"] = user_serial.data["name"]

        data2 = {}
        data2['result'] = comments_list
        return JsonResponse(data2)
