from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
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
