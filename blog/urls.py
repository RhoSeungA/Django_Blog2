from django.urls import path
from . import views #현재 위치에서 views 가져오기.
urlpatterns = [
    #ip주소/blog ------- FBV
    #path('',views.index), #ip주소/blog (index라는 거는 내가 정한 함수 이름. views.py에 있음)
    #path('<int:pk>/', views.single_post_page)

    ## CBV
    path('',views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/',views.new_comment),
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()),
    path('create_post/' , views.PostCreate.as_view()),
    path('update_post/<int:pk>/',views.PostUpdate.as_view()),
    path('category/<str:slug>/',views.category_page),
    path('tag/<str:slug>/',views.tag_page),
    path('search/<str:q>/',views.PostSearch.as_view()),



]