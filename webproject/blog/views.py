from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import View
from .models import Category, Post
from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from hitcount.models import HitCount
from taggit.models import Tag
from hitcount.views import HitCountDetailView


def base_context():
    """
    블로그에 기본적으로 들어갈 context을 넘겨주는 함수. (사이드바,구글 태그 매니저)
    context.update(base_context())  통해 각페이지 context에 카테고리 정보를 넘겨준다
    :return:
    """
    gtm = getattr(settings,'GTM_STATE')
    categorytree = Category.tree.navi_bar()
    context_dic = {'categorytree': categorytree, 'gtm': gtm}
    return context_dic

def makepage(request,post_list,viewnum=8):
    """
    포스트목록을 페이지 처리를 하여 포스트목록을 반환한다.
    :param request: 처리할 요청의 request/ page 정보값을 알아낼때 사용
    :param post_list: 포스트 목록에 뿌려질 정보 모음
    :param viewnum: 한 페이지에 보여줄 포스트 수
    :return: 해당 페이지에 맞는 포스트 목록
    """
    # 페이지 번호
    page = request.GET.get('page')
    # 넘겨받은 자료를 페이징 처리
    paginator = Paginator(post_list, viewnum)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts

class Index(View):
    def get(self, request, data=None):
        # index 페이지에 넘겨줄 컨텐츠 context
        tags = Tag.objects.all().filter(post__publish=True).annotate(Count('post')).values_list('name', 'post__count')
        publish = Post.published.publish()
        # 최신글 목록 추출
        q_newposts = publish.order_by('-create_date')[:2]
        newposts = Post.published.posts_info(q_newposts)

        # 인기글 목록 추출
        q_starposts = publish.order_by('-posthits__hits')[:3]
        starposts = Post.published.posts_info(q_starposts)


        # 사이드바에 필요한 context를 합쳐줌
        context = {'tags': tags, 'newposts': newposts, 'starposts': starposts}
        context.update(base_context())
        data = render_to_string("blog/index.html", context, request=request)
        return HttpResponse(data)


def CategoryList(request, name):
    c = get_object_or_404(Category, name=name)
    categorys = Category.tree.under_list(c)
    if c.level == 3:
        post_queryset = Post.published.publish().filter(category=c).order_by('-id')
    else:
        categorys = Category.tree.under_list(c)
        post_queryset = Post.published.publish().filter(category__in=categorys).order_by('-id')
    post_list = Post.published.posts_info(post_queryset)

    #포스트 목록 페이지 처리
    posts = makepage(request,post_list,viewnum=3)

    context = {"posts": posts, "name": c.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(base_context())
    return render(request, 'blog/category.html', context)


def TagList(request, name):
    tag = Tag.objects.get(name=name)
    # 태그에 속한 모든 포스트를 찾는다
    post_queryset = Post.published.publish().filter(tag__name__in=[tag]).order_by('-id')
    post_list = Post.published.posts_info(post_queryset)

    #포스트 목록 페이지 처리
    posts = makepage(request,post_list)

    context = {"posts": posts, "name": tag.name}
    # 사이드바에 필요한 context를 합쳐줌
    context.update(base_context())
    return render(request, 'blog/tag.html', context)


class PostDetail(HitCountDetailView):
    model = Post
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

        context['shortname'] = getattr(settings, 'SHORTNAME')
        context['og'] = getattr(settings,'OG_TAG')
        if getattr(settings,'AD_STATE'):
            context['ad'] = getattr(settings,'AD_STATE')

        # 사이드바에 필요한 context를 합쳐줌
        context.update(base_context())
        return context
