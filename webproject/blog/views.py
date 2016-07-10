from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from blog.models import Category, Post


from django_jinja.views.generic.detail import DetailView
# Create your views here.
from taggit.models import Tag

class Index(View):
    def get(self, request, data=None):
        level1 = Category.objects.filter(level=1)
        data = render_to_string("blog/index.jinja", {"post": ['test',2],'categorys': level1,'tags':Tag.objects.all().reverse()},
                                request=request)
        return HttpResponse(data)


class CategoryList(ListView):
    model = Category
    template_name = 'blog/category.jinja'

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/postdetail.jinja'

# jinja2 테스트 코드
def jinjadef(request):
    test = 'abcd'
    manydict = {1:{"first":1,"second":2,"tree":{3:33}}}
    return render(request,'blog/def.jinja',{'hi' :test,"test":manydict})

class jinjaclass(DetailView):
    model = Post

