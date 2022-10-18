from django.test import TestCase,Client
from bs4 import BeautifulSoup
from .models import Post
class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        response= self.client.get('/blog/')#html문서 넘어감.
        # response 결과가 정상적인지
        self.assertEqual(response.status_code,200) #오류페이지가 났을때,??...음... 상태값이 200이라면, 문서를 보여주게됨.

        soup = BeautifulSoup(response.content, 'html.parser')

        #타이틀이 정상적으로 보이는지
        self.assertEqual(soup.title.text,'Blog')#text안쓰면 <title>이거 까지 다 가져옴.

        #navbar가 정상적으로 보이는지
        navbar=soup.nav
        self.assertIn('Blog', navbar.text) #nav안의 모든 텍스트들 중에서 blog가 있는지
        self.assertIn('AboutMe',  navbar.text)

        #post가 정상적으로 보이는지
        #1.맨처음엔 포스트가 하나도 안보임.
        self.assertEqual(Post.objects.count(), 0)
        main_area=soup.find('div',id="main-area")
        self.assertIn('아무 게시물이 없습니다.',main_area.text)

        #2.포스트가 있는 경우
        post_001=Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.")
        post_002=Post.objects.create(title="두번째 포스트", content="두번째 포스트 입니다.")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/') #새로 가져오기??
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div',id="main-area")
        self.assertIn(post_001.title,main_area.text)
        self.assertIn(post_002.title,main_area.text)
        self.assertNotIn('아무 게시물이 없습니다.',main_area.text)

        def test_post_detail(self):
            post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.")
            self.assertEqual(post_001.get_absolute_url(), '/blog/1')

            response = self.client.get(post_001.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')

            navbar = soup.nav
            self.assertIn('Blog', navbar.text)
            self.assertIn('AboutMe', navbar.text)

            self.assertIn(post_001.title, soup.title.text)

            main_area= soup.find('div',id='main-area')
            post_area = main_area.find('div', id='post-area')
            self.assertIn(post_001.title, post_area.text)
            self.assertIn(post_001.content, post_area.text)



    #Ceate your tests here.
