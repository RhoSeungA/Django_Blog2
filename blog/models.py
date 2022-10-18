from django.db import models
import os

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)

    content = models.TextField()

    # %Y 2022, %y 22
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    #이거의 시작은 어디냐..,,,, 그리고 blog앞에는 _media생략?

    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #author 추후 작성

    def __str__(self):
        return f'[{self.pk}]{self.title} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
        #basename은 파일이름만
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #~.txt 나 ~.xlsx 여기서 확장자만 분리해야함. split으로 분리
        #a.txt이면,,, [0]은 a이고, [1]은 txt
        #근데 문제는 a.b.x.txt 같은 형태고 있음, 따라서 -1로 해주는 것이 좋음.