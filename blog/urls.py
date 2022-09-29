from django.urls import path
from . import views #현재 위치에서 views 가져오기.
urlpatterns = [
    #ip주소/blog
    path('',views.index), #ip주소/blog (index라는 거는 내가 정한 함수 이름. views.py에 있음)
    path('<int:pk>/', views.single_post_page)


]