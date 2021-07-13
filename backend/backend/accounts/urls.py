from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('oauth/', views.oauth, name='oauth'),
    path('kakao_login/', views.kakao_login, name='kakao_login'),
    path('oauth2/', views.oauth2, name='oauth2'),
    path('google_login/', views.google_login, name='google_login'),
    path('get_all_profile/', views.get_all_profile, name="get_all_profile"),
    path('check_email/', views.check_email, name="check_email"),
    path('unlink/', csrf_exempt(views.UnlinkView.as_view()), name='unlink'),
    path('profile/<int:user_pk>/', csrf_exempt(views.ProfileView.as_view()), name='profile'),
    path('privacy/<int:user_pk>/', csrf_exempt(views.PrivacyView.as_view()), name="privacy"),
    path('password/<int:user_pk>/', csrf_exempt(views.PasswordView.as_view()), name='password'),
    path('calendar/', csrf_exempt(views.CalendarView.as_view()), name='calendar'),
]