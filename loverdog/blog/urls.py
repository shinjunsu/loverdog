from django.urls import path
from . import views

# localhost:8000/blog

urlpatterns = [
    # /blog : views.py 에 정의 되어 있는 index function을 호출
    # path('',views.index),
    path('', views.PostList.as_view()),
    # /blog/3 , 넘어오는 파라미터를 pk 부른다.
    # path('<int:pk>', views.single_post_page),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),

    path('search/<str:q>/', views.PostSearch.as_view()),
]