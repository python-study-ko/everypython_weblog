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
    """
    level = models.IntegerField(choices=[(1,'1차 카테고리'),(2,'2차 카테고리'),(3,'3차 카테고')],default=1)
    name = models.CharField(max_length=20)
    under_category = models.ManyToManyField("self",symmetrical=True,blank=True)


    def under_list(self):
        """
        해당 객체의 하위 카테고리를 추출한다.
        :return: 하위 카테고리가 없으면 Noen / 있으면 리스트에 해당객체를 담아줌
        """
        # 하위 카테고리 목록 초기화
        cate_list = None

        # 1차 카테고리
        if self.level == 1:
            cate_list = [x for x in self.under_category.all().reverse() if x.level == 2]
        # 2차 카테고리
        elif self.level == 2:
            cate_list = [x for x in self.under_category.all().reverse() if x.level == 3]
        # 3차 카테고리 : 하위 카테고리를 가질수 없음
        else:
            cate_list = None
            return cate_list

        return cate_list if len(cate_list) != 0 else None
    """
    하위 카테고리 사용 예시
    a = Category.objects.get(id=1)
    for x in a.under_list():
        print("{}차 카테고리 {}의 {}차 하위 카테고리 {}".format(a.level,a.name,x.level,x.name))
        if x.under_list() != None:
            for u in x.under_list():
                print("{}차 카테고리 {}의 {}차 하위 카테고리 {}".format(x.level,x.name,u.level,u.name))

    """
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    블로그 포스트 모델
    """
    category = models.ForeignKey('Category',blank=True,null=True)
    title = models.CharField(max_length=40)
    author = models.ForeignKey(User)
    content = RichTextUploadingField()
    tag = TaggableManager()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)


    def __str__(self):
        return self.title






