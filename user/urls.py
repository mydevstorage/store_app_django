from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    # UpdateView должен получить в маршруте pk пользователя с которым работает!!! 
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
