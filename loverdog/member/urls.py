from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index-page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
]
