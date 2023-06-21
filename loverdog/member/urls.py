from django.urls import path
from . import views


# localhost:8000/member
# 라는 요청이오면 여기까지온다.


urlpatterns = [

    path('', views.index),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),

    path('home/', views.home),

]


