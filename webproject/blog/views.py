from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import View
from .models import Category, Post
from django.conf import settings
from django.db.models import Count

from hitcount.models import HitCount
from taggit.models import Tag
from hitcount.views import HitCountDetailView

def sidebar_context():
    """
    사이드바 위젯에 들어갈 context을 넘겨주는 함수.
    context.update(sidebar_context())이걸 통해 각페이지 context에 카테고리나 태그정보가 담긴 context를 함께 넘겨준다
    :return:
    """
    tags = Tag.objects.all().filter(post__publish=True).annotate(Count('post')).values_list('id','name','post__count')
    categorytree = Category.tree.navi_bar()
    context_dic={'tags':tags,'categorytree':categorytree}
    return context_dic


class Index(View):
    def get(self, request, data=None):
        # index 페이지에 넘겨줄 컨텐츠 context
        # 최신글 목록 추출
        newposts = Post.published.publish().values_list('pk','create_date','title','category__name').order_by('-create_date')[:2]

        # 인기글 목록 추출
        starposts = HitCount.objects.all().filter(post__publish=True).values_list('post__pk', 'hits', 'post__title', 'post__category__name')[:3]

        # 사이드바에 필요한 context를 합쳐줌
        context = {'newposts':newposts,'starposts':starposts}
        context.update(sidebar_context())
        data = render_to_string("blog/index.html", context, request=request)
        return HttpResponse(data)


def CategoryList(request,pk):
    c = get_object_or_404(Category,pk=pk)
    categorys = Category.tree.under_list(c)
    if c.level == 3:
        post_list = Post.published.publish().filter(category=c).order_by('-id').values_list('pk', 'create_date',
                                                                                            'title', 'posthits__hits')
    else:
        categorys = Category.tree.under_list(c)
        post_list = Post.published.publish().filter(category__in=categorys).order_by('-id').values_list('pk', 'create_date', 'title', 'posthits__hits')

    # 포스트 목록
    context = {"posts": post_list,"name":c.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    return render(request,'blog/category.html',context)

def TagList(request,name):
    tag = Tag.objects.get(name=name)
    # 태그에 속한 모든 포스트를 찾는다
    posts = Post.published.publish().filter(tag__name__in=[tag]).order_by('-id').values_list('pk', 'create_date', 'title', 'posthits__hits')

    context = {"posts": posts,"name":tag.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(sidebar_context())
    return render(request,'blog/tag.html',context)

class PostDetail(HitCountDetailView):
    model = Post
    count_hit = True
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # 포스트 태그 리스트를 생성
        tags = Post.objects.get(pk=self.kwargs.get('pk')).tag.get_queryset().annotate(Count('post')).values_list('id','name','post__count')
        context['posttag'] = tags
        context['shortname'] = getattr(settings,'SHORTNAME')
        # 사이드바에 필요한 context를 합쳐줌
        context.update(sidebar_context())
        return context


