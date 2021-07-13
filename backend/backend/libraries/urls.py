from django.urls import path
from . import views


app_name = 'libraries'

urlpatterns = [
    path('get_lib_all/', views.get_lib_all, name='get_lib_all'),
]