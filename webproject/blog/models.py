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
        cate_list =[]
        if self.level == 1:
            cate_list = [x for x in self.under_category.all().reverse() if x.level == 2]
        elif self.level == 2:
            cate_list = [x for x in self.under_category.all().reverse() if x.level == 3]
        else:
            cate_list = []

        return cate_list
    """
    템플릿에서 사용시 아래 형식처럼 사용하면 된다.
    for x in a.under_list():
        print("하위 카테고리 {}".format(x))
        if not len(x.under_list()) == 0:
            print("{}의 하위 카테고리 {}".format(x, x.under_list()))

    """

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






