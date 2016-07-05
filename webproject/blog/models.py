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

    # 하위 카테고리를 추출해주는 메소드 : 반환값의 len()이 0일경우 하위카테고리 없음 처리
    def under_list(self):
        """
        해당 객체의 하위 카테고리를 추출한다.
        :return: 하위 카테고리가 없으면 Noen / 있으면 리스트에 해당객체를 담아
        """
        # 하위 카테고리 목록 초기화
        cate_list = None

        # 보조 함수
        def check_list(u_list):
            """
            하위 카테고리 존재여부 확인
            :param u_list: 하위 카테고리 리스트
            :return: 하위 카테고리가 존재하지 않은면 None값을 반환
            """
            if len(u_list) == 0:
                return None
            else:
                return u_list

        # 1차 카테고리
        if self.level == 1:
            u_list = [x for x in self.under_category.all().reverse() if x.level == 2]
            cate_list = check_list(u_list)

        # 2차 카테고리
        elif self.level == 2:
            u_list = [x for x in self.under_category.all().reverse() if x.level == 3]
            cate_list = check_list(u_list)
        # 3차 카테고리 : 하위 카테고리를 가질수 없음
        else:
            cate_list = None

        return cate_list
    """
    하위 카테고리 사용 예시
    a = Category.objects.get(id=1)
    for x in a.under_list():
        print("하위 카테고리 {}".format(x))
        if x.under_list() != None:
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






