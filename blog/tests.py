from django.test import TestCase,Client
from bs4 import BeautifulSoup
from .models import Post,Category
from django.contrib.auth.models import User

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_kim = User.objects.create_user(username="kim",password="somepassword")
        self.user_lee = User.objects.create_user(username="lee",password="somepassword")

        self.category_com = Category.objects.create(name="computer",slug="computer")
        self.category_cul = Category.objects.create(name="culture",slug="culture")

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",
                                       author = self.user_kim, category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트 입니다.",
                                       author=self.user_lee,category=self.category_cul)
        self.post_003=Post.objects.create(title="세번째 포스트", content="세번째 포스트 입니다.",
                                       author=self.user_lee)

    #test로 시작하면 자동으로 시작..test로 시작하면 안됨
    def nav_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('AboutMe', navbar.text)

        home_btn= navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], "/")#attrs은 속성
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], "/blog/")
        About_btn = navbar.find('a', text="AboutMe")
        self.assertEqual(About_btn.attrs['href'], "/about_me/")

#
    def category_test(self,soup):
        category_card =soup.find('div',id='category-card')
        self.assertIn('Categories',category_card.text)
        self.assertIn(f'{self.category_com} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_cul} ({self.category_cul.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)



    def test_post_list(self):
        response= self.client.get('/blog/')#html문서 넘어감.
        # response 결과가 정상적인지
        self.assertEqual(response.status_code,200) #오류페이지가 났을때,??...음... 상태값이 200이라면, 문서를 보여주게됨.

        soup = BeautifulSoup(response.content, 'html.parser')

        #타이틀이 정상적으로 보이는지
        self.assertEqual(soup.title.text,'Blog')#text안쓰면 <title>이거 까지 다 가져옴.


        #
        #navbar가 정상적으로 보이는지
        #navbar=soup.nav
        #self.assertIn('Blog', navbar.text) #nav안의 모든 텍스트들 중에서 blog가 있는지
        #self.assertIn('AboutMe',  navbar.text)
        self.nav_test(soup)
        self.category_test(soup)

        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')  # 새로 가져오기??
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)
        self.assertNotIn('아무 게시물이 없습니다.', main_area.text)

        Post.objects.all().delete()
        #post가 정상적으로 보이는지
        #1.맨처음엔 포스트가 하나도 안보임.

        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')  # html문서 넘어감.
        # response 결과가 정상적인지
        self.assertEqual(response.status_code, 200)  # 오류페이지가 났을때,??...음... 상태값이 200이라면, 문서를 보여주게됨.

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div',id="main-area")
        self.assertIn('아무 게시물이 없습니다.',main_area.text)

        #2.포스트가 있는 경우
        #post_001=Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",author=self.user_kim)
        #post_002=Post.objects.create(title="두번째 포스트", content="두번째 포스트 입니다.",author=self.user_lee)
        # self.assertEqual(Post.objects.count(), 2)
        #
        # response = self.client.get('/blog/') #새로 가져오기??
        # self.assertEqual(response.status_code, 200)
        # soup = BeautifulSoup(response.content, 'html.parser')
        # main_area=soup.find('div',id="main-area")
        # self.assertIn(post_001.title,main_area.text)
        # self.assertIn(post_002.title,main_area.text)
        # self.assertIn(post_001.author.username.upper(), main_area.text)
        # self.assertIn(post_002.author.username.upper(), main_area.text)
        # self.assertNotIn('아무 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
            #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",author=self.user_kim)
            self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

            response = self.client.get(self.post_001.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')

            # navbar = soup.nav
            # self.assertIn('Blog', navbar.text)
            # self.assertIn('AboutMe', navbar.text)
            self.nav_test(soup)

            self.assertIn(self.post_001.title, soup.title.text)

            main_area = soup.find('div',id='main-area')
            post_area = main_area.find('div', id='post-area')
            self.assertIn(self.post_001.title, post_area.text)
            self.assertIn(self.post_001.content, post_area.text)
            self.assertIn(self.post_001.author.username.upper(), post_area.text)

    #Ceate your tests here.
