from django.shortcuts import render ,redirect
from .models import Post,Category,Tag
from django.views.generic import ListView,DetailView,CreateView,UpdateView ##장고에서 제공
from django.contrib.auth.mixins import  LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
# Create your views here.

##def index(request): #render는 웹에서 보여지는...
##    posts1=Post.objects.all().order_by('-pk')#pk는 primary key / -pk로 하면 반대.
  ##  return render(request, 'blog/index.html', {'posts':posts1} )

##def single_post_page(request,pk):
 ##   post2 = Post.objects.get(pk=pk)
   ## return render(request, 'blog/single_post_page.html', {'post':post2})

class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields = ['title','hook_text','content','head_image','file_upload','category','tags']

    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def form_valid(self, form):#request는 client??
        current_User=self.request.user
        if current_User.is_authenticated and (current_User.is_superuser or current_User.is_staff):
            form.instance.author = current_User
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

    # 템플릿 : 모델명_form.html


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count']= Post.objects.filter(category=None).count
        return context

class PostList(ListView):## ListView 장고에서 제공
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count']= Post.objects.filter(category=None).count
        return context
    # 템플릿 모델명_list.html : post_list.html (템플릿 이름 자동으로 생성?) --> index.html 이름 수정
    #자동으로 전달되는 데이터/ 파라메터/-->  모델명_list 형태로 전달. -->post_list 형태로 전달

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context
 #템플릿 모델명_detail.html : post_detail.html (이름 자동 생성) --> single_post_page 이름 수정
    #파라메터 --> 모델명 --> post


def category_page(request ,slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)#오른쪽 slug는 url을 통해서전달된 slug값?
        post_list = Post.objects.filter(category=category)



    return render(request,'blog/post_list.html',{
        'category' : category, #따옴표 안에 있는게 변수
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })#1.request 2.html파일 3. html에 전달할 값?!

def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(request, 'blog/post_list.html',{
        'tag' : tag,
        'post_list' : post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })






