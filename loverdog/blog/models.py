from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
import os

from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # SlugField ; URL에서 활용
    # allow_unicode=True : 모든 유니코드 문자를 지원한다.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'




class Post(models.Model):
    title = models.CharField(max_length=50)     # 제목
    hook_text = models.CharField(max_length=100, blank=True)        # 요약문
    # content = models.TextField()                # 내용
    content = MarkdownxField()                # 내용

    # 해당 폴더를 만들어서 년, 월, 일로 내려가서 저장하도록 설정 / blank=True : 필수 기능 아니라는 뜻
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)

    # 파일 업로드
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    create_at = models.DateTimeField(auto_now_add=True)     # 작성일
    update_at = models.DateTimeField(auto_now=True)         # 수정일
    # author : 작성자, 추 후 작성
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # category 외래키 걸기
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)

    # ManytoMany
    tags = models.ManyToManyField(Tag, blank=True)

    # 파이썬 내장 메서드로, 클래스의 인스턴스를 문자열로 표현한는데 사용한다.

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):         # get_absolute_url, 사용자 정의 함수,
        return f'/blog/{self.pk}/'       # /blog/3

    # 파일 name 가지고오기
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    # 파일 확장자만 가져오기
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):         # 사용자 정의 함수
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} :: {self.content}'


    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    # # + id 값을 넣어주면 그 id값으로 바로 찾아간다.

    def is_update(self):
        return self.update_at - self.create_at > timedelta(seconds=1)

