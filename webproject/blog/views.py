from django.shortcuts import render, render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from blog.models import Category, Post
from django.db.models import Q


from hitcount.models import HitCount
from taggit.models import Tag
from django_jinja.views.generic.base import Jinja2TemplateResponseMixin
from hitcount.views import HitCountDetailView as hitdetailview


class DetailView(Jinja2TemplateResponseMixin,hitdetailview):
    """
    조회수를 측정할 hitdetailview클래스에 jinjan 템플릿 클래스를 믹스인 시켜준다.
    """
    pass

def sidebar_context():
    """
    사이드바 위젯에 들어갈 context을 넘겨주는 함수.
    context.update(sidebar_context())이걸 통해 각페이지 context에 카테고리나 태그정보가 담긴 context를 함께 넘겨준다
    :return:
    """
    tags = Tag.objects.all().values_list('id','name')
    context_dic={'tags':tags,'categorytree':categoryinfo()}
    return context_dic



# --------카테고리 함수----------

def under_c(c):
    # 하위 카테고리 리스트를 만들어 준다
    if c.under_list():
        allc = []
        allc += [c]
        for c2 in c.under_list():
            allc += [c2]
            if c2.under_list():
                allc += c2.under_list()
        return allc

    # 하위 카테고리가 없을 경우
    else:
        return [c]

def categorytree():
    # 전체 카테고리 리스트를 만들어 준다
    c1 = Category.objects.filter(level=1)
    ctree=[]
    for c in c1:
        ctree.append(under_c(c))
    return ctree

def categoryinfo():
    # 카테고리 세부 정보를 모아준다 - (레벨,번호,이름,하위 포스트 갯수)
    c_info = []
    for group in categorytree():
        groupinfo = []
        for c in group:
            info = (c.level,c.id,c.name,len(c.post_set.all()))
            groupinfo.append(info)
        c_info.append(groupinfo)
    return c_info

def c_postlist(c_list):
    # 카테고리 목록을 받아 해당 카테고리에 속한 모든 포스트 가져와서 정렬시킨다.
    post_list = []
    # 모든 포스트를 가져온
    for c in c_list:
        post_list += c.post_set.all()
    # 포스트의 번호를 역순으로 하여 정렬한
    post_obj_list = sorted(post_list, key=lambda x: x.pk , reverse=True)
    posts = postcontext(post_obj_list)
    return posts


# -----글목록 정보 추출 함수-----------

def postcontext(post_obj_list):
    posts = []
    for post in post_obj_list:
        info = (post.pk, post.create_date, post.title, post.hit_count.hits)
        posts.append(info)
    return posts


class Index(View):
    def get(self, request, data=None):
        # index 페이지에 넘겨줄 컨텐츠 context
        # 최신글 목록 추출
        newposts = Post.objects.all().values_list('pk','create_date','title','category__name').order_by('-create_date')[:5]

        # 인기글 목록 추출
        starposts = HitCount.objects.all().values_list('post__pk', 'hits', 'post__title', 'post__category__name')[:5]

        # 사이드바에 필요한 context를 합쳐줌
        context = {'newposts':newposts,'starposts':starposts}
        context.update(sidebar_context())
        data = render_to_string("blog/index.jinja", context, request=request)
        return HttpResponse(data)


def CategoryList(request,pk):
    c = get_object_or_404(Category,pk=pk)

    # 쿼리 최적화
    if c.level == 1:
        c2 = c.under_category.filter(level=2)
        c3 = c2.filter(under_category__level=3).values_list('under_category__id',flat=True)
        under_C = Category.objects.filter(
            Q(id=c.id) | Q(id__in=c2.values_list("id", flat=True)) | Q(id__in=c3)).values_list('id',flat=True)
    elif c.level == 2:
        under_C = Category.objects.filter(
            Q(id=c.id) | Q(id__in=c.under_category.filter(level=3).values_list("id", flat=True))).values_list('id', flat=True)
    elif c.level == 3:
        under_C = [c.id]

    post_list = Post.objects.filter(category__id__in=under_C).order_by('-id').values_list('pk', 'create_date', 'title', 'posthits__hits')

    # 포스트 목록
    context = {"posts": post_list,"name":c.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    return render(request,'blog/category.jinja',context)

def TagList(request,pk):
    tag = Tag.objects.get(id=pk)
    # 태그에 속한 모든 포스트를 찾는다
    post_obj_list = Post.objects.filter(tag__name__in=[tag])
    posts = postcontext(post_obj_list)

    context = {"posts": posts,"name":tag.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    return render(request,'blog/tag.jinja',context)

class PostDetail(DetailView):
    model = Post
    count_hit = True
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['tagmodel']=Tag
        context.update(sidebar_context())
        return context

# jinja2 테스트 코드
def jinjadef(request):
    test = 'abcd'
    cycle = 'a','b','c','d'
    manydict = {1:{"first":1,"second":2,"tree":{3:33}}}
    return render(request,'blog/def.jinja',{'hi' :test,"test":manydict,'cylist':cycle})

class jinjaclass(DetailView):
    model = Post


"""
포스트 글목록 로직
현재까지 구현한부분
from django.db.models import Q
c = Category.objects.get(id=2) #최상위 카테고리중 하나
>>> Category.objects.filter(Q(id=c.id)|Q(id__in=c.under_category.values_list("id",flat=True)))
결과 : [<Category: 웹프레임워크>, <Category: 파이썬>, <Category: GUI>]
>>> under_c = Category.objects.filter(Q(id=c.id)|Q(id__in=c.under_category.values_list("id",flat=True))).values_list('id',flat=True)
결과 : [1, 2, 12]
--- 최상위 카테고리와 2차 카테고리를 리스트로 만들어줌
Post.objects.filter(category__id__in=under_c).order_by('-create_date')
--- 포스트 모델에서 카테고리명이 겹치는 포스트를 불러와 최신순으로 정렬하기
---카테고리 목록이 구해지면 포스트 목록을 구하는 쿼리는 구현완료
---하위 카테고리 목록을 구현하는 쿼리 제작해야함

"""

