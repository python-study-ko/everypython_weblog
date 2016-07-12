from django.shortcuts import render, render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from blog.models import Category, Post


from django_jinja.views.generic.detail import DetailView
# Create your views here.
from taggit.models import Tag

def sidebar_context():
    """
    사이드바 위젯에 들어갈 context을 넘겨주는 함수로 선사이드바가 있는 뷰에 자체 컨텍스트에 이것을 합쳐 템플릿에 넘겨주면 된다.
    :return:
    """
    level1 = Category.objects.filter(level=1)
    context_dic={'categorys': level1,'tags':Tag.objects.all().reverse()}
    return context_dic

def under_c(c):
    """
    하위 카테고리 리스트를 만들어 준다
    :param category:
    :return:
    """
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

def c_postlist(c_list):
    # 카테고리 목록을 받아 해당 카테고리에 속한 모든 포스트 가져와서 정렬시킨다.
    post_list = []
    # 모든 포스트를 가져온
    for c in c_list:
        post_list += c.post_set.all()
    # 포스트의 번호를 역순으로 하여 정렬한
    sortlist = sorted(post_list, key=lambda x: x.pk , reverse=True)
    return sortlist

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

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context.update(sidebar_context())
        return context

# jinja2 테스트 코드
def jinjadef(request):
    test = 'abcd'
    manydict = {1:{"first":1,"second":2,"tree":{3:33}}}
    return render(request,'blog/def.jinja',{'hi' :test,"test":manydict})

class jinjaclass(DetailView):
    model = Post

