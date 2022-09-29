from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView ##장고에서 제공
# Create your views here.

##def index(request): #render는 웹에서 보여지는...
##    posts1=Post.objects.all().order_by('-pk')#pk는 primary key / -pk로 하면 반대.
  ##  return render(request, 'blog/index.html', {'posts':posts1} )

##def single_post_page(request,pk):
 ##   post2 = Post.objects.get(pk=pk)
   ## return render(request, 'blog/single_post_page.html', {'post':post2})


class PostList(ListView):## ListView 장고에서 제공
    model = Post
    ordering = '-pk'
    # 템플릿 모델명_list.html : post_list.html (템플릿 이름 자동으로 생성?) --> index.html 이름 수정
    #자동으로 전달되는 데이터/ 파라메터/-->  모델명_list 형태로 전달. -->post_list 형태로 전달

class PostDetail(DetailView):
    model = Post
    #템플릿 모델명_detail.html : post_detail.html (이름 자동 생성) --> single_post_page 이름 수정
    #파라메터 --> 모델명 --> post

