from django.shortcuts import render, render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from blog.models import Category, Post


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
    context_dic={'tags':tags(),'categorytree':categoryinfo()}
    return context_dic

# --------태그 함수-------------
def tags():
    """
    전체 태그정보를 (번호,태그명)형식으로 담아 리스트로 내보낸다
    :return:
    """
    tags = []
    taglist = Tag.objects.all()
    for tag in taglist:
        info = (tag.id,tag.name)
        tags.append(info)
    return tags

# --------태그 함수끝-----------

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

# --------카테고리 함수 끝 ----------

def c_postlist(c_list):
    # 카테고리 목록을 받아 해당 카테고리에 속한 모든 포스트 가져와서 정렬시킨다.
    post_list = []
    # 모든 포스트를 가져온
    for c in c_list:
        post_list += c.post_set.all()
    # 포스트의 번호를 역순으로 하여 정렬한
    sortlist = sorted(post_list, key=lambda x: x.pk , reverse=True)

    posts = []
    for post in sortlist:
        info = (post.pk,post.create_date,post.title,post.hit_count.hits)
        posts.append(info)
    return posts

class Index(View):
    def get(self, request, data=None):

        # index 페이지에 넘겨줄 컨텐츠 context
        context ={}
        # 사이드바에 필요한 context를 합쳐줌
        context.update(sidebar_context())
        data = render_to_string("blog/index.jinja", context, request=request)
        return HttpResponse(data)


def CategoryList(request,pk):
    category = get_object_or_404(Category,pk=pk)
    # 모든 하위카테고리를 구한후 해당 카테고리들의 모든 포스트를 추출한다.
    post_list = c_postlist(under_c(category))
    # 포스트 목록
    context = {"posts": post_list,"name":category.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    # 테스트 코드
    return render(request,'blog/category.jinja',context)

def TagList(request,pk):
    tag = Tag.objects.get(id=pk)
    # 태그에 속한 모든 포스트를 찾는다
    post_list = Post.objects.filter(tag__name__in=[tag])
    context = {"posts": post_list,"name":tag.name}
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

