from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'reviews'

urlpatterns = [
    # path('create/', views.create, name='create'),
    # path('detail/<int:review_pk>/', views.detail, name='detail'),
    # path('update/<int:review_pk>/', views.update, name='update'),
    # path('delete/<int:review_pk>/', views.delete, name='delete'),
    path('review/', csrf_exempt(views.ReviewView.as_view()), name='review'),
    path('phrase/', csrf_exempt(views.PhraseView.as_view()), name='phrase'),
    path('community/', csrf_exempt(views.CommunityView.as_view()), name='community'),
    path('comment/', csrf_exempt(views.CommentView.as_view()), name='comment'),
]