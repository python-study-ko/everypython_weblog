from django.shortcuts import render, render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from blog.models import Category, Post
from django.conf import settings

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
    categorytree = Category.tree.navi_bar()
    context_dic={'tags':tags,'categorytree':categorytree}
    return context_dic


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
        data = render_to_string("blog/index.html", context, request=request)
        return HttpResponse(data)


def CategoryList(request,pk):
    c = get_object_or_404(Category,pk=pk)
    categorys = Category.tree.under_list(c)
    if c.level == 3:
        post_list = Post.objects.filter(category=c).order_by('-id').values_list('pk', 'create_date',
                                                                                            'title', 'posthits__hits')
    else:
        categorys = Category.tree.under_list(c)
        post_list = Post.objects.filter(category__in=categorys).order_by('-id').values_list('pk', 'create_date', 'title', 'posthits__hits')

    # 포스트 목록
    context = {"posts": post_list,"name":c.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    return render(request,'blog/category.jinja',context)

def TagList(request,pk):
    tag = Tag.objects.get(id=pk)
    # 태그에 속한 모든 포스트를 찾는다
    posts = Post.objects.filter(tag__name__in=[tag]).order_by('-id').values_list('pk', 'create_date', 'title', 'posthits__hits')

    context = {"posts": posts,"name":tag.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    return render(request,'blog/tag.jinja',context)

class PostDetail(DetailView):
    model = Post
    count_hit = True
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # 포스트 태그 리스트를 생성
        tags = Post.objects.get(pk=self.kwargs.get('pk')).tag.get_queryset().values_list('id','name')
        context['posttag'] = tags
        context['shortname'] = getattr(settings,'SHORTNAME')
        # 사이드바에 필요한 context를 합쳐줌
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

