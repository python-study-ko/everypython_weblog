from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
# Create your models here.



class Category(models.Model):
    """
    포스트 카테고리
    level = 카테고리 단계로 총 3단계까지 있음
    name = 카테고리 명
    under_category = 관계된 카테고리
    카테고리 트리를 불러올떈 level = 1  카테고리를 추출후 관련된 2차 카테고리,3차 카테고리를 차레로 추출한다.
    """
    level = models.IntegerField(choices=[(1,'1차 카테고리'),(2,'2차 카테고리'),(3,'3차 카테고')],default=1)
    name = models.CharField(max_length=20)
    under_category = models.ManyToManyField("self",symmetrical=True,blank=True)

    # 하위 카테고리를 추출해주는 메소드
    def under_list(self):
        # 1차 카테고리
    
        under_list = []
        if self.level == 1:
            cate_list = self.under_category.all().reverse()
            for x in cate_list:
                if x.level == 2:
                    under_list.append(x)

        # 할일 : [ x for x in self.under_category.all() if x.level == 2] 처러 만들기
        # return under_list
        return cate_list

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    블로그 포스트 모델
    """
    category = models.ForeignKey('Category',blank=True,null=True)
    title = models.CharField(max_length=40)
    author = models.ForeignKey(User, unique=True)
    content = RichTextUploadingField()
    tag = TaggableManager()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)


    def __str__(self):
        return self.title






