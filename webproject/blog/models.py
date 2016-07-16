from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount

# hticount 필드 연결용
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class CategoryMixin(object):
    """
    카테고리 정보를 추출해준다
    """
    def root_category(self):
        """
        최상단 카테고리를 추출한다
        :return:
        """
        return self.filter(level=1)

    def under_list(self,obj):
        """
        하위 카테고리 목록을 추출한다
        :param obj:
        :return:
        """
        if obj.level == 3:
            return obj
        elif obj.level == 2:
            Category.object.get(under_category.filter(level=3))
            return clist
        elif obj.level == 1:
            for c2 in obj.under_category.filter(level=2):
                clist += Category.tree.under_list(c2)
            return clist


class CategoryQuerySets(QuerySet,CategoryMixin):
    pass

class CategoryManager(models.Manager,CategoryMixin):
    def get_query_set(self):
        return CategoryQuerySets(self.model, using=self._db)

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
    object = models.Manager()
    # 카테고리 매니저
    tree = CategoryManager()

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


class Post(models.Model,HitCountMixin):
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
    # hitcount 모듈과 연동
    posthits = GenericRelation(HitCount, related_query_name='post',object_id_field='object_pk')

    def __str__(self):
        return self.title






