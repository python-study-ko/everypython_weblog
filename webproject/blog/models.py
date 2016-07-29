from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django.db.models.query import QuerySet
from django.db.models import Q, Count
# 오류 발생용
from django.core.exceptions import ValidationError

# hticount 필드 연결용
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


# 카테고리 목록 매니저
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

    def under_list(self, c):
        """
        하위 카테고리 목록 쿼리셋을 반환한
        :param obj:
        :return:
        """
        order = "ordercategory__order_num"
        if c.level == 1:
            c2 = Category.objects.filter(parent=c)
            c3 = Category.objects.filter(parent__in=c2)
            under_C = Category.objects.filter(
                Q(id=c.id) | Q(id__in=c2.values_list("id", flat=True)) | Q(id__in=c3.values_list("id", flat=True))).order_by(order)
        elif c.level == 2:
            c3 = Category.objects.filter(parent=c)
            under_C = Category.objects.filter(Q(id=c.id) | Q(id__in=c3.values_list("id", flat=True))).order_by(order)
        elif c.level == 3:
            under_C = Category.objects.get(id=c.id)
        return under_C

    def navi_bar(self):
        category_tree = []
        for c1 in Category.tree.root_category():
            under_tree = Category.tree.under_list(c1).filter(post__publish=True).annotate(postcount=Count('post')).values_list('level', 'id', 'name', 'postcount')
            category_tree.append(under_tree)
        return category_tree

    def categorys_post(self,c):
        posts = Category.tree.under_list(c)
        return posts

class CategoryQuerySets(QuerySet, CategoryMixin):
    pass


class CategoryManager(models.Manager, CategoryMixin):
    def get_query_set(self):
        return CategoryQuerySets(self.model, using=self._db)

# 카테고리 모델
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
    objects = models.Manager()
    # 카테고리 매니저
    tree = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        # 부모 카테고리 검증
        if self.parent:
            if self.parent_id == self.id:
                raise ValidationError('자기자신을 상위카테고리로 지정할수 없습니다.', code='invalid')

    def save(self, *args, **kwargs):
        if self.parent:
            if self.parent_id == self.id:
                raise ValidationError('자기자신을 상위카테고리로 지정할수 없습니다.', code='invalid')
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


# 카테고리 정렬 매니저
class OrderMixin(object):
    """
    카테고리 순서 번호를 갱신한다.
    """
    def reset_order(self):
        OrderCategory.objects.all().delete()
        loop_c1 = 0
        for c1 in Category.tree.root_category():
            loop_c1 += 1
            c1obj = OrderCategory(c_pk_id=c1.id,order_num=10000*loop_c1)
            c1obj.save()
            c2s = Category.objects.filter(parent_id=c1.id)
            if c2s.exists():
                loop_c2 = 0
                for c2 in c2s:
                    loop_c2 += 1
                    c2obj = OrderCategory(c_pk_id=c2.id,order_num=c1obj.order_num+100*loop_c2)
                    c2obj.save()
                    c3s = Category.objects.filter(parent_id=c2.id)
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

# 카테고리 정렬 모델
class OrderCategory(models.Model):
    """카테고리 순서 갱신용 모델"""
    c_pk = models.OneToOneField('Category',unique=True)
    order_num = models.IntegerField()
    objects = models.Manager()
    order = OrderManager()

    def __str__(self):
        return self.c_pk.name


# 포스트 발행 관리 매니저
class PublishMixin(object):
    """
    포스트 발행 관리를 위한 믹스인
    """
    def publish(self):
        """발행된 포스트 목록"""
        return self.filter(publish=True)

    def dreft(self):
        """미발행 포스트(초안) 목록"""
        return self.filter(publish=False)

class PublishQuerySets(QuerySet, PublishMixin):
    pass

class PublishManager(models.Manager,PublishMixin):
    def get_query_set(self):
        return PublishQuerySets(self.model,using=self._db)

# 포스트 모델
class Post(models.Model,HitCountMixin):
    """
    블로그 포스트 모델
    """
    category = models.ForeignKey('Category',blank=True,null=True)
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User)
    description = models.CharField(max_length=160,blank=True,null=True,help_text="포스트를 sns에 공유하거나 검색에서 노출될 포스트에 대한 요약입니다.")
    content = RichTextUploadingField()
    tag = TaggableManager()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False,help_text="포스트 발행시 외부에 포스트가 공개됩니다. 만약 발행하지 않는다면 작성자만 해당 포스트를 볼 수 있습니다.")

    # hitcount 모듈과 연동
    posthits = GenericRelation(HitCount, related_query_name='post',object_id_field='object_pk')

    objects = models.Manager()
    # 발행 포스트 관리 매니저
    published = PublishManager()

    def __str__(self):
        return self.title






