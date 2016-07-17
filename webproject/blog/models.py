from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django.db.models.query import QuerySet
from django.db.models import Q
# 오류 발생용
from django.core.exceptions import ValidationError

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

    def under_list(self, obj):
        """
        하위 카테고리 목록을 추출한다
        :param obj:
        :return:
        """
        clist =[]
        if obj.level == 3:
            return obj
        elif obj.level == 2:
            clist += Category.object.get(under_category.filter(level=3))
            return clist
        elif obj.level == 1:
            for c2 in obj.under_category.filter(level=2):
                clist += Category.tree.under_list(c2)
            return clist


class CategoryQuerySets(QuerySet, CategoryMixin):
    pass


class CategoryManager(models.Manager, CategoryMixin):
    def get_query_set(self):
        return CategoryQuerySets(self.model, using=self._db)

class Category(models.Model):
    """
    포스트 카테고리 - 추가,업데이트,삭제 할때마다 카테고리 순서 모델을 갱신시킨다.
    정규화된 카테고리 이동은 아직 지원 안함, 카테고리 이동시 주의 필
    level = 카테고리 단계로 총 3단계까지 있음
    name = 카테고리 명
    under_category = 관계된 카테고리
    """

    parent = models.ForeignKey('self',limit_choices_to=Q(level=1)|Q(level=2),on_delete=models.CASCADE,blank=True,null=True,help_text="상위 카테고리를 정해주세요,미지정시 최상위 카테고리가 됩니")
    name = models.CharField(max_length=15,unique=True,help_text="카테고리 이름을 입력하세요")
    level = models.IntegerField(choices=[(1, '최상위 카테고리'), (2, '2차 카테고리'), (3, '3차 카테고리')], blank=True)
    object = models.Manager()
    # 카테고리 매니저
    tree = CategoryManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #부모 카테고리 검증
        if self.parent:
            if self.parent_id == self.id:
                raise ValidationError('자기자신을 상위카테고리로 지정할수 없습니다.',code='invalid')
        # 카테고리 레벨 자동 지정
        if not self.parent:
            self.level = 1
        elif self.parent.level == 1:
            self.level = 2
        elif self.parent.level == 2:
            self.level = 3
        super(Category,self).save(*args, **kwargs)
        # 카테고리 순서 모델을 갱신
        OrderCategory.order.reset_order()

    def delete(self, *args, **kwargs):
        super(Category,self).delete(*args, **kwargs)
        # 카테고리 순서 모델을 갱신
        OrderCategory.order.reset_order()



class OrderMixin(object):
    """
    카테고리 순서 번호를 갱신한다.
    """
    def reset_order(self):
        OrderCategory.object.all().delete()
        loop_c1 = 0
        for c1 in Category.tree.root_category():
            loop_c1 += 1
            c1obj = OrderCategory(c_pk_id=c1.id,order_num=10000*loop_c1)
            c1obj.save()
            c2s = Category.object.filter(parent_id=c1.id)
            if c2s.exists():
                loop_c2 = 0
                for c2 in c2s:
                    loop_c2 += 1
                    c2obj = OrderCategory(c_pk_id=c2.id,order_num=c1obj.order_num+100*loop_c2)
                    c2obj.save()
                    c3s = Category.object.filter(parent_id=c2.id)
                    if c3s.exists():
                        loop_c3 = 0
                        for c3 in c3s:
                            loop_c3 += 1
                            c3obj = OrderCategory(c_pk_id=c3.id,order_num=c2obj.order_num+1*loop_c3)
                            c3obj.save()
                    else:
                        continue
            else:
                continue


class OrderQuerySets(QuerySet, OrderMixin):
    pass

class OrderManager(models.Manager, OrderMixin):
    def get_query_set(self):
        return OrderQuerySets(self.model, using=self._db)

class OrderCategory(models.Model):
    """카테고리 순서 갱신용 모델"""
    c_pk = models.OneToOneField('Category',unique=True)
    order_num = models.IntegerField()
    object = models.Manager()
    order = OrderManager()


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






