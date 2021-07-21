from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'analyze'

urlpatterns = [
    path('temp/', views.temp, name='temp'),
    path('make_info/', views.make_info, name='make_info'),
    path('get_info/', views.get_info, name='get_info'),
    path('like_temp/', csrf_exempt(views.RocomLikeView.as_view()), name='like_temp'),
    path('desc_temp/', csrf_exempt(views.RocomDescView.as_view()), name='desc_temp'),
    path('title_temp/', csrf_exempt(views.RocomTitleView.as_view()), name='title_temp'),
    path('review_temp/', csrf_exempt(views.RocomReviewView.as_view()), name='review_temp'),
    path('recommend_temp/', csrf_exempt(views.RecommendBooksView.as_view()), name='recommend_temp'),
    path('feature_temp/', csrf_exempt(views.RecomFeatureView.as_view()), name='feature_temp'),
    path('tendency_temp/', csrf_exempt(views.TendencyBooksView.as_view()), name='tendency_temp'),
]