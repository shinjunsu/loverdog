from django.urls import path
from . import views

# localhost:8000/blog

urlpatterns = [
    path('', views.landing),
    path('about_me/', views.about_me),
]