from django.shortcuts import render
from .models import Post
# Create your views here.
def index(request): #render는 웹에서 보여지는...
    posts1=Post.objects.all().order_by('-pk')#pk는 primary key / -pk로 하면 반대.
    return render(request, 'blog/index.html', {'posts':posts1} )

def single_post_page(request,pk):
    post2 = Post.objects.get(pk=pk)
    return render(request, 'blog/single_post_page.html', {'post':post2})

