from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from taggit.models import Tag
from hitcount.models import HitCountMixin, HitCount
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Sum, Case, When, IntegerField
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
        """ 입력받은 카테고리에 대한 하위카테고리 목록을 쿼리셋으로 돌려준 """
        order = "ordercategory__order_num"
        if c.level == 1:
            c2 = Category.objects.filter(parent=c)
            under_C = Category.objects.filter(Q(name=c) | Q(parent=c) | Q(parent__in=c2)).order_by(order)
        elif c.level == 2:
            under_C = Category.objects.filter(Q(name=c) | Q(parent=c)).order_by(order)
        elif c.level == 3:
            under_C = c
        return under_C

    def navi_bar(self):
        """
        네비게이션 바에 뿌려줄 카테고리 목록을 만들어주는 함수
        전체 카테고리에 대한 정보를 추출하여 뷰와 템플릿에서 처리하기 쉽도록 아래의 구조로 바꿔준다.
        -- return값 구조
            카테고리 리스트엔 각 최상위 카테고리와 그 하위 카테고리 정보가 담긴 리스트들로 구성되있다.
            예시 : [ [(카테고리1),(카테고리1-1),..], [(카테고리2),(카테고리2-1),...] ]
        """
        c_list = Category.objects.all().order_by("ordercategory__order_num")
        # 발행된 포스트만 계수하기 위한 ORM : 발행=1, 미발행=0으로 하여 총 합을 구한다.
        postcount=Sum(Case(When(post__publish=True, then=1), default=0, output_field=IntegerField()))
        #  전체 카테고리의 정보를 튜플로 추출한다.
        c_info = c_list.annotate(count_posts=postcount).values_list('level', 'name', 'count_posts')

        # 카테고리 정보를 뷰와 템플릿에서 처리하기 쉽도록 구조를 변경한다.
        category_tree = []
        c_underlist = []
        for c in c_info:
            if c[0]==1: # 최상위 카테고리
                if c_underlist: # 이전 최상위 카테고리 목록이 존재할 경우 카테고리 목록 초기화
                    category_tree.append(c_underlist)
                    c_underlist = []
                c_underlist.append(c)
            else: # 차상위 카테고리
                c_underlist.append(c)
        category_tree.append(c_underlist) # 마지막 촤상위 카테고리 목록 추가
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

    parent = models.ForeignKey('self',limit_choices_to=Q(level=1)|Q(level=2),on_delete=models.CASCADE,blank=True,null=True,help_text="상위 카테고리를 정해주세요,미지정시 최상위 카테고리가 됩니", verbose_name='상위 카테고리')
    name = models.CharField(max_length=15,unique=True,help_text="카테고리 이름을 입력하세요", verbose_name='이름')
    level = models.IntegerField(choices=[(1, '최상위 카테고리'), (2, '2차 카테고리'), (3, '3차 카테고리')], blank=True, verbose_name='단계')
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

    def posts_info(self,post_queryset):
        """
        포스트 목록 쿼리셋을 받아 포스트목록에 보여줄 정보를 취합하여 list로 넘겨준다
        list에 담겨지는 포스 정보의 구조 : (pk,category,created_date,hitcounts,title,description(없을시엔 contnent의 100자까지로 대체),tags)
        """
        posts = list(post_queryset.select_related('category').prefetch_related('tag'))
        info_list = [(p.pk, p.category.name, p.create_date, p.title, p.description if p.description else p.content[:100] , [t.name for t in p.tag.all()]) for p in posts]
        return info_list


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
    category = models.ForeignKey('Category',blank=True,null=True, verbose_name='카테고리')
    title = models.CharField(verbose_name='제목', max_length=60)
    author = models.ForeignKey(User, verbose_name='글쓴이')
    description = models.CharField(verbose_name='요약', max_length=160,blank=True,null=True,help_text="포스트를 sns에 공유하거나 검색에서 노출될 포스트에 대한 요약입니다.")
    content = RichTextUploadingField(verbose_name='내용')
    markdown = models.BooleanField(verbose_name="마크다운",default=False,blank=True,help_text="마크다운 형식으로 글을 작성하려면 체크하세")
    tag = TaggableManager()
    create_date = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    edit_date = models.DateTimeField(verbose_name='수정일', auto_now=True)
    publish = models.BooleanField(verbose_name='발행여부', default=False,help_text="포스트 발행시 외부에 포스트가 공개됩니다. 만약 발행하지 않는다면 작성자만 해당 포스트를 볼 수 있습니다.")

    # hitcount 모듈과 연동
    posthits = GenericRelation(HitCount, related_query_name='post',object_id_field='object_pk')

    objects = models.Manager()
    # 발행 포스트 관리 매니저
    published = PublishManager()

    def __str__(self):
        return self.title



