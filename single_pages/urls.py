from django.urls import path
from . import views #현재 위치에서 views 가져오기.


urlpatterns = [
    #ip주소/
    path('',views.landing),             #ip주소/
    path('about_me/',views.about_me),   #ip주소/about_me/
    
]