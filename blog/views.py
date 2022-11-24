from django.shortcuts import render ,redirect
from .models import Post,Category,Tag ,Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView ##장고에서 제공
from django.contrib.auth.mixins import  LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

##def index(request): #render는 웹에서 보여지는...
##    posts1=Post.objects.all().order_by('-pk')#pk는 primary key / -pk로 하면 반대.
  ##  return render(request, 'blog/index.html', {'posts':posts1} )

##def single_post_page(request,pk):
 ##   post2 = Post.objects.get(pk=pk)
   ## return render(request, 'blog/single_post_page.html', {'post':post2})

class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields = ['title','hook_text','content','head_image','file_upload','category']

    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_str = tags_str.strip()  # 앞뒤 빈칸 없앰
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
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
            response=super(PostCreate,self).form_valid(form)
            tags_str=self.request.POST.get('tags_str')#여기서 POST는 (데이터 전달 방식: get 방식 혹은 post방식) ,method=post??
            if tags_str :
                tags_str = tags_str.strip()#앞뒤 빈칸 없앰
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    #get_or_created는 튜플 반환
                    #뒤에는 created되면 참 반환?
                    #tag에는 가져온거.
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
            #return super(PostCreate, self).form_valid(form)
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
    paginate_by = 5
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count']= Post.objects.filter(category=None).count
        return context

    # 템플릿 모델명_list.html : post_list.html (템플릿 이름 자동으로 생성?) --> index.html 이름 수정
    #자동으로 전달되는 데이터/ 파라메터/-->  모델명_list 형태로 전달. -->post_list 형태로 전달

class PostSearch(PostList):#ListView 상속,post_list,post_list.html 자동 호출
    paginated_by=None

    def get_queryset(self):#listview 가 제공해주는 함수
    #queryseㅅ --> 검색 결과,검색 결과 얻는 함수
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) |
            Q(tags__name__contains=q)
        ).distinct()
        return post_list
    def get_context_data(self, *,object_list=None,**kwargs):
        context = super(PostSearch,self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q}({self.get_queryset().count()})'
        return context



class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['comment_form'] = CommentForm
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

def new_comment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=pk)
        #포스트 모델에서 pk=pk인거 가지고 오기
        if request.method =='POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: #GET으로 온 경우
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    #CreateView,UpdateView 이던지,,, form을 사용하면, 템플릿이 model명_forms로 자동을 만들어짐.
    # 템플릿 모델명_forms : comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied














